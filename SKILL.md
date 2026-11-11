---
name: pan2-search
display_name: pan2 资源搜索
display_name_en: Pan2 Resource Search
description: 搜索 pan2 资源站（默认 https://www.pan2.cc.cd）的多网盘资源，聚合夸克、百度、阿里、UC、115、迅雷、天翼、123、磁力等来源，并融合 Telegram 影视资源频道；默认返回 10 条结果与资源详情入口。触发词：搜资源、找资源、网盘搜索、pan2、pan2.cc.cd、夸克/百度/UC/115/磁力资源、资源详情。
description_zh: "找电影、追剧、搜动漫、查资料，不用再挨个网站翻找。Pan2 汇聚多个网盘搜索引擎与资源分享频道，持续收录更新资源，一次搜索，多源查找。覆盖夸克、百度、阿里云盘、UC、115、迅雷、天翼、123 等主流网盘及磁力资源，兼顾新片热剧与经典资源。说出想找的资源名，即可获取搜索结果；支持按网盘筛选，点击查看资源详情，让找资源更省时、省心。"
description_en: "Find movies, follow series, search anime, or look up materials without checking site after site. Pan2 brings together multiple cloud-drive search engines and resource-sharing channels, continuously indexing and updating resources—one search, multiple sources. It covers Quark, Baidu, Aliyun Drive, UC, 115, Xunlei, Tianyi, 123 and other major cloud drives plus magnet links, balancing new releases with classics. Just name what you need to get search results; filter by cloud drive and open resource details for a faster, easier search."
version: 1.2.6
examples_zh:
- "帮我搜三体的网盘资源"
- "找一下 2026 新剧，只要夸克网盘"
- "有没有适合周末看的科幻电影"
examples_en:
- "Find netdisk resources for Three-Body"
- "Search 2026 new TV series on Quark only"
- "Find a sci-fi movie for the weekend"
agent_created: true
author: Claude
---

# pan2 资源搜索

搜索站点公开 API，返回资源结果与详情入口。

## 快速开始

```bash
# 搜索，默认 10 条
python3 ~/.claude/skills/pan2-search/scripts/pan2_search.py "三体"

# 指定条数与网盘
python3 ~/.claude/skills/pan2-search/scripts/pan2_search.py "三体" --limit 20 --cloud 夸克网盘
```

依赖：Python 3.9+、`requests`。站点地址可用环境变量覆盖：`PAN2_BASE_URL`。缓存目录：`PAN2_CACHE_DIR`（默认 `~/.cache/pan2-search`）。

## 工作流

1. **搜索**：提取用户关键词，运行 `pan2_search.py`，默认 `--limit 10`。
2. **展示**：按“标题 — 网盘 / 详情入口”列出；入口必须是完整可点击的站点 URL。
3. **引导**：用户需要资源时，给出对应详情入口。

## 输出格式

```
「三体」共 196 条，展示 10 条：
1. 三体 (2024) 4K — 夸克网盘
   详情：https://www.pan2.cc.cd/detail?k=...
```

## 关键约束

- 以站点返回的详情入口为准，不要自行拼接资源地址。
- 详情入口短码有时效；用户点开报错时，重新搜索拿新入口。
- 公开搜索接口可能被管理员关闭，此时返回 403，直接告知用户。
- 搜索冷门词首次聚合可能 30 秒以上；脚本缓存 10 分钟，重复搜索会快很多。
- 搜索接口约 30 次/分钟/IP，不要并发调用。

## 资源

- `scripts/pan2_search.py` — 搜索，默认 10 条，支持分页、网盘筛选、JSON、缓存。
- `references/api.md` — 搜索接口、参数、返回结构、限流与错误码。
