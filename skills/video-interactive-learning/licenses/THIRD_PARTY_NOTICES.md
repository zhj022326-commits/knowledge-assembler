# Third-party notices

## Yueying（阅影）

- Project: https://github.com/vsh5dvsch7-png/yueying
- Vendored revision: `e8fb72eabf9a2193b8d8cf5ce4e5c17de4edbcfe`
- License: MIT
- Copyright: 2026 yueying contributors

The complete upstream MIT license is preserved at `vendor/yueying/LICENSE`. The vendored source is retained substantially intact; integration changes are documented in `vendor/yueying/PATCHES.md`.

## Runtime dependencies declared by Yueying

These packages are resolved at install/run time and are not copied into this Skill package:

- faster-whisper — MIT
- PyAV — BSD-3-Clause (constrained to `<19` for faster-whisper compatibility)
- yt-dlp — The Unlicense
- imageio-ffmpeg — BSD-2-Clause
- Pillow — HPND / MIT-CMU style license
- Model Context Protocol Python SDK — MIT

`imageio-ffmpeg` supplies an ffmpeg executable. FFmpeg licensing depends on the distributed build and enabled components; inspect the runtime binary's license/configuration when redistributing it separately. This Skill package does not embed that binary.
