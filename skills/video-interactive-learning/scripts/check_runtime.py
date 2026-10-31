#!/usr/bin/env python3
"""Check the bundled runtime once without installing or mutating anything."""

from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import shutil
import sys
from pathlib import Path


REQUIRED_MODULES = ("yt_dlp", "faster_whisper", "imageio_ffmpeg", "PIL")


def inspect_runtime() -> dict:
    root = Path(__file__).resolve().parents[1]
    vendor = root / "vendor" / "yueying"
    missing = [name for name in REQUIRED_MODULES if importlib.util.find_spec(name) is None]
    python_ok = sys.version_info >= (3, 10)
    vendor_ok = (vendor / "pyproject.toml").is_file() and (vendor / "src" / "yueying" / "cli.py").is_file()
    return {
        "ok": python_ok and vendor_ok and not missing,
        "python": platform.python_version(),
        "python_ok": python_ok,
        "vendor_ok": vendor_ok,
        "missing_modules": missing,
        "uv": shutil.which("uv"),
        "skill_root": str(root),
        "vendor_project": str(vendor),
        "notes": [
            "Run this script through `uv run --project vendor/yueying` so dependencies are prepared automatically."
        ] if missing else [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="检查信息流学习机的本地运行环境")
    parser.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    args = parser.parse_args()
    result = inspect_runtime()
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print("运行环境可用" if result["ok"] else "运行环境未就绪")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

