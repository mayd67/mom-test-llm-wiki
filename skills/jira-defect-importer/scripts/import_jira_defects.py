#!/usr/bin/env python3
"""Inspect Jira fields and create KMMOM defects from normalized CSV rows."""

from __future__ import annotations

import argparse
import base64
import csv
import json
import os
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from urllib import error, request

from jira_project_sprints import (
    SprintCatalogError,
    build_sprint_catalog,
    load_sprint_connection_config,
)

CREATE_ISSUE_PATH = "/rest/api/2/issue"
FIELDS_PATH = "/rest/api/2/field"
TRANSITIONS_PATH = "/rest/api/2/issue/{issue_key}/transitions"

DEFAULT_FIELD_MODES = {
    "责任人": "user",
    "测试责任人": "user",
    "缺陷产生者": "user",
    "缺陷严重程度": "option",
    "缺陷来源": "option",
    "缺陷引入阶段": "option",
    "模块": "option",
    "对用户的影响程度": "option",
    "Sprint": "number",
    "影响范围分析": "text",
}

CUSTOM_COLUMNS = [
    "责任人",
    "测试责任人",
    "缺陷产生者",
    "缺陷严重程度",
    "缺陷来源",
    "缺陷引入阶段",
    "模块",
    "对用户的影响程度",
    "Sprint",
    "影响范围分析",
]

REQUIRED_IMPORT_COLUMNS = ["概要", "描述"]


class JiraImportError(RuntimeError):
    """Raised when Jira import steps fail."""


@dataclass
class RuntimeConfig:
    api_base_url: str
    project_key: str
    username: str
    password: str
    user_identity_key: str
    default_issue_type: str
    default_create_status: str
    append_impact_analysis_to_description: bool
    strict_custom_fields: bool
    timeout_seconds: int
    field_map: Dict[str, str]
    field_modes: Dict[str, str]
    defaults: Dict[str, str]
    transition_name_map: Dict[str, str]
    transition_id_map: Dict[str, str]
    extra_fields: Dict[str, Any]
    omit_fields: set[str]


