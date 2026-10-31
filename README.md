# no-feed-skills

本仓库收录七个可独立调用的 Agent Skills。

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

## 安装

以下命令安装本仓库中的全部 Skills：

```bash
npx -y skills add zhj022326-commits/no-feed-skills -g --all
```

## 使用

- 研究问题并组装文章：使用 `$knowledge-assembler`。
- 还原第一人称自述：使用 `$self-narrative-restoration`。
- 维护人生档案：使用 `$life-archive`。
- 检查文案是否误伤目标观众：使用 `$three-part-method`。
- 评估开口、寻找理论或把观点变成开口：使用 `$content-production`。
- 立即开始互动学习：使用 `$interactive-learning`。
- 生成或检查情绪修辞角度：使用 `$eight-emotions-four-uses`。

## 运行依赖

- 支持 Agent Skills 的客户端

## 发布内容

仓库包含运行这些 Skills 所需的入口说明、客户端元数据和参考材料。本地自动评测结果与运行记录不包含在公开包中。
