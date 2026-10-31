# 兼容性与运行说明

## Agent Skill 包

包顶层只有一个 `SKILL.md`，采用通用 Agent Skills 目录结构，并提供 `agents/openai.yaml`。可执行脚本和依赖项目全部位于 Skill 目录内部，便于 GPT/Codex 类本地 Agent 导入。

豆包/火山方舟支持上传自定义 Skill ZIP；本包按其顶层 `SKILL.md` 约束组织。能否真正执行取决于目标 Agent 是否开放 Python/uv、网络、文件读写与图片读取权限。仅能读取提示词、不能运行脚本的环境无法自动完成视频下载和本地 ASR。

## 运行依赖

- Python 3.10+，推荐由 `uv` 自动建立隔离环境。
- 网络可访问目标视频平台；受登录、会员、地区或反爬限制的视频可能需要浏览器 Cookie。
- 首次 ASR 会下载 faster-whisper 模型；默认 `auto` 在 CPU 上选 small，在 GPU 上选 large-v3-turbo。
- ffmpeg 由 imageio-ffmpeg 提供，不要求用户另行配置系统 ffmpeg。
- 抽帧救稿要求宿主 Agent 能读取生成的 JPG；否则必须把抽帧结果判为不可用，不能假装已经 OCR。

## 平台边界

实际平台支持范围由内置 yt-dlp 版本决定。包内暂时移植了 yt-dlp PR #17826 的抖音 403 修复，并已用公开抖音作品完成无 Cookie 的媒体获取与 ASR 实测。该 PR 尚未进入正式版，平台接口也可能继续变化；私密、已删除、登录态、地区限制和风控页面仍不能保证解析。失败后遵守主 Skill 的一次停止规则。
