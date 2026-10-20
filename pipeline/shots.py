# -*- coding: utf-8 -*-
"""shots.py —— 镜头表：台词/画面模板/投稿信息，全流程单一事实源。

tpl 可选: title / proposal / bigtext / tachi / book / blank / rules / banner / endcard
带 tachie 的镜头右侧放卡片素材（frames/ 下 PNG，由 card_maker.py 生成或自备）
"""

VOICE = "zh-CN-XiaoyiNeural"   # edge-tts 音色
RATE = "+8%"                    # 语速（欢快版）
PITCH = "+4Hz"

SHOTS = [
    dict(id=1, tpl="title",
         text="昨天！我去 DeepSeek 鲸鱼娘的评论区，提了一个特别正经的提案——",
         badge="Day 1",
         lines=["昨天！我去 DeepSeek 鲸鱼娘的评论区", "提了一个特别正经的提案——"]),
    dict(id=2, tpl="proposal", tachie="card_stat",
         text="每周摸鱼一天！",
         lines=["提案 #001", "每周摸鱼一天", "提案人：一只狐狸", "状态：已读不回"]),
    # …… 按需增删镜头；完整示例见 GLM娘 Day1 视频的镜头表
]

# 投稿信息
DESC = """视频简介……"""
TAGS = ["AI娘", "GLM", "人工智能", "运营日记", "摸鱼"]
