from __future__ import annotations

import argparse
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock


SKILL_ROOT = Path(__file__).resolve().parents[1]
VENDOR_SRC = SKILL_ROOT / "vendor" / "yueying" / "src"
if str(VENDOR_SRC) not in sys.path:
    sys.path.insert(0, str(VENDOR_SRC))
if str(SKILL_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT / "scripts"))

from yueying import download as download_module  # noqa: E402
import extract_transcript  # noqa: E402


class FakeYoutubeDL:
    calls: list[dict] = []
    info: dict = {}

    def __init__(self, options):
        self.options = dict(options)
        self.__class__.calls.append(self.options)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def extract_info(self, url, download=False):
        return dict(self.__class__.info)

    def download(self, urls):
        template = self.options["outtmpl"]
        if self.options.get("skip_download"):
            ext = "zh.vtt"
            content = "WEBVTT\n\n00:00.000 --> 00:01.000\nhello\n"
        elif self.options.get("format") == "bestaudio/best":
            ext = "m4a"
            content = "audio"
        else:
            ext = "mp4"
            content = "video"
        path = Path(template.replace("%(ext)s", ext))
        path.write_text(content, encoding="utf-8")


class DownloadFastPathTests(unittest.TestCase):
    def setUp(self):
        FakeYoutubeDL.calls = []

    def _run(self, info, **kwargs):
        FakeYoutubeDL.info = info
        fake_module = types.SimpleNamespace(YoutubeDL=FakeYoutubeDL)
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(sys.modules, {"yt_dlp": fake_module}):
            with mock.patch.object(download_module.ffm, "ffmpeg_exe", return_value="ffmpeg"):
                result = download_module.download("https://example.test/video", tmp, log=lambda _msg: None, **kwargs)
            return result, list(FakeYoutubeDL.calls)

    def test_platform_subtitles_skip_media_download(self):
        info = {
            "title": "captioned", "duration": 10, "webpage_url": "https://example.test/video",
            "subtitles": {"zh": [{"ext": "vtt"}]}, "automatic_captions": {},
        }
        result, calls = self._run(info, transcript_only=True)
        self.assertIsNone(result["video"])
        self.assertTrue(result["subs"])
        self.assertTrue(calls[-1]["skip_download"])
        self.assertNotIn("format", calls[-1])

    def test_no_subtitles_downloads_audio_only(self):
        info = {
            "title": "spoken", "duration": 10, "webpage_url": "https://example.test/video",
            "subtitles": {}, "automatic_captions": {},
        }
        result, calls = self._run(info, transcript_only=True)
        self.assertTrue(result["video"].endswith(".m4a"))
        self.assertEqual(calls[-1]["format"], "bestaudio/best")
        self.assertNotIn("merge_output_format", calls[-1])

    def test_frame_mode_retains_video_download(self):
        info = {
            "title": "slides", "duration": 10, "webpage_url": "https://example.test/video",
            "subtitles": {}, "automatic_captions": {},
        }
        result, calls = self._run(info, transcript_only=False)
        self.assertTrue(result["video"].endswith(".mp4"))
        self.assertIn("height<=720", calls[-1]["format"])
        self.assertEqual(calls[-1]["merge_output_format"], "mp4")


class WrapperCommandTests(unittest.TestCase):
    def _args(self, mode):
        return argparse.Namespace(
            output_dir="out", mode=mode, source="https://example.test/video",
            model="auto", device="auto", lang=None, force_asr=False,
            frame_interval=2.0, cookies_from_browser=None,
        )

    def test_transcript_mode_disables_frames_only(self):
        command, out_dir = extract_transcript.build_command(self._args("transcript"), SKILL_ROOT)
        self.assertIn("--no-frames", command)
        self.assertNotIn("--no-asr", command)
        self.assertEqual(out_dir.name, "raw")

    def test_rescue_mode_disables_asr_and_keeps_frames(self):
        command, out_dir = extract_transcript.build_command(self._args("frames"), SKILL_ROOT)
        self.assertIn("--no-asr", command)
        self.assertNotIn("--no-frames", command)
        self.assertEqual(out_dir.name, "frame-rescue")


if __name__ == "__main__":
    unittest.main()
