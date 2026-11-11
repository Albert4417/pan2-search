# Pan2 Search

> 一个技能，搜遍全网网盘与 Telegram 影视资源频道。

夸克、百度、阿里云盘、UC、115、迅雷、天翼、移动、123、磁力……一次搜索，多源聚合，去重合并后只给你最值得看的 10 条。

## 为什么用它

- **多引擎聚合**：不是只查一家。多个公开网盘搜索源并发查询，结果按分享身份去重，减少重复和噪音。
- **TG 影视频道加持**：后台持续收录 Telegram 影视资源频道，新片、热剧、动漫、综艺更新更快。
- **默认 10 条**：不堆列表，不让你在几百条结果里翻找；需要更多再加 `--limit`。
- **站内详情入口**：每条结果都有对应的资源详情页，点开即可查看资源信息。
- **本地缓存**：10 分钟内重复搜索直接命中缓存，冷门词也不用反复等。
- **不碰账号**：不需要登录，不保存 Cookie、Token 或任何网盘凭据。

## 适合这些场景

```text
帮我找三体的 4K 资源
搜一下庆余年，只要夸克网盘
有没有 2026 年新剧的网盘资源
找一部适合周末看的科幻电影
```

## 安装

作为 Claude Code 技能使用：

```bash
git clone https://github.com/<your-name>/pan2-search.git ~/.claude/skills/pan2-search
python3 -m pip install requests
```

或者把整个目录复制到 `~/.claude/skills/pan2-search`。

## 使用

```bash
# 默认返回 10 条
python3 ~/.claude/skills/pan2-search/scripts/pan2_search.py "三体"

# 返回 20 条
python3 ~/.claude/skills/pan2-search/scripts/pan2_search.py "三体" --limit 20

# 只看夸克网盘
python3 ~/.claude/skills/pan2-search/scripts/pan2_search.py "庆余年" --cloud 夸克网盘

# 结构化输出
python3 ~/.claude/skills/pan2-search/scripts/pan2_search.py "三体" --json
```

输出示例：

```text
「三体」共 196 条，展示 10 条：
1. 三体 (2024) 4K — 夸克网盘
   详情：https://www.pan2.cc.cd/detail?k=...
2. 三体 · 周年纪念版 (2023) 1080P — 百度网盘
   详情：https://www.pan2.cc.cd/detail?k=...
```

## 支持的网盘

夸克、百度、阿里云盘、UC、115、迅雷、天翼、移动、联通、123、PikPak、蓝奏、微云、城通，以及磁力、电驴等链接类型；实际以站点返回结果为准。

## 工作方式

`pan2_search.py` 调用站点公开搜索接口，按关键词、页码和网盘类型取回聚合结果；默认 10 条，支持本地缓存。结果只包含标题、网盘类型和站内详情入口。

## 注意

- 资源来自互联网公开分享，仅供学习交流，请遵守版权和当地法律。
- 公开接口可能限流或临时关闭，遇到 403/429 时稍后重试。
- 本项目只做搜索聚合，不存储文件，也不提供下载服务。
- 与任何网盘平台无隶属关系。

## License

MIT
