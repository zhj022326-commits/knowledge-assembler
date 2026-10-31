#!/usr/bin/env python3
"""Thin, deterministic wrapper around the vendored Yueying pipeline.

Transcript mode fetches subtitles or audio only. Frame mode is a one-shot
rescue path and deliberately disables ASR.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def build_command(args: argparse.Namespace, root: Path) -> tuple[list[str], Path]:
    target = Path(args.output_dir).expanduser().resolve()
    if args.mode == "transcript":
        out_dir = target / "raw"
        command = [
            sys.executable, "-m", "yueying.cli", args.source,
            "--out", str(out_dir), "--no-frames", "--model", args.model,
            "--device", args.device, "--ui-lang", "zh", "--json",
        ]
        if args.lang:
            command.extend(["--lang", args.lang])
        if args.force_asr:
            command.append("--force-asr")
    else:
        out_dir = target / "frame-rescue"
        command = [
            sys.executable, "-m", "yueying.cli", args.source,
            "--out", str(out_dir), "--no-asr", "--interval", str(args.frame_interval),
            "--ui-lang", "zh", "--json",
        ]
    if args.cookies_from_browser:
        command.extend(["--cookies-from-browser", args.cookies_from_browser])
    return command, out_dir


def run(command: list[str], root: Path) -> int:
    vendor_src = root / "vendor" / "yueying" / "src"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(vendor_src) + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.Popen(
        command,
        cwd=str(root),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.stdout is not None
    for line in proc.stdout:
        print(line, end="", flush=True)
    return proc.wait()


def load_manifest(out_dir: Path) -> dict | None:
    path = out_dir / "manifest.json"
    if not path.is_file():
        return None
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="字幕/语音优先的视频文字稿提取器")
    parser.add_argument("--source", required=True, help="视频链接或本地视频路径")
    parser.add_argument("--output-dir", required=True, help="本次视频的工作目录")
    parser.add_argument("--mode", choices=("transcript", "frames"), default="transcript")
    parser.add_argument("--lang", help="语音语言代码，如 zh、en；默认自动检测")
    parser.add_argument("--model", default="auto", help="Whisper 模型，默认 auto")
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    parser.add_argument("--force-asr", action="store_true", help="忽略平台字幕，强制语音识别")
    parser.add_argument("--frame-interval", type=float, default=2.0, help="救稿抽帧间隔，默认 2 秒")
    parser.add_argument("--cookies-from-browser", choices=("chrome", "edge", "firefox"))
    parser.add_argument("--json", action="store_true", help="输出结果 JSON")
    args = parser.parse_args(argv)

    root = Path(__file__).resolve().parents[1]
    command, out_dir = build_command(args, root)
    out_dir.mkdir(parents=True, exist_ok=True)
    code = run(command, root)
    manifest = load_manifest(out_dir)

    if code != 0:
        status = "extract_failed"
        exit_code = 1
    elif manifest is None:
        status = "missing_manifest"
        exit_code = 2
    elif args.mode == "transcript" and (manifest.get("text_source") or {}).get("kind") == "none":
        status = "no_transcript"
        exit_code = 3
    elif args.mode == "frames" and not manifest.get("frames"):
        status = "no_frames"
        exit_code = 4
    else:
        status = "success"
        exit_code = 0

    result = {
        "status": status,
        "mode": args.mode,
        "output_dir": str(out_dir),
        "manifest": str(out_dir / "manifest.json") if manifest else None,
        "transcript": manifest.get("transcript_txt") if manifest else None,
        "text_source": manifest.get("text_source") if manifest else None,
        "frames": len(manifest.get("frames") or []) if manifest else 0,
        "grids": manifest.get("grids") if manifest else [],
    }
    if args.json:
        print("VIDEO_LEARNING_RESULT=" + json.dumps(result, ensure_ascii=False), flush=True)
    else:
        print(status, flush=True)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

