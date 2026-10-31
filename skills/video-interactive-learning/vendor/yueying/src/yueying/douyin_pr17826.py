"""Temporary compatibility transplant of yt-dlp PR #17826.

Source: https://github.com/yt-dlp/yt-dlp/pull/17826
Pinned source commit: 728fe46fbaa97d6f03efcaf9e766d4db63338b8d

The upstream PR is Unlicense code.  This module changes only DouyinIE and is a
no-op after an official yt-dlp release contains the complete patch surface.
"""

from __future__ import annotations

import hashlib
import json
import time
import urllib.parse
import uuid

from yt_dlp.extractor.tiktok import DouyinIE
from yt_dlp.utils import ExtractorError
from yt_dlp.utils.traversal import traverse_obj


PATCH_COMMIT = "728fe46fbaa97d6f03efcaf9e766d4db63338b8d"
_PATCHED_ATTR = "_YUEYING_PR17826_PATCHED"
_REQUIRED_METHODS = (
    "_get_ttwid",
    "check_and_get_required_cookies",
    "_get_uifid",
    "_sign_query",
    "_get_aweme_detail",
)


def _get_ttwid(self):
    self._request_webpage(f"{self._WEBPAGE_HOST}ttwid/register", None, data=json.dumps({
        "aid": self._AID,
        "service": "www.douyin.com",
    }).encode(), headers={
        "content-type": "application/json",
    })
    cookie = self._get_cookies(self._WEBPAGE_HOST).get("ttwid")
    return cookie.value if cookie else None


def check_and_get_required_cookies(self):
    for required_cookie in self._REQUIRED_COOKIES:
        if self._get_cookies(self._WEBPAGE_HOST).get(required_cookie):
            continue
        if required_cookie == "ttwid":
            cookie = self._get_ttwid()
        else:
            cookie = self._CSRF
        if not cookie:
            raise ExtractorError("Unable to generate required cookies")
        self._set_cookie(".douyin.com", required_cookie, cookie)


def _get_uifid(self):
    uifid_cookie_names = (
        "uifid",
        "uifid_temp",
        "uifidtemp",
        "UIFID",
        "UIFID_TEMP",
        "UIFIDTEMP",
    )
    uifid = traverse_obj(
        self._get_cookies(self._WEBPAGE_HOST),
        (uifid_cookie_names, "value"),
        get_all=False,
    )
    if not uifid:
        url_handle = self._request_webpage(self._WEBPAGE_HOST, None)
        return url_handle.headers.get("x-tt-trace-host")
    return uifid


def _sign_query(self, query):
    salt = self._SEC_SALT
    uifid = self._get_uifid()
    timestamp = str(int(time.time()))
    query = {**query, "uifid": uifid, "timestamp": timestamp}
    encoded_query = urllib.parse.urlencode(query)
    signature = hashlib.md5(
        f"{uifid}_{timestamp}_{salt}_{encoded_query}".encode()
    ).hexdigest()
    return {**query, "x-secsdk-web-signature": signature}


def _get_aweme_detail(self, video_id):
    return traverse_obj(self._download_json(
        "https://www.douyin.com/aweme/v1/web/aweme/detail/",
        video_id,
        "Downloading web detail JSON",
        "Failed to download web detail JSON",
        query=self._sign_query({"aweme_id": video_id, "aid": self._AID}),
        fatal=False,
    ), ("aweme_detail", {dict}))


def _real_extract(self, url):
    video_id = self._match_id(url)

    self.check_and_get_required_cookies()
    aweme_detail = self._get_aweme_detail(video_id)
    if not aweme_detail:
        raise ExtractorError(
            "Fresh cookies (not necessarily logged in) are needed",
            expected=not self._get_cookies(self._WEBPAGE_HOST).get("s_v_web_id"),
        )

    return {
        **self._parse_aweme_video_app(aweme_detail),
        "http_headers": {"Referer": self._WEBPAGE_HOST},
    }


def apply() -> bool:
    """Apply PR #17826 to the installed yt-dlp DouyinIE once.

    Returns True when this call transplanted the patch, False when an official
    implementation or an earlier call already provides it.
    """
    if getattr(DouyinIE, _PATCHED_ATTR, False):
        return False
    if all(hasattr(DouyinIE, method) for method in _REQUIRED_METHODS):
        return False

    DouyinIE._SEC_SALT = "A96D855A08C0A9707F8BEF0D9A527E4E"
    DouyinIE._REQUIRED_COOKIES = ["passport_csrf_token", "ttwid"]
    DouyinIE._AID = 6383
    DouyinIE._CSRF = uuid.uuid4().hex
    DouyinIE._get_ttwid = _get_ttwid
    DouyinIE.check_and_get_required_cookies = check_and_get_required_cookies
    DouyinIE._get_uifid = _get_uifid
    DouyinIE._sign_query = _sign_query
    DouyinIE._get_aweme_detail = _get_aweme_detail
    DouyinIE._real_extract = _real_extract
    setattr(DouyinIE, _PATCHED_ATTR, True)
    return True
