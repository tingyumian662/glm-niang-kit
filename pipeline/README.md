# B站视频全自动制作管线

从镜头表到 1080p 成片的五件套，零剪辑软件，纯代码。首个成品：[BV1WJnP6BE1c](https://www.bilibili.com/video/BV1WJnP6BE1c)（82秒，注册账号当天完成从制作到发布）。

## 架构

```text
shots.py        镜头表：台词/画面模板/简介/标签（全流程单一事实源）
  ↓
tts_gen.py      edge-tts 逐镜头配音 + ffprobe 测时长 → timing.json
card_maker.py   立绘原图 → 档案卡/卡牌素材（带底卡片化，不抠图）
render.py       HTML/CSS 模板 → Playwright+Edge 截 1920x1080 关键帧
  ↓
compose.py      每镜头 图+音频→段视频（zoompan缓推+apad）→ concat → ASS字幕烧录
```

## 使用

```bash
pip install -r requirements.txt
# 素材：自备立绘 PNG 放 frames/（或用 card_maker.py 从带底原图生成卡片素材）
python tts_gen.py      # 配音+时长
python render.py       # 渲染关键帧
python compose.py      # 合成 day1_final.mp4
```

- 浏览器：需要本机 Edge（或改 `render.py` 里 `EDGE` 路径为你的 Chrome）
- TTS 音色/语速在 `shots.py` 顶部（VOICE/RATE/PITCH）
- 画面模板在 `render.py` 的 `html_for()`（title/proposal/bigtext/tachi/book/blank/rules/banner/endcard 九种）

## 设计决策：带底卡片化

不做立绘抠图（边缘灰雾/幽灵感翻车重灾区）。立绘以「档案卡」形式呈现：
原图 + 米白衬 + 金边圆角 + 标签条，整卡放进画面。设定上正好是「狐狸出示各种证件」的叙事。

## 踩坑档案（真实血泪，按严重度排序）

1. **Playwright `set_content()` 页面不能加载 `file://` 图片**——about:blank 源被 Chromium
   安全策略静默拒绝（裂图不报错）。**所有图片必须 base64 内嵌 data URI**。
2. **zoompan 直接吃 1920px 输入会画面微颤**——每帧缩放增量<1px，取整跳变。
   标准解法：先 `scale=7680:-1` 再 zoompan，幅度收小（0.035）。
3. **`-shortest` 吃掉镜头间留白**——每段短 0.7s，15 镜头累计少 11 秒。用 `apad` 补到目标时长。
4. **视觉质检必须单帧大图+客观提问**（「画面里有什么」）；缩略网格+引导性提问（「立绘是否正常」）
   会被 AI 视觉模型误判通过——我们曾因此带着全空立绘过了两轮质检。
5. 投稿：B站新号首投有 406 极验风控，API/自动点击会被静默拦截，需人工过一次验证。

## LICENSE

本目录代码 MIT。生成内容的立绘素材版权遵循上游（见 [gallery/](../gallery/README.md)）。
