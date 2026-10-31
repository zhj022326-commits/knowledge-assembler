# Integration changes

Upstream source: Yueying 0.2.1 at commit `e8fb72eabf9a2193b8d8cf5ce4e5c17de4edbcfe`.

Minimal integration changes:

1. Renamed the nested upstream `SKILL.md` to `UPSTREAM_SKILL.md`, and updated package data/install references, so the distributable contains exactly one top-level Agent Skill entry file.
2. Added `transcript_only` and `force_asr` inputs to the downloader.
3. In transcript-only mode, platform subtitles use yt-dlp `skip_download`; when no subtitle is available, yt-dlp downloads best audio only.
4. Allowed the CLI to process a subtitle-only result without a media file and skip ffmpeg probing in that case.
5. Expanded recognized media extensions to include common audio containers used by yt-dlp.
6. Pinned `av<19` because PyAV 19 removed the `metadata_errors` argument still used by faster-whisper 1.2.1.
7. Transplanted the Douyin extractor changes from upstream yt-dlp PR #17826 at
   immutable commit `728fe46fbaa97d6f03efcaf9e766d4db63338b8d` into
   `src/yueying/douyin_pr17826.py`. The compatibility patch generates required
   cookies, signs the aweme detail query, passes `aid=6383`, and adds the CDN
   Referer. It patches only `DouyinIE`, is idempotent, and becomes a no-op once
   an official yt-dlp release exposes the same implementation. Keeping the
   released yt-dlp dependency preserves Yueying's Python 3.10 compatibility.
8. The public Agent Skill package omits upstream CI configuration, tests, test
   media, generated sample output, demo images, and developer-only documents to
   reduce installation time. Runtime source, CLI/MCP integrations, dependency
   declarations, licenses, and all video-processing behavior are retained.

The original full video/keyframe behavior remains available and is used by the one-shot frame rescue path.
