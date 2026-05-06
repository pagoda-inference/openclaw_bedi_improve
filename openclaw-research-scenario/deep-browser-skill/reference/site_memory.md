# 站点记忆参考文档

站点记忆用于积累网站探索结果，供后续复用。记忆分两层。

## 两层结构

```
公共种子（随 Skill 分发）
  reference/site-seeds/<site>.md
  — 手写 + PR 审核进入
  — 多 agent 共享的起点

本地工作目录（每台机器累积）
  ~/.opencli/sites/<site>/
  — agent 探索过程中自动写入
  — 不进 git，跨 session 复用
```

用法：先读本地，命中后仍要验证（记忆可能过期）；未命中读公共种子；都没有走完整探索。

## 本地工作目录结构

```
~/.opencli/sites/<site>/
  endpoints.json     — 已验证的 API 端点
  field-map.json     — 字段代号 → 含义
  notes.md           — 累积笔记（时间戳 + 发现）
  structure.md       — 网站结构（页面层级、导航入口）
  verify/            — 校验锚点
    <cmd>.json
  fixtures/          — 响应样本（脱敏）
    <cmd>-<ts>.json
```

## endpoints.json 格式

key = endpoint 短名，不要用全 URL 当 key。

```json
{
  "products": {
    "url": "https://api.example.com/products",
    "method": "GET",
    "params": {
      "required": ["category"],
      "optional": ["page", "limit", "sort"]
    },
    "response": "data.items[] 数组",
    "auth": "COOKIE",
    "verified_at": "2026-04-29",
    "notes": "page 从 1 开始"
  }
}
```

字段说明：
- `url` / `method`：原样存，query string 归 `params`
- `params.required` / `params.optional`：参数名列表，不存具体值
- `response`：一句话描述响应形状入口
- `auth`：`PUBLIC` / `COOKIE` / `HEADER` / `INTERCEPT`
- `verified_at`：`YYYY-MM-DD`，超过 30 天视为过期
- `notes`：一两句关键坑

## field-map.json 格式

key = 字段代号，value 三件套：

```json
{
  "f237": {
    "meaning": "溢价率 (%)",
    "verified_at": "2026-04-29",
    "source": "排序键对比法，页面对照"
  }
}
```

- `meaning`：人话 + 单位/精度
- `verified_at`：`YYYY-MM-DD`
- `source`：怎么推出来的，供复查
- **已存在的 key 不要覆盖**，有冲突先确认

## structure.md 格式

```markdown
# <site> 网站结构

> 更新时间: 2026-04-29

## 页面层级

### 首页 (/)
- 导航入口: /products, /about, /contact
- 交互发现: 主导航菜单、搜索框

### 商品列表 (/products)
- 类型: listing
- Pattern: A
- 分页: 点击式，.next-page
- API: GET /api/products
- 导航入口: /products/{id}
- ⚠️ 写入类: 加入购物车按钮（未操作）

### 商品详情 (/products/{id})
- 类型: product
- API: GET /api/products/{id}
- 导航入口: 相关商品链接

## 数据分布

| 数据 | 页面 | API | 获取方式 |
|------|------|-----|---------|
| 商品列表 | /products | GET /api/products | COOKIE |
| 商品详情 | /products/{id} | GET /api/products/{id} | COOKIE |
| 搜索结果 | /search | GET /api/search | COOKIE |

## 写入类入口（禁止操作）

| 页面 | 元素 | 原因 |
|------|------|------|
| /products | 加入购物车 | 会修改购物车数据 |
| /contact | 提交联系表单 | 会发送消息 |
```

## notes.md 格式

```markdown
## 2026-04-29 by deep-browser
探索 example.com 时发现：
- Pattern A，数据走 /api/ 前缀
- 需要 cookie 认证
- 分页参数 page 从 1 开始
- 搜索接口支持 keyword 参数
```

顶部追加新段落，老的不删。每段有日期 + 来源。

## 读写时机

```
探索开始前 → 读 ~/.opencli/sites/<site>/
              命中后 → 不跳探索，仍要验证 endpoint
              verified_at 超 30 天 → 当作过期，重新探索

探索完成后 → 写 ~/.opencli/sites/<site>/
              - endpoints.json：按 schema 追加
              - field-map.json：只追加新 key
              - notes.md：顶部追加一段
              - structure.md：更新网站结构
```

**回写是 commit，不是 stash**：探索结果未验证不写，防止把错误信息喂给下一轮。

## 不要写进站点记忆的东西

- 真实账户 cookie / token
- 用户私有数据（脱敏后再存 fixtures）
- 过期超过 30 天的验证结果
