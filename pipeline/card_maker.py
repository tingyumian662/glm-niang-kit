# -*- coding: utf-8 -*-
"""card_maker.py —— 带底原图加工成「档案卡」（圆角+金边+内衬+标签条），不抠图。

用法：准备带浅色底的立绘原图放 assets/，运行后输出 frames/card_*.png
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ASSETS = Path(__file__).parent / "assets"   # 立绘原图目录
OUT = Path(__file__).parent / "frames"      # 输出目录
GOLD = (255, 205, 90)
DARK = (13, 18, 32)
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"  # 中文粗体字体；Linux 换 Noto Sans CJK


def make_card(src_name, out_name, label="GLM娘 · 档案照", rotate=0):
    im = Image.open(ASSETS / src_name).convert("RGB")
    H = 1400
    W = round(im.width * H / im.height)
    im = im.resize((W, H), Image.LANCZOS)
    pad = 28
    inner = Image.new("RGB", (W + pad * 2, H + pad * 2 + 90), (245, 243, 238))
    inner.paste(im, (pad, pad))
    d = ImageDraw.Draw(inner)
    d.rectangle([0, H + pad * 2, inner.width, inner.height], fill=DARK)
    f = ImageFont.truetype(FONT_BOLD, 44)
    tw = d.textlength(label, font=f)
    d.text(((inner.width - tw) / 2, H + pad * 2 + 20), label, font=f, fill=GOLD)
    outer = Image.new("RGB", (inner.width + 20, inner.height + 20), GOLD)
    outer.paste(inner, (10, 10))
    R = 36
    mask = Image.new("L", outer.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, outer.width, outer.height], R, fill=255)
    card = Image.new("RGBA", outer.size, (0, 0, 0, 0))
    card.paste(outer, (0, 0), mask)
    if rotate:
        card = card.rotate(rotate, expand=True, resample=Image.BICUBIC)
    OUT.mkdir(exist_ok=True)
    card.save(OUT / out_name)
    print(out_name, card.size)


if __name__ == "__main__":
    make_card("tachie_1.webp", "card_1.png", "GLM娘 · 档案照 №001")
