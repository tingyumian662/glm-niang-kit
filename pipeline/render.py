# -*- coding: utf-8 -*-
"""render.py —— HTML/CSS 模板渲染 1920x1080 关键帧（Playwright 截图）。

关键点：图片必须 base64 内嵌（set_content 页面不能加载 file:// 资源）。
"""
import base64
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

from shots import SHOTS

ROOT = Path(__file__).resolve().parent
FRAMES = ROOT / "frames"
# 浏览器：优先环境变量 EDGE_PATH，其次常见安装位置，最后交给 playwright 默认
EDGE = os.environ.get("EDGE_PATH") or (
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe").exists() else None)

BASE_CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
html,body { width:1920px; height:1080px; overflow:hidden;
  font-family: "Microsoft YaHei", "PingFang SC", sans-serif; }
.stage { width:1920px; height:1080px; position:relative; overflow:hidden;
  background: radial-gradient(1200px 800px at 30% 20%, #16203a 0%, #0d1220 55%, #090d18 100%); }
.orb { position:absolute; border-radius:50%; filter:blur(2px); opacity:.10; background:#ffcd5a; }
.badge { display:inline-block; background:#e5484d; color:#fff; font-size:30px; font-weight:700;
  padding:10px 26px; border-radius:14px; letter-spacing:2px; }
.ai-tag { position:absolute; top:36px; right:44px; color:#aab6d0; font-size:26px;
  border:2px solid #3a4664; border-radius:10px; padding:8px 18px; z-index:10; }
.tachie { position:absolute; bottom:50px; right:80px; height:930px;
  filter: drop-shadow(0 22px 55px rgba(0,0,0,.65)); }
.tachi-sm { position:absolute; bottom:36px; right:150px; height:690px; opacity:.95; }
.tachi-dim { position:absolute; bottom:60px; right:200px; height:740px; opacity:.5; }
.tachi-mid { position:absolute; bottom:50px; right:170px; height:880px; }
.sticker { display:inline-block; background:#ffcd5a; color:#20160a; font-weight:900;
  padding:22px 56px; border-radius:18px; transform:rotate(-2deg);
  box-shadow: 0 10px 0 #c99e3f, 0 24px 48px rgba(0,0,0,.4); }
.card { background:rgba(22,30,52,.92); border:2px solid #33415f; border-radius:22px; }
"""


def tachi_img(name, cls="tachie", style=""):
    p = FRAMES / f"{name}.png"
    if not p.exists():
        return ""
    data = base64.b64encode(p.read_bytes()).decode()
    return f'<img class="{cls}" style="{style}" src="data:image/png;base64,{data}">'


def html_for(shot):
    """按 tpl 生成画面 HTML（title/proposal/bigtext/tachi/book/blank/rules/banner/endcard）。
    完整模板实现见 GLM娘 Day1 的 render.py，此处为核心骨架，按需扩展。"""
    ai = '<div class="ai-tag">本视频由 AI 生成内容</div>'
    badge = f'<div class="badge">{shot["badge"]}</div>' if shot.get("badge") else ""
    t = shot["tpl"]
    if t == "title":
        body = f'''<div style="position:absolute;left:120px;top:300px;width:1200px">
          {badge}<div style="height:34px"></div>
          <div style="font-size:84px;line-height:1.5;color:#f2f5fb;font-weight:700">{"<br>".join(shot['lines'])}</div></div>'''
    elif t == "tachi":
        body = f'''{tachi_img(shot.get('tachie',''), 'tachi-mid')}
        <div style="position:absolute;left:110px;top:250px;width:980px">{badge}
          <div style="font-size:78px;line-height:1.55;color:#f2f5fb;font-weight:700;margin-top:30px">{"<br>".join(shot['lines'])}</div></div>'''
    else:
        body = f'''<div style="position:absolute;inset:0;display:flex;align-items:center;
          justify-content:center"><div style="font-size:100px;font-weight:900;color:#ffcd5a">
          {"<br>".join(shot['lines'])}</div></div>'''
    orbs = "".join(f'<div class="orb" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px"></div>'
                   for x, y, s in [(220,160,90),(1660,240,60),(420,880,120),(1500,900,70)])
    return f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head><body><div class="stage">{orbs}{ai}{body}</div></body></html>'


def main():
    only = {int(x) for x in sys.argv[1:]} if len(sys.argv) > 1 else None
    kw = {"executable_path": EDGE} if EDGE else {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, **kw)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        for shot in SHOTS:
            if only and shot["id"] not in only:
                continue
            page.set_content(html_for(shot), wait_until="networkidle")
            out = FRAMES / f"shot{shot['id']:02d}.png"
            out.parent.mkdir(exist_ok=True)
            page.screenshot(path=str(out))
            print("rendered", out.name)
        browser.close()


if __name__ == "__main__":
    main()
