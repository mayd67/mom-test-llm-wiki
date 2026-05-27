#!/usr/bin/env python3
"""Fetch Jira board sprints and suggest the most suitable sprint for a date."""

from __future__ import annotations

import base64
import json
import os
import re
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib import error, request

BOARD_SPRINTS_PATH = "/rest/agile/1.0/board/{board_id}/sprint"
SPRINT_DETAIL_PATH = "/rest/agile/1.0/sprint/{sprint_id}"
DEFAULT_DB_SQL_CANDIDATES = [
    Path(r"D:\07_Git\km-rde\backend\km-rde\scripts\db.sql"),
]
BOARD_ID_SQL_RE = re.compile(
    r"\(SEQ_ID\.NEXTVAL,\s*'jira\.boardId',\s*'[^']*',\s*'(?P<board_id>[^']+)',\s*'PROJECT',\s*'(?P<project_code>[^']+)'\)"
)


class SprintCatalogError(RuntimeError):
    """Raised when sprint catalog resolution fails."""


@dataclass
class SprintConnectionConfig:
    api_base_url: str
    username: str
    password: str
    board_id: str
    project_key: str
    project_code: str
    timeout_seconds: int
    km_rde_db_sql_path: str


@dataclass
class JiraSprint:
    id: str
    name: str
    state: str
    start_date: str
    end_date: str


def read_secret(
    config: Dict[str, Any],
    direct_key: str,
    env_key: str,
    direct_override: str = "",
    env_override: str = "",
) -> str:
    if direct_override.strip():
        return direct_override.strip()
    if env_override.strip():
        return os.environ.get(env_override.strip(), "").strip()

    direct_value = str(config.get(direct_key, "")).strip()
    if direct_value:
        return direct_value

    env_name = str(config.get(env_key, "")).strip()
    if env_name:
        return os.environ.get(env_name, "").strip()
    return ""


