# Pan2 Search

找电影、追剧、搜动漫、查资料，不用再挨个网站翻找。Pan2 汇聚多个网盘搜索引擎与资源分享频道，持续收录更新资源，一次搜索，多源查找。覆盖夸克、百度、阿里云盘、UC、115、迅雷、天翼、123 等主流网盘及磁力资源，兼顾新片热剧与经典资源。说出想找的资源名，即可获取搜索结果；支持按网盘筛选，点击查看资源详情，让找资源更省时、省心。

## 为什么用它

- **多引擎聚合**：不是只查一家。多个公开网盘搜索源并发查询，结果按分享身份去重，减少重复和噪音。
- **TG 影视频道加持**：后台持续收录 Telegram 影视资源频道，新片、热剧、动漫、综艺更新更快。
- **默认 10 条**：不堆列表，不让你在几百条结果里翻找；需要更多再加 `--limit`。
- **站内详情入口**：每条结果都有对应的资源详情页，点开即可查看资源信息。
- **本地缓存**：10 分钟内重复搜索直接命中缓存，冷门词也不用反复等。
- **不碰账号**：不需要登录，不保存账号凭据或 Cookie。

## 适合这些场景

```text
帮我找一份 Python 入门教程
搜一下免费的 PPT 模板
有没有适合新手的 Excel 学习资料
找一套开源项目的学习文档
```

## 安装

作为 Claude Code 技能使用：

```bash
git clone https://github.com/Albert4417/pan2-search.git ~/.claude/skills/pan2-search
python3 -m pip install requests
```

或者把整个目录复制到 `~/.claude/skills/pan2-search`。

## 使用

```bash
# 默认返回 10 条
python3 ~/.claude/skills/pan2-search/scripts/pan2_search.py "Python 入门教程"

# 返回 20 条
python3 ~/.claude/skills/pan2-search/scripts/pan2_search.py "Python 入门教程" --limit 20

# 只看夸克网盘
python3 ~/.claude/skills/pan2-search/scripts/pan2_search.py "PPT 模板" --cloud 夸克网盘

# 结构化输出
python3 ~/.claude/skills/pan2-search/scripts/pan2_search.py "Python 入门教程" --json
```

输出示例：

```text
「Python 入门教程」共 196 条，展示 10 条：
1. Python 入门教程（2026 版）— 夸克网盘
   详情：https://www.pan2.cc.cd/detail?k=...
2. Excel 函数与数据透视表教程 — 百度网盘
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
