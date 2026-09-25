#!/usr/bin/env python3
"""Sort VS Code settings.json object keys recursively."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from typing import Any

DEFAULT_SETTINGS = Path.home() / "AppData" / "Roaming" / "Code" / "User" / "settings.json"


def sort_keys(value: Any) -> Any:
    """Sort JSON object keys recursively while preserving array order."""
    if isinstance(value, dict):
        return {key: sort_keys(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [sort_keys(item) for item in value]
    return value


def object_pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Detect duplicate keys in one JSON object; last value wins (dict semantics)."""
    seen: set[str] = set()
    duplicates: list[str] = []
    for key, _ in pairs:
        if key in seen:
            duplicates.append(key)
        seen.add(key)
    if duplicates:
        print(f"警告: 对象中存在重复键 {sorted(set(duplicates))}，仅保留最后一个值。")
    return dict(pairs)


def load_json(path: Path) -> Any:
    """Read JSON with BOM tolerance; report parse errors with position, exit code 1."""
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as settings_file:
            return json.load(settings_file, object_pairs_hook=object_pairs_hook)
    except json.JSONDecodeError as error:
        raise SystemExit(
            f"JSON 解析失败: {path}\n"
            f"  错误: {error.msg}（第 {error.lineno} 行，第 {error.colno} 列）"
        ) from None


def sort_settings(path: Path) -> None:
    settings = load_json(path)
    sorted_settings = sort_keys(settings)
    if json.dumps(settings) == json.dumps(sorted_settings):
        print(f"按键名已有序，无需修改: {path}")
        return
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            prefix=f"{path.name}.",
            suffix=".sorted.tmp",
            dir=path.parent,
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            json.dump(sorted_settings, temporary_file, ensure_ascii=False, indent=4)
            temporary_file.write("\n")
        with temporary_path.open("r", encoding="utf-8", newline="") as temporary_file:
            verified_settings = json.load(temporary_file)
        if verified_settings != settings:
            raise ValueError("临时文件校验失败，源文件未修改。")
        # Atomic on the same volume: the temp file lives next to the target.
        temporary_path.replace(path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    print(f"已按键名排序: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="递归排序 VS Code settings.json 的对象键名，保持数组顺序不变。"
    )
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=DEFAULT_SETTINGS,
        help=f"设置文件路径（默认: {DEFAULT_SETTINGS}）",
    )
    args = parser.parse_args()
    if not args.path.is_file():
        parser.error(f"找不到设置文件: {args.path}")
    sort_settings(args.path)


if __name__ == "__main__":
    main()