def load_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SprintCatalogError(f"Config file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SprintCatalogError(f"Config file is not valid JSON: {path}: {exc}") from exc


def discover_board_id(project_code: str, db_sql_path_text: str) -> Tuple[str, str]:
    candidates: List[Path] = []
    if db_sql_path_text.strip():
        candidates.append(Path(db_sql_path_text.strip()))
    candidates.extend(DEFAULT_DB_SQL_CANDIDATES)

    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen or not candidate.exists():
            continue
        seen.add(candidate)
        text = candidate.read_text(encoding="utf-8", errors="replace")
        matches = [
            match.groupdict()
            for match in BOARD_ID_SQL_RE.finditer(text)
            if not project_code or match.group("project_code").strip() == project_code
        ]
        if len(matches) == 1:
            return matches[0]["board_id"].strip(), str(candidate)
        if len(matches) > 1:
            raise SprintCatalogError(
                f"Found multiple jira.boardId entries for project_code={project_code or '<empty>'} in {candidate}"
            )

    return "", ""


def load_sprint_connection_config(
    config_path: Path,
    username_override: str = "",
    password_override: str = "",
    username_env_override: str = "",
    password_env_override: str = "",
) -> SprintConnectionConfig:
    raw = load_json(config_path)
    api_base_url = str(raw.get("api_base_url", "")).strip().rstrip("/")
    username = read_secret(raw, "username", "username_env", username_override, username_env_override)
    password = read_secret(raw, "password", "password_env", password_override, password_env_override)
    project_key = str(raw.get("project_key", "")).strip()
    project_code = str(raw.get("project_code", "")).strip()
    board_id = str(raw.get("board_id", "")).strip()
    km_rde_db_sql_path = str(raw.get("km_rde_db_sql_path", "")).strip()
    timeout_seconds = int(raw.get("timeout_seconds", 30) or 30)

    discovered_from = ""
    if not board_id:
        board_id, discovered_from = discover_board_id(project_code, km_rde_db_sql_path)

    if not api_base_url:
        raise SprintCatalogError("Config must provide api_base_url.")
    if not username or not password:
        raise SprintCatalogError("Config must provide Jira credentials or *_env indirection.")
    if not board_id:
        hint = ""
        if discovered_from:
            hint = f" Tried reading board id from {discovered_from}."
        raise SprintCatalogError(
            "Config must provide board_id, or provide project_code plus km_rde_db_sql_path so board_id can be discovered."
            + hint
        )

    return SprintConnectionConfig(
        api_base_url=api_base_url,
        username=username,
        password=password,
        board_id=board_id,
        project_key=project_key,
        project_code=project_code,
        timeout_seconds=timeout_seconds,
        km_rde_db_sql_path=km_rde_db_sql_path or discovered_from,
    )


def encode_basic_auth(username: str, password: str) -> str:
    token = f"{username}:{password}".encode("utf-8")
    return base64.b64encode(token).decode("ascii")


def request_json(cfg: SprintConnectionConfig, method: str, path: str) -> Any:
    url = path if path.startswith("http://") or path.startswith("https://") else f"{cfg.api_base_url}{path}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {encode_basic_auth(cfg.username, cfg.password)}",
    }
    req = request.Request(url, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=cfg.timeout_seconds) as resp:
            body = resp.read()
            if not body:
                return {}
            text = body.decode("utf-8")
            return json.loads(text) if text.strip() else {}
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SprintCatalogError(f"{method} {url} failed with HTTP {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise SprintCatalogError(f"{method} {url} failed: {exc}") from exc


def parse_iso_date(value: str) -> str:
    text = value.strip()
    if not text:
        return ""
    return text[:10]


def to_sprint(node: Dict[str, Any]) -> JiraSprint:
    return JiraSprint(
        id=str(node.get("id", "")).strip(),
        name=str(node.get("name", "")).strip(),
        state=str(node.get("state", "")).strip(),
        start_date=parse_iso_date(str(node.get("startDate", "") or "")),
        end_date=parse_iso_date(str(node.get("endDate", "") or "")),
    )


def fetch_sprint_detail(cfg: SprintConnectionConfig, sprint_id: str) -> JiraSprint:
    node = request_json(cfg, "GET", SPRINT_DETAIL_PATH.format(sprint_id=sprint_id))
    if not isinstance(node, dict):
        raise SprintCatalogError(f"Unexpected sprint detail response for sprint {sprint_id}")
    return to_sprint(node)


def fetch_board_sprints(cfg: SprintConnectionConfig) -> List[JiraSprint]:
    start_at = 0
    max_results = 50
    seen_ids: set[str] = set()
    results: List[JiraSprint] = []

    while True:
        path = f"{BOARD_SPRINTS_PATH.format(board_id=cfg.board_id)}?startAt={start_at}&maxResults={max_results}"
        node = request_json(cfg, "GET", path)
        if not isinstance(node, dict):
            raise SprintCatalogError("Unexpected board sprint response.")

        values = node.get("values", [])
        if not isinstance(values, list):
            raise SprintCatalogError("Board sprint response missing values array.")

        for item in values:
            if not isinstance(item, dict):
                continue
            sprint = to_sprint(item)
            if sprint.id in seen_ids:
                continue
            if not sprint.start_date or not sprint.end_date:
                try:
                    sprint = fetch_sprint_detail(cfg, sprint.id)
                except SprintCatalogError:
                    pass
            seen_ids.add(sprint.id)
            results.append(sprint)

        is_last = bool(node.get("isLast", False))
        if is_last or not values:
            break
        start_at += max_results

    return results


def parse_date_text(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def suggest_sprint(sprints: List[JiraSprint], today: date) -> Tuple[Optional[JiraSprint], str]:
    dated = [item for item in sprints if item.start_date and item.end_date]
    active_now = [
        item
        for item in dated
        if parse_date_text(item.start_date) <= today <= parse_date_text(item.end_date)
    ]
    active_now.sort(key=lambda item: (item.state != "active", item.end_date, item.id))
    if active_now:
        chosen = active_now[0]
        return chosen, f"当前日期 {today.isoformat()} 落在 Sprint {chosen.name}({chosen.id}) 的周期内。"

    future = [item for item in dated if parse_date_text(item.start_date) > today]
    future.sort(key=lambda item: (item.start_date, item.id))
    if future:
        chosen = future[0]
        return chosen, f"当前日期 {today.isoformat()} 不在已知 Sprint 周期内，已选择最近即将开始的 Sprint {chosen.name}({chosen.id})。"

    closed = [item for item in dated if parse_date_text(item.end_date) < today]
    closed.sort(key=lambda item: (item.end_date, item.id), reverse=True)
    if closed:
        chosen = closed[0]
        return chosen, f"当前日期 {today.isoformat()} 晚于已知 Sprint 周期，已选择最近结束的 Sprint {chosen.name}({chosen.id})。"

    if sprints:
        chosen = sorted(sprints, key=lambda item: item.id)[-1]
        return chosen, f"无法取得完整日期区间，已回退到最后一个已读取 Sprint {chosen.name}({chosen.id})。"

    return None, "未读取到任何 Sprint。"


def build_sprint_catalog(cfg: SprintConnectionConfig, today: date) -> Dict[str, Any]:
    sprints = fetch_board_sprints(cfg)
    suggestion, reason = suggest_sprint(sprints, today)
    return {
        "project_key": cfg.project_key,
        "project_code": cfg.project_code,
        "board_id": cfg.board_id,
        "today": today.isoformat(),
        "suggestion_reason": reason,
        "suggested_sprint": asdict(suggestion) if suggestion else {},
        "sprints": [asdict(item) for item in sorted(sprints, key=lambda sprint: (sprint.start_date, sprint.id))],
    }


def load_sprint_catalog(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SprintCatalogError(f"Sprint catalog not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SprintCatalogError(f"Sprint catalog is not valid JSON: {path}: {exc}") from exc
