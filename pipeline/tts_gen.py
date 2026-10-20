# -*- coding: utf-8 -*-
"""tts_gen.py —— 按镜头表生成配音并测时长，输出 timing.json"""
import asyncio
import json
import subprocess
from pathlib import Path

import edge_tts

from shots import SHOTS, VOICE, RATE, PITCH

ROOT = Path(__file__).resolve().parent
AUDIO = ROOT / "audio"


def ff_path() -> str:
    r = subprocess.run(["python", "-c", "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"],
                       capture_output=True, text=True)
    return r.stdout.strip()


async def gen(shot):
    mp3 = AUDIO / f"shot{shot['id']:02d}.mp3"
    tts = edge_tts.Communicate(shot["text"], VOICE, rate=RATE, pitch=PITCH)
    await tts.save(str(mp3))
    return mp3


def dur(path, FF):
    r = subprocess.run([FF, "-i", str(path)], capture_output=True, text=True,
                       encoding="utf-8", errors="ignore")
    for line in r.stderr.splitlines():
        if "Duration" in line:
            t = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = t.split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    raise RuntimeError(f"no duration for {path}")


async def main():
    AUDIO.mkdir(exist_ok=True)
    FF = ff_path()
    timing = []
    for shot in SHOTS:
        mp3 = await gen(shot)
        d = dur(mp3, FF)
        pad = 0.9 if shot["tpl"] in ("banner", "bigtext") else 0.7
        timing.append(dict(id=shot["id"], audio=str(mp3), tts_dur=round(d, 2), dur=round(d + pad, 2)))
        print(f"shot{shot['id']:02d}  {d:5.2f}s -> {d+pad:5.2f}s")
    print(f"TOTAL: {sum(t['dur'] for t in timing):.1f}s")
    (ROOT / "timing.json").write_text(json.dumps(timing, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    asyncio.run(main())