def load_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise JiraImportError(f"Config file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise JiraImportError(f"Config file is not valid JSON: {path}: {exc}") from exc


def read_secret(
    config: Dict[str, Any],
    direct_key: str,
    env_key: str,
    direct_override: str = "",
    env_override: str = "",
) -> str:
    direct = direct_override.strip()
    if direct:
        return direct

    if env_override.strip():
        return os.environ.get(env_override.strip(), "").strip()

    direct = str(config.get(direct_key, "")).strip()
    if direct:
        return direct
    env_name = str(config.get(env_key, "")).strip()
    if env_name:
        return os.environ.get(env_name, "").strip()
    return ""


def build_runtime_config(
    config_path: Path,
    require_auth: bool,
    username_override: str = "",
    password_override: str = "",
    username_env_override: str = "",
    password_env_override: str = "",
) -> RuntimeConfig:
    raw = load_json(config_path)
    api_base_url = str(raw.get("api_base_url", "")).strip().rstrip("/")
    project_key = str(raw.get("project_key", "")).strip()
    username = read_secret(raw, "username", "username_env", username_override, username_env_override)
    password = read_secret(raw, "password", "password_env", password_override, password_env_override)
    user_identity_key = str(raw.get("user_identity_key", "name")).strip() or "name"
    default_issue_type = str(raw.get("default_issue_type", "缺陷")).strip() or "缺陷"
    default_create_status = str(raw.get("default_create_status", "缺陷编制中")).strip() or "缺陷编制中"
    append_impact = bool(raw.get("append_impact_analysis_to_description", True))
    strict_custom_fields = bool(raw.get("strict_custom_fields", False))
    timeout_seconds = int(raw.get("timeout_seconds", 30) or 30)
    field_map = {str(key): str(value).strip() for key, value in dict(raw.get("field_map", {})).items()}
    field_modes = {str(key): str(value).strip() for key, value in dict(raw.get("field_modes", {})).items()}
    defaults = {str(key): str(value) for key, value in dict(raw.get("defaults", {})).items()}
    transition_name_map = {str(key): str(value).strip() for key, value in dict(raw.get("transition_name_map", {})).items()}
    transition_id_map = {str(key): str(value).strip() for key, value in dict(raw.get("transition_id_map", {})).items()}
    extra_fields = dict(raw.get("extra_fields", {}))
    omit_fields = {str(item).strip() for item in list(raw.get("omit_fields", [])) if str(item).strip()}

    if not project_key:
        raise JiraImportError("Config must provide project_key.")
    if require_auth:
        if not api_base_url:
            raise JiraImportError("Config must provide api_base_url for live Jira requests.")
        if not username or not password:
            raise JiraImportError("Config must provide Jira credentials or *_env indirection for live Jira requests.")

    return RuntimeConfig(
        api_base_url=api_base_url,
        project_key=project_key,
        username=username,
        password=password,
        user_identity_key=user_identity_key,
        default_issue_type=default_issue_type,
        default_create_status=default_create_status,
        append_impact_analysis_to_description=append_impact,
        strict_custom_fields=strict_custom_fields,
        timeout_seconds=timeout_seconds,
        field_map=field_map,
        field_modes=field_modes,
        defaults=defaults,
        transition_name_map=transition_name_map,
        transition_id_map=transition_id_map,
        extra_fields=extra_fields,
        omit_fields=omit_fields,
    )


def encode_basic_auth(username: str, password: str) -> str:
    token = f"{username}:{password}".encode("utf-8")
    return base64.b64encode(token).decode("ascii")


def request_json(cfg: RuntimeConfig, method: str, path: str, payload: Optional[Dict[str, Any]] = None) -> Any:
    if not cfg.api_base_url:
        raise JiraImportError("api_base_url is required for Jira requests.")

    url = path if path.startswith("http://") or path.startswith("https://") else f"{cfg.api_base_url}{path}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {encode_basic_auth(cfg.username, cfg.password)}",
    }
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    req = request.Request(url, data=data, headers=headers, method=method)

    try:
        with request.urlopen(req, timeout=cfg.timeout_seconds) as resp:
            body = resp.read()
            if not body:
                return {}
            text = body.decode("utf-8")
            if not text.strip():
                return {}
            return json.loads(text)
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise JiraImportError(f"{method} {url} failed with HTTP {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise JiraImportError(f"{method} {url} failed: {exc}") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect Jira fields and create KMMOM defects from CSV.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    import_parser = subparsers.add_parser("import", help="Create Jira defects from a normalized CSV file.")
    import_parser.add_argument("--username", type=str, default="", help="Override Jira login username for this run.")
    import_parser.add_argument("--password", type=str, default="", help="Override Jira login password for this run.")
    import_parser.add_argument("--username-env", type=str, default="", help="Read Jira login username from this environment variable.")
    import_parser.add_argument("--password-env", type=str, default="", help="Read Jira login password from this environment variable.")
    import_parser.add_argument("--config", required=True, type=str, help="Path to jira import config JSON.")
    import_parser.add_argument("--csv", required=True, type=str, help="Path to normalized defect CSV.")
    import_parser.add_argument("--dry-run", action="store_true", help="Only build payloads and warnings; do not call Jira.")
    import_parser.add_argument("--limit", type=int, default=0, help="Only process the first N rows.")
    import_parser.add_argument("--report", type=str, default="", help="Optional path to write JSON report.")

    fields_parser = subparsers.add_parser("fields", help="Query Jira field metadata.")
    fields_parser.add_argument("--username", type=str, default="", help="Override Jira login username for this run.")
    fields_parser.add_argument("--password", type=str, default="", help="Override Jira login password for this run.")
    fields_parser.add_argument("--username-env", type=str, default="", help="Read Jira login username from this environment variable.")
    fields_parser.add_argument("--password-env", type=str, default="", help="Read Jira login password from this environment variable.")
    fields_parser.add_argument("--config", required=True, type=str, help="Path to jira import config JSON.")
    fields_parser.add_argument("--names", nargs="*", default=[], help="Optional field names to filter by substring.")

    transitions_parser = subparsers.add_parser("transitions", help="Query available transitions for one issue.")
    transitions_parser.add_argument("--username", type=str, default="", help="Override Jira login username for this run.")
    transitions_parser.add_argument("--password", type=str, default="", help="Override Jira login password for this run.")
    transitions_parser.add_argument("--username-env", type=str, default="", help="Read Jira login username from this environment variable.")
    transitions_parser.add_argument("--password-env", type=str, default="", help="Read Jira login password from this environment variable.")
    transitions_parser.add_argument("--config", required=True, type=str, help="Path to jira import config JSON.")
    transitions_parser.add_argument("--issue-key", required=True, type=str, help="Existing Jira issue key.")

    sprints_parser = subparsers.add_parser("sprints", help="Read project sprints and suggest a sprint for the current date.")
    sprints_parser.add_argument("--username", type=str, default="", help="Override Jira login username for this run.")
    sprints_parser.add_argument("--password", type=str, default="", help="Override Jira login password for this run.")
    sprints_parser.add_argument("--username-env", type=str, default="", help="Read Jira login username from this environment variable.")
    sprints_parser.add_argument("--password-env", type=str, default="", help="Read Jira login password from this environment variable.")
    sprints_parser.add_argument("--config", required=True, type=str, help="Path to jira import config JSON.")
    sprints_parser.add_argument("--today", type=str, default="", help="Override current date with YYYY-MM-DD when suggesting a sprint.")
    sprints_parser.add_argument("--report", type=str, default="", help="Optional path to write sprint catalog JSON.")

    return parser.parse_args()


def read_csv_rows(csv_path: Path) -> List[Dict[str, str]]:
    try:
        with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = [
                {str(key).strip(): (value or "").strip() for key, value in row.items() if key is not None}
                for row in reader
            ]
    except FileNotFoundError as exc:
        raise JiraImportError(f"CSV file not found: {csv_path}") from exc

    if not rows:
        raise JiraImportError(f"CSV file has no data rows: {csv_path}")

    missing_columns = [column for column in REQUIRED_IMPORT_COLUMNS if column not in rows[0]]
    if missing_columns:
        raise JiraImportError(f"CSV is missing required columns: {', '.join(missing_columns)}")

    return rows


def normalize_due_date(value: str) -> str:
    text = value.strip()
    if not text:
        return ""

    for pattern in ("%Y/%m/%d", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, pattern).strftime("%Y-%m-%d")
        except ValueError:
            continue

    raise JiraImportError(f"到期日格式无效，应为 yyyy/MM/dd 或 yyyy-MM-dd: {value}")


def trim_empty_list(values: Iterable[str]) -> List[str]:
    return [value for value in (item.strip() for item in values) if value]


def apply_mode(mode: str, value: str, cfg: RuntimeConfig) -> Any:
    if mode == "user":
        return {cfg.user_identity_key: value}
    if mode == "option":
        return {"value": value}
    if mode == "component_array":
        return [{"name": value}]
    if mode == "text":
        return value
    if mode == "number":
        if value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
            return int(value)
        return float(value)
    if mode == "json":
        return json.loads(value)
    raise JiraImportError(f"Unsupported field mode: {mode}")


def get_effective_custom_value(column: str, row: Dict[str, str], cfg: RuntimeConfig) -> str:
    explicit = row.get(column, "").strip()
    if explicit:
        return explicit
    return str(cfg.defaults.get(column, "")).strip()


def is_omitted(cfg: RuntimeConfig, *keys: str) -> bool:
    return any(key.strip() in cfg.omit_fields for key in keys if key and key.strip())


def build_description(row: Dict[str, str], cfg: RuntimeConfig, warnings: List[str]) -> str:
    description = row.get("描述", "").strip()
    impact = row.get("影响范围分析", "").strip()
    impact_field_id = cfg.field_map.get("影响范围分析", "").strip()

    if impact and not impact_field_id:
        if cfg.append_impact_analysis_to_description:
            if description:
                description = f"{description}\n\n影响范围分析：\n{impact}"
            else:
                description = f"影响范围分析：\n{impact}"
        else:
            warnings.append("字段 影响范围分析 未配置 Jira 字段 ID，且未启用追加到描述，已跳过。")

    return description


def build_issue_payload(row: Dict[str, str], cfg: RuntimeConfig) -> Dict[str, Any]:
    warnings: List[str] = []
    summary = row.get("概要", "").strip()
    if not summary:
        raise JiraImportError("CSV 行缺少 概要。")

    description = build_description(row, cfg, warnings)
    issue_type = row.get("问题类型", "").strip() or cfg.default_issue_type
    if not description:
        warnings.append("描述 为空，Jira 是否允许空描述取决于实例配置。")

    fields: Dict[str, Any] = {
        "project": {"key": cfg.project_key},
        "issuetype": {"name": issue_type},
        "summary": summary,
        "description": description,
    }

    priority = row.get("优先级", "").strip()
    if priority and not is_omitted(cfg, "优先级", "priority"):
        fields["priority"] = {"name": priority}

    due_date = row.get("到期日", "").strip()
    if due_date and not is_omitted(cfg, "到期日", "duedate"):
        fields["duedate"] = normalize_due_date(due_date)

    version = row.get("使用的版本", "").strip()
    if version and not is_omitted(cfg, "使用的版本", "versions"):
        fields["versions"] = [{"name": version}]

    fix_version = row.get("修复的版本", "").strip()
    if fix_version and not is_omitted(cfg, "修复的版本", "fixVersions"):
        fields["fixVersions"] = [{"name": fix_version}]

    for column in CUSTOM_COLUMNS:
        value = get_effective_custom_value(column, row, cfg)
        field_id = cfg.field_map.get(column, "").strip()

        if not value:
            continue

        if is_omitted(cfg, column, field_id):
            continue

        if not field_id:
            if column == "影响范围分析" and cfg.append_impact_analysis_to_description:
                continue
            message = f"字段 {column} 有值但未配置 Jira 字段 ID，已跳过。"
            if cfg.strict_custom_fields:
                raise JiraImportError(message)
            warnings.append(message)
            continue

        mode = cfg.field_modes.get(column, DEFAULT_FIELD_MODES.get(column, "text")).strip()
        fields[field_id] = apply_mode(mode, value, cfg)

    if cfg.extra_fields:
        fields.update(cfg.extra_fields)

    requested_status = row.get("状态", "").strip() or cfg.default_create_status
    return {
        "fields": fields,
        "_warnings": warnings,
        "_requested_status": requested_status,
        "_summary": summary,
    }


def find_transition_id(cfg: RuntimeConfig, transitions: List[Dict[str, Any]], target_status: str) -> str:
    direct_id = cfg.transition_id_map.get(target_status, "").strip()
    if direct_id:
        return direct_id

    transition_name = cfg.transition_name_map.get(target_status, "").strip()
    if not transition_name:
        raise JiraImportError(
            f"状态 {target_status} 需要 transition，但配置中未提供 transition_name_map/transition_id_map。"
        )

    for item in transitions:
        if str(item.get("name", "")).strip() == transition_name:
            return str(item.get("id", "")).strip()

    raise JiraImportError(f"未在 Jira 可用 transition 中找到名称 {transition_name} 对应的状态 {target_status}。")


def fetch_transitions(cfg: RuntimeConfig, issue_key: str) -> List[Dict[str, Any]]:
    response = request_json(cfg, "GET", TRANSITIONS_PATH.format(issue_key=issue_key))
    transitions = response.get("transitions", [])
    if not isinstance(transitions, list):
        raise JiraImportError(f"Jira transitions 返回异常，issue={issue_key}")
    return transitions


def import_rows(rows: List[Dict[str, str]], cfg: RuntimeConfig, dry_run: bool) -> Dict[str, Any]:
    results: List[Dict[str, Any]] = []
    success_count = 0
    failure_count = 0

    for index, row in enumerate(rows, start=1):
        summary = row.get("概要", "").strip()
        try:
            payload = build_issue_payload(row, cfg)
            record = {
                "row_index": index,
                "summary": payload.pop("_summary"),
                "requested_status": payload.pop("_requested_status"),
                "warnings": payload.pop("_warnings"),
                "payload": payload,
                "status": "dry-run" if dry_run else "pending",
                "issue_key": "",
                "issue_id": "",
                "transition_applied": "",
                "error": "",
            }

            if dry_run:
                success_count += 1
                results.append(record)
                continue

            created = request_json(cfg, "POST", CREATE_ISSUE_PATH, record["payload"])
            record["issue_key"] = str(created.get("key", "")).strip()
            record["issue_id"] = str(created.get("id", "")).strip()
            record["status"] = "created"

            requested_status = record["requested_status"]
            if requested_status and requested_status != cfg.default_create_status:
                transitions = fetch_transitions(cfg, record["issue_key"])
                transition_id = find_transition_id(cfg, transitions, requested_status)
                request_json(
                    cfg,
                    "POST",
                    TRANSITIONS_PATH.format(issue_key=record["issue_key"]),
                    {"transition": {"id": transition_id}},
                )
                record["transition_applied"] = requested_status

            success_count += 1
            results.append(record)
        except Exception as exc:  # noqa: BLE001
            failure_count += 1
            results.append(
                {
                    "row_index": index,
                    "summary": summary,
                    "requested_status": row.get("状态", "").strip() or cfg.default_create_status,
                    "warnings": [],
                    "payload": {},
                    "status": "failed",
                    "issue_key": "",
                    "issue_id": "",
                    "transition_applied": "",
                    "error": str(exc),
                }
            )

    return {
        "mode": "dry-run" if dry_run else "import",
        "project_key": cfg.project_key,
        "success_count": success_count,
        "failure_count": failure_count,
        "results": results,
    }


def write_report(report_path: Path, data: Dict[str, Any]) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def print_fields(data: List[Dict[str, Any]]) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def handle_fields(args: argparse.Namespace) -> int:
    cfg = build_runtime_config(
        Path(args.config),
        require_auth=True,
        username_override=args.username,
        password_override=args.password,
        username_env_override=args.username_env,
        password_env_override=args.password_env,
    )
    fields = request_json(cfg, "GET", FIELDS_PATH)
    if not isinstance(fields, list):
        raise JiraImportError("Jira field metadata response is not a list.")

    filters = trim_empty_list(args.names)
    output: List[Dict[str, Any]] = []
    for item in fields:
        name = str(item.get("name", "")).strip()
        if filters and not any(token in name for token in filters):
            continue
        schema = item.get("schema", {}) if isinstance(item.get("schema", {}), dict) else {}
        output.append(
            {
                "id": item.get("id", ""),
                "name": name,
                "custom": item.get("custom", False),
                "schema_type": schema.get("type", ""),
                "schema_items": schema.get("items", ""),
                "schema_custom": schema.get("custom", ""),
            }
        )

    print_fields(output)
    return 0


def handle_transitions(args: argparse.Namespace) -> int:
    cfg = build_runtime_config(
        Path(args.config),
        require_auth=True,
        username_override=args.username,
        password_override=args.password,
        username_env_override=args.username_env,
        password_env_override=args.password_env,
    )
    transitions = fetch_transitions(cfg, args.issue_key)
    output = [
        {
            "id": item.get("id", ""),
            "name": item.get("name", ""),
            "to_status": item.get("to", {}).get("name", "") if isinstance(item.get("to", {}), dict) else "",
        }
        for item in transitions
    ]
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


def handle_sprints(args: argparse.Namespace) -> int:
    cfg = load_sprint_connection_config(
        Path(args.config),
        username_override=args.username,
        password_override=args.password,
        username_env_override=args.username_env,
        password_env_override=args.password_env,
    )
    today = datetime.strptime(args.today, "%Y-%m-%d").date() if args.today else date.today()
    catalog = build_sprint_catalog(cfg, today)
    print(json.dumps(catalog, ensure_ascii=False, indent=2))
    if args.report:
        write_report(Path(args.report), catalog)
    return 0


def print_import_summary(report: Dict[str, Any]) -> None:
    print(
        f"{report['mode']} completed for {report['project_key']}: "
        f"success={report['success_count']}, failure={report['failure_count']}"
    )
    for item in report["results"]:
        line = f"row {item['row_index']}: {item['status']} | {item['summary']}"
        if item.get("issue_key"):
            line += f" | {item['issue_key']}"
        if item.get("transition_applied"):
            line += f" | transitioned={item['transition_applied']}"
        if item.get("warnings"):
            line += f" | warnings={len(item['warnings'])}"
        if item.get("error"):
            line += f" | error={item['error']}"
        print(line)


def handle_import(args: argparse.Namespace) -> int:
    csv_path = Path(args.csv)
    cfg = build_runtime_config(
        Path(args.config),
        require_auth=not args.dry_run,
        username_override=args.username,
        password_override=args.password,
        username_env_override=args.username_env,
        password_env_override=args.password_env,
    )
    rows = read_csv_rows(csv_path)
    if args.limit and args.limit > 0:
        rows = rows[: args.limit]

    report = import_rows(rows, cfg, dry_run=args.dry_run)
    print_import_summary(report)

    if args.report:
        write_report(Path(args.report), report)

    if report["failure_count"]:
        return 1
    return 0


def main() -> int:
    args = parse_args()
    if args.command == "fields":
        return handle_fields(args)
    if args.command == "transitions":
        return handle_transitions(args)
    if args.command == "sprints":
        return handle_sprints(args)
    if args.command == "import":
        return handle_import(args)
    raise JiraImportError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (JiraImportError, SprintCatalogError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
