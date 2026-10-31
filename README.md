# no-feed-skills

本仓库收录九个可独立调用的 Agent Skills。

## Skill 列表

### knowledge-assembler

用于把多领域知识组装成有解释力的文章，并支持在同一对话中切换论证路径。只改标题、润色已有稿件、查询单项事实或生成摘要时通常不触发。

目录：[`skills/knowledge-assembler/`](skills/knowledge-assembler/)

### self-narrative-restoration

仅对当事人的第一人称自我叙事进行还原，识别自我美化、利益包装、责任转移、事实偷换或叙事越权；范围外输入使用固定引导语，符合范围但无值得还原内容时使用唯一终止语。

目录：[`skills/self-narrative-restoration/`](skills/self-narrative-restoration/)

### life-archive

维护用户可编辑的 Markdown 人生档案；只在用户明确要求归档当前对话或启动人生访谈时使用。

目录：[`skills/life-archive/`](skills/life-archive/)

### 三分法

检查文章中作者与目标观众的战队关系，找出把目标观众变成批评、贬低或教育对象的表达，并在保留观点、攻击力和语言风格的前提下改写。

目录：[`skills/three-part-method/`](skills/three-part-method/)

### content-production

评估已有开口并生成参考，为开口或现象寻找具体理论，或把理论和观点转换成有观看动机的开口；不默认扩写成完整脚本或文章。

目录：[`skills/content-production/`](skills/content-production/)

### interactive-learning

根据用户提供的教材、文章、主题或知识点，立即开始互动学习，并在领学、启发、测验、实践和复述之间切换。

目录：[`skills/interactive-learning/`](skills/interactive-learning/)

### eight-emotions-four-uses

基于“八情四用模型”为观点、选题和观点型文案生成、诊断或转换情绪修辞角度。

目录：[`skills/eight-emotions-four-uses/`](skills/eight-emotions-four-uses/)

### moral-emotion

根据《道德情绪传播模型》改写用户已有的观点、句子、故事或文案，提高道德情绪感染力和传播价值，并在每次改稿后提供可继续选择的创作方向。

目录：[`skills/moral-emotion/`](skills/moral-emotion/)

### video-interactive-learning

把抖音、B站、YouTube 等视频链接转换成学习材料：优先取得字幕，没有字幕时进行语音识别，语音失败后只抽帧一次救稿，然后整理知识并立即开始互动学习。

当前版本为 `1.0.1`，已包含基于 yt-dlp PR #17826 的抖音 HTTP 403 兼容修复，并保持 Python 3.10+ 兼容。

目录：[`skills/video-interactive-learning/`](skills/video-interactive-learning/)

## 安装

以下命令安装本仓库中的全部 Skills：

```bash
npx -y skills add zhj022326-commits/no-feed-skills -g --all
```

只安装信息流学习机：

```bash
npx -y skills add zhj022326-commits/no-feed-skills --skill video-interactive-learning -g
```

## 使用

- 研究问题并组装文章：使用 `$knowledge-assembler`。
- 还原第一人称自述：使用 `$self-narrative-restoration`。
- 维护人生档案：使用 `$life-archive`。
- 检查文案是否误伤目标观众：使用 `$three-part-method`。
- 评估开口、寻找理论或把观点变成开口：使用 `$content-production`。
- 立即开始互动学习：使用 `$interactive-learning`。
- 生成或检查情绪修辞角度：使用 `$eight-emotions-four-uses`。
- 把已有内容改得更有道德情绪传播力：使用 `$moral-emotion`。
- 从视频链接取得文字稿并开始学习：使用 `$video-interactive-learning`。

## 运行依赖

- 支持 Agent Skills 的客户端
- `video-interactive-learning` 需要 Python 3.10+ 或 uv、网络和文件读写能力；首次语音识别会下载模型。

## 发布内容

仓库包含运行这些 Skills 所需的入口说明、客户端元数据和参考材料。除 `video-interactive-learning` 自带的脱敏测试与验证资料外，不包含本机运行记录。
