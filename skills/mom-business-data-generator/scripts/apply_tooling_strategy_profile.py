from __future__ import annotations

import argparse
import json
from pathlib import Path

from tooling_strategy_profiles import apply_profile


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='为种子文件补充工装检定/保养策略关系')
    parser.add_argument('--profile', required=True, help='工装策略配置名称，例如 automotive_engine')
    parser.add_argument('--seed', type=Path, required=True, help='待处理的种子 JSON 路径')
    parser.add_argument('--output', type=Path, default=None, help='输出路径；默认原地覆盖')
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    seed_path = args.seed
    output_path = args.output or seed_path
    with seed_path.open('r', encoding='utf-8-sig') as handle:
        seed = json.load(handle)
    summary = apply_profile(seed, args.profile)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open('w', encoding='utf-8-sig') as handle:
        json.dump(seed, handle, ensure_ascii=False, indent=2)
    print(json.dumps({'seed': str(output_path), 'summary': summary}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
