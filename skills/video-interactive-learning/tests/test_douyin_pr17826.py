from __future__ import annotations

import hashlib
import sys
import unittest
import urllib.parse
from pathlib import Path
from unittest import mock


SKILL_ROOT = Path(__file__).resolve().parents[1]
VENDOR_SRC = SKILL_ROOT / "vendor" / "yueying" / "src"
if str(VENDOR_SRC) not in sys.path:
    sys.path.insert(0, str(VENDOR_SRC))

from yueying.douyin_pr17826 import apply  # noqa: E402
from yt_dlp.extractor import tiktok  # noqa: E402


class DouyinPr17826Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        apply()

    def test_required_patch_surface_is_present(self):
        ie = tiktok.DouyinIE()
        self.assertEqual(ie._AID, 6383)
        self.assertEqual(ie._SEC_SALT, "A96D855A08C0A9707F8BEF0D9A527E4E")
        self.assertEqual(ie._REQUIRED_COOKIES, ["passport_csrf_token", "ttwid"])
        for method in (
            "_get_ttwid",
            "check_and_get_required_cookies",
            "_get_uifid",
            "_sign_query",
            "_get_aweme_detail",
        ):
            self.assertTrue(callable(getattr(ie, method, None)), method)

    def test_signature_matches_pr_algorithm(self):
        ie = tiktok.DouyinIE()
        with mock.patch.object(ie, "_get_uifid", return_value="test-uifid"):
            with mock.patch.object(tiktok.time, "time", return_value=1_700_000_000):
                signed = ie._sign_query({"aweme_id": "7695626378841984283", "aid": ie._AID})

        unsigned = {
            "aweme_id": "7695626378841984283",
            "aid": 6383,
            "uifid": "test-uifid",
            "timestamp": "1700000000",
        }
        encoded = urllib.parse.urlencode(unsigned)
        expected = hashlib.md5(
            f"test-uifid_1700000000_{ie._SEC_SALT}_{encoded}".encode()
        ).hexdigest()
        self.assertEqual(signed["x-secsdk-web-signature"], expected)

    def test_extractor_checks_cookies_and_adds_download_referer(self):
        ie = tiktok.DouyinIE()
        parsed = {"id": "7695626378841984283", "formats": []}
        with mock.patch.object(ie, "check_and_get_required_cookies") as check_cookies:
            with mock.patch.object(ie, "_get_aweme_detail", return_value={"aweme_id": "detail"}):
                with mock.patch.object(ie, "_parse_aweme_video_app", return_value=parsed):
                    result = ie._real_extract(
                        "https://www.douyin.com/video/7695626378841984283"
                    )

        check_cookies.assert_called_once_with()
        self.assertEqual(result["id"], parsed["id"])
        self.assertEqual(result["http_headers"], {"Referer": "https://www.douyin.com/"})


if __name__ == "__main__":
    unittest.main()
