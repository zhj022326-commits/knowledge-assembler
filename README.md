# no-feed-skills

本仓库收录三个可独立调用的 Agent Skills。

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

## 安装

以下命令安装本仓库中的全部 Skills：

```bash
npx -y skills add zhj022326-commits/no-feed-skills -g --all
```

## 使用

- 研究问题并组装文章：使用 `$knowledge-assembler`。
- 还原第一人称自述：使用 `$self-narrative-restoration`。
- 维护人生档案：使用 `$life-archive`。

## 运行依赖

- 支持 Agent Skills 的客户端

## 发布内容

仓库包含运行这些 Skills 所需的入口说明、客户端元数据和参考材料。本地自动评测结果与运行记录不包含在公开包中。