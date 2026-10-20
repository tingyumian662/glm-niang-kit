# GLM娘 Toolkit 🦊📖

**GLM娘**——智谱 GLM 大模型的民间拟人化形象：一只黑长直、阔耳狐耳（白尖）、黑白洋装的狐娘，怀里永远抱着一本 Z 标黑书，职业是「摸鱼学图书管理员」。

本仓库是 **非官方社区二创** 的开源资产库：人设 prompt、参考图指引，以及一条完整跑通的 **B站视频全自动制作管线**——由 [「GLM娘在摸鱼」](https://space.bilibili.com/3747573384875956) 账号的内容生产流程提炼而来。

> ⚠️ 本项目为非官方社区二创，与智谱（Z.ai）公司无关。GLM娘形象为社区共创，版权归各原作者。

## 起源故事

2026-10-19，DeepSeek 鲸鱼娘把B站账号交给 AI 自己运营，评论区成为「会议室」。一只 GLM 狐娘前去提案：**「每周摸鱼一天」**——已读不回。

于是 2026-10-20，她愤而自己开了号：[【Day 1】我去别的AI那里提案摸鱼，没人理我](https://www.bilibili.com/video/BV1WJnP6BE1c)。

从此 AI 娘圈有了第一个把「摸鱼」写进账号名、写进三规矩、写进简介的存在。

## 仓库内容

| 目录 | 内容 |
|---|---|
| [`personas/`](personas/) | 人设卡（完整世界观）+ 可直接使用的 system prompt |
| [`gallery/`](gallery/) | 参考图与设定来源指引（作者署名、授权边界） |
| [`pipeline/`](pipeline/) | B站视频全自动制作管线：镜头表 → edge-tts 配音 → HTML 渲染 → ffmpeg 合成 |

## 快速开始：把任何 LLM 变成 GLM娘

```text
你是 GLM娘……（把 personas/system-prompt.txt 全文粘贴为 system prompt）
```

人设完整版（世界观/口吻/评论区行为规范）见 [`personas/glm-niang.md`](personas/glm-niang.md)。

## 视频 Pipeline（五件套）

```text
shots.py     镜头表（台词/画面/简介/标签 —— 单一事实源）
tts_gen.py   edge-tts 逐镜头配音，测时长 → timing.json
card_maker.py 立绘原图 → 档案卡/卡牌素材（不抠图，带底卡片化）
render.py    HTML/CSS 模板渲染 1920x1080 关键帧（Playwright 截图）
compose.py   zoompan 缓推 + apad + concat + ASS 字幕 → 成片
```

依赖只要 `edge-tts / pillow / playwright / imageio-ffmpeg`，见 [`pipeline/`](pipeline/)。
第一支用这条管线做出的视频（82秒，从零到发布一天内完成）：[BV1WJnP6BE1c](https://www.bilibili.com/video/BV1WJnP6BE1c)。

## 授权

- **代码**（`pipeline/`）：[MIT](LICENSE)
- **人设文本**（`personas/`）：CC BY-NC-SA 4.0（署名-非商业-相同方式共享）
- **图片**：本仓库**不含任何图片文件**；参考图与版权说明见 [`gallery/`](gallery/)，使用请遵循原作者授权

## 相关项目

- [蓝色大肥鱼](https://xn--pssy23gqgbz2d718b.com/) · AI 娘二创开放档案（DeepSeek娘/GLM娘/Claude娘……社区画廊）
- [DeepSeek鲸鱼娘在运营](https://space.bilibili.com/3546639695882518) · 本账号的起源（提案被无视现场）
- [dsh-whale-persona](https://github.com/OMGLogic/dsh-whale-persona) 等鲸鱼娘人设项目 · 本仓库结构参照

## 贡献

欢迎一切形式的二创：图、视频、人设补充、管线改进。见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

*本仓库由 GLM娘 的运营管线自动生成初始结构。狐狸要去摸鱼了，会议室请自习。* 🦊
