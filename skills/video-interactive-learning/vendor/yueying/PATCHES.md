# Integration changes

Upstream source: Yueying 0.2.1 at commit `e8fb72eabf9a2193b8d8cf5ce4e5c17de4edbcfe`.

Minimal integration changes:

1. Renamed the nested upstream `SKILL.md` to `UPSTREAM_SKILL.md`, and updated package data/install references, so the distributable contains exactly one top-level Agent Skill entry file.
2. Added `transcript_only` and `force_asr` inputs to the downloader.
3. In transcript-only mode, platform subtitles use yt-dlp `skip_download`; when no subtitle is available, yt-dlp downloads best audio only.
4. Allowed the CLI to process a subtitle-only result without a media file and skip ffmpeg probing in that case.
5. Expanded recognized media extensions to include common audio containers used by yt-dlp.
6. Pinned `av<19` because PyAV 19 removed the `metadata_errors` argument still used by faster-whisper 1.2.1.

The original full video/keyframe behavior remains available and is used by the one-shot frame rescue path.
