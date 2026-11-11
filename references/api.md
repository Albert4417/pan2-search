# pan2 站点 API 参考

默认站点：`https://www.pan2.cc.cd`。

## 搜索

`GET /api`

| 参数 | 说明 |
|---|---|
| `keyword` | 关键词，必填 |
| `page` | 页码，从 1 开始 |
| `page_size` | 每页条数，默认 10，上限 100；不传分页参数时 `limit` 默认 10 |
| `cloud_name` | 网盘筛选，如 `夸克网盘`、`115网盘`、`磁力链接` |
| `limit` | 兼容旧参数，不传 `page/page_size` 时生效 |

返回：

```json
{
  "success": true,
  "total": 196,
  "page": 1,
  "page_size": 10,
  "has_more": true,
  "results": [{
    "source": "database",
    "name": "三体 (2024) 4K",
    "cloud_name": "夸克网盘",
    "detail_url": "/detail?k=..."
  }]
}
```

- 数据库结果优先于外部聚合结果；数据库内 RSS 来源优先。
- 内部最多取 500 条。

## 详情入口

`GET /detail?k=<短码>`（兼容旧令牌时可能是 `t=<短码>`）

## 搜索建议

`GET /api/suggest?keyword=...` → `{"data": ["..."]}`

## 错误

| HTTP | 含义 |
|---|---|
| 400 | 参数错误、详情短码失效 |
| 403 | 公开搜索接口已关闭 |
| 429 | 请求过于频繁，响应头 `Retry-After` |
| 5xx | 站点或上游聚合异常 |

冷门关键词首次搜索可能耗时 30 秒以上；热门词有服务端缓存。搜索接口约 30 次/分钟/IP。
