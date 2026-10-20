# -*- coding: utf-8 -*-
"""compose.py —— 镜头图+音频 → 段视频 → concat → ASS 字幕 → 成片

关键点：
1. zoompan 前先 scale=7680（消除取整抖动）
2. 音频用 apad 补到目标时长（-shortest 会吃留白）
"""
import json
import subprocess
from pathlib import Path

from shots import SHOTS

ROOT = Path(__file__).resolve().parent
FF = subprocess.run(["python", "-c", "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"],
                    capture_output=True, text=True).stdout.strip()
timing = {t["id"]: t for t in json.loads((ROOT / "timing.json").read_text(encoding="utf-8"))}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    if r.returncode != 0:
        print(r.stderr[-1500:])
        raise SystemExit("ffmpeg failed")


for shot in SHOTS:
    tid = timing[shot["id"]]
    dur, pad = tid["dur"], round(tid["dur"] - tid["tts_dur"], 2)
    img = ROOT / "frames" / f"shot{shot['id']:02d}.png"
    out = ROOT / "clips" / f"c{shot['id']:02d}.mp4"
    out.parent.mkdir(exist_ok=True)
    zoom = (f"scale=7680:-1,zoompan=z='1+0.035*on/{int(dur*30)}':d={int(dur*30)}"
            f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30")
    fade = f"fade=t=in:st=0:d=0.18,fade=t=out:st={dur-0.15:.2f}:d=0.15"
    run([FF, "-y", "-loop", "1", "-i", str(img), "-i", str(tid["audio"]),
         "-filter_complex", f"[0:v]{zoom},format=yuv420p,{fade}[v];[1:a]apad=pad_dur={pad}[a]",
         "-map", "[v]", "-map", "[a]", "-t", f"{dur}",
         "-c:v", "libx264", "-preset", "medium", "-crf", "18",
         "-c:a", "aac", "-b:a", "160k", str(out)])
    print(f"clip {shot['id']:02d} ok ({dur}s)")

lst = ROOT / "clips" / "list.txt"
lst.write_text("".join(f"file 'c{s['id']:02d}.mp4'\n" for s in SHOTS), encoding="utf-8")
run([FF, "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(ROOT / "day1_raw.mp4")])


def sec(t):
    m, s = divmod(t, 60)
    h, m = divmod(int(m), 60)
    return f"{h}:{m:02d}:{s:05.2f}"


events, cursor = [], 0.0
for shot in SHOTS:
    d = timing[shot["id"]]["dur"]
    t0, t1 = cursor + 0.25, cursor + d - 0.25
    if t1 > t0:
        events.append(f"Dialogue: 0,{sec(t0)},{sec(t1)},glm,,0,0,0,,{shot['text']}")
    cursor += d
header = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\n\n"
          "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
          "BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
          "Style: glm,Microsoft YaHei,54,&H00FFFFFF,&H00FFFFFF,&H00101828,&H80000000,-1,1,3,1,2,60,60,44,1\n\n"
          "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
(ROOT / "day1.ass").write_text(header + "\n".join(events) + "\n", encoding="utf-8")

ass_escaped = str(ROOT / "day1.ass").replace("\\", "/").replace(":", "\\:")
run([FF, "-y", "-i", str(ROOT / "day1_raw.mp4"), "-vf", f"subtitles='{ass_escaped}'",
     "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-c:a", "copy",
     str(ROOT / "day1_final.mp4")])
print("FINAL:", ROOT / "day1_final.mp4")
