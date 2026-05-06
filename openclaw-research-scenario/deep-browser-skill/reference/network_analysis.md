# 网络分析参考文档

本文档提供网络请求分析方法论，帮助发现 API 端点、识别数据源、推断响应结构。

## 分析目标

1. **API 端点** — 哪些 URL 返回目标数据
2. **响应结构** — shape 推断（路径→类型映射）
3. **认证方式** — PUBLIC / COOKIE / HEADER / INTERCEPT
4. **安全性** — 读取 API vs 写入 API

## 核心命令

```bash
# 列出网络请求（带 shape 预览）
opencli browser network

# 按字段过滤（AND 语义）
opencli browser network --filter "title,price,author"

# 获取完整响应体
opencli browser network --detail <key>

# 包含所有请求（含静态资源）
opencli browser network --all
```

## 输出结构

`opencli browser network` 返回每个请求的：

```json
{
  "key": "r3",
  "method": "GET",
  "status": 200,
  "url": "https://api.example.com/products?page=1",
  "ct": "application/json",
  "size": 15234,
  "shape": {
    "data.items[].id": "number",
    "data.items[].title": "string",
    "data.items[].price": "number",
    "data.total": "number",
    "data.page": "number"
  }
}
```

- `key`：稳定引用，用于 `--detail <key>`
- `shape`：响应体的路径→类型映射（不含原 body，省 token）
- 默认过滤静态资源/埋点/追踪请求

## API 发现流程

```
1. opencli browser network
   └─ 获取所有请求的 shape 预览

2. opencli browser network --filter "目标字段"
   └─ 精确过滤包含目标字段的请求

3. opencli browser network --detail <key>
   └─ 拉完整响应体，确认数据结构

4. 验证 endpoint
   └─ 确认是否可直接 fetch（不需要浏览器上下文）
```

## 认证方式分类

| 方式 | 特征 | 可复用性 |
|------|------|---------|
| PUBLIC | 无认证 | ✅ 可直接 fetch |
| COOKIE | 依赖浏览器 cookie | ⚠️ 需浏览器上下文 |
| HEADER | 需要 CSRF token / Bearer | ⚠️ 需浏览器上下文 |
| INTERCEPT | 必须在浏览器内拦截 | ❌ 无法独立调用 |

**判断方法**：
- PUBLIC：请求头无自定义字段，无 cookie 也能访问
- COOKIE：请求依赖 cookie（登录态）
- HEADER：请求头有 `X-CSRF-Token` / `Authorization: Bearer` 等
- INTERCEPT：数据只在浏览器上下文中可用

## Shape 推断

`opencli browser network` 的 `shape` 字段自动推断响应结构：

```json
{
  "data.items[].id": "number",
  "data.items[].title": "string",
  "data.items[].price": "number",
  "data.items[].tags[]": "string",
  "data.total": "number",
  "data.page": "number"
}
```

**用途**：
- 快速判断响应是否包含目标字段
- 不需要拉完整 body 就能了解数据结构
- `--filter` 基于 shape 过滤

## API 安全性分类

### 只读 API（允许验证和调用）

| 类型 | HTTP 方法 | 特征 |
|------|----------|------|
| 数据获取 | GET | 获取展示数据 |
| 搜索 | GET/POST | 获取搜索结果 |
| 列表查询 | GET | 获取列表数据 |

### 写入 API（禁止调用）

| 类型 | HTTP 方法 | 特征 |
|------|----------|------|
| 创建数据 | POST | 创建新资源 |
| 更新数据 | PUT/PATCH | 修改已有资源 |
| 删除数据 | DELETE | 删除资源 |
| 认证操作 | POST | 登录/注册 |
| 提交操作 | POST | 提交表单 |

**注意**：同样是 POST，搜索类（如 `POST /api/search`）是只读，创建类（如 `POST /api/products`）是写入。根据业务上下文判断。

## 写入站点记忆

发现的 API 端点应写入 `~/.opencli/sites/<site>/endpoints.json`：

```json
{
  "products": {
    "url": "https://api.example.com/products",
    "method": "GET",
    "params": {
      "required": [],
      "optional": ["page", "limit", "category"]
    },
    "response": "data.items[] 数组",
    "auth": "COOKIE",
    "verified_at": "2026-04-29",
    "notes": "page 从 1 开始"
  }
}
```

详见 [站点记忆参考](site_memory.md)。

## 相关参考

- [站点侦察](site_recon.md) — Pattern 分类和 API 发现策略
- [浏览器操作参考](browser_operations_reference.md) — network 命令详解
- [站点记忆](site_memory.md) — 记忆格式
