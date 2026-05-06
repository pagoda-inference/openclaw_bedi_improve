# 页面状态模板

使用此模板在 `states/` 目录中创建页面状态文件。

## 模板

```markdown
# 页面状态: {state-id}

> 状态ID: {state-id}
> 创建时间: {timestamp}
> 更新时间: {timestamp}

## 基本信息

- **URL**: {page-url}
- **标题**: {page-title}
- **Pattern**: {A/B/C/D/E}
- **状态**: {pending|analyzing|analyzed|failed}

## 页面快照

```
{opencli browser state 的输出}
```

## 导航入口

| 引用 | 文本 | 目标URL | 安全性 | 导航价值 |
|------|------|---------|--------|---------|
| [1] | {text} | {url} | ✅只读 | ⭐⭐⭐ |

## 网络请求

| key | 方法 | URL | shape 预览 | 安全性 |
|-----|------|-----|-----------|--------|
| r3 | GET | /api/products | data.items[].title | ✅只读 |

## 分析结果

**页面类型**: {listing|product|search|...}

**数据位置**: {API / 页面 / 需交互}

### API 端点

| 端点 | 认证方式 | 包含字段 |
|------|---------|---------|
| GET /api/products | COOKIE | title, price, id |

### 交互发现

| 交互 | 发现结果 | 安全性 |
|------|---------|--------|
| click [2] 展开筛选 | 显示更多筛选选项 | ✅ 只读 |

## 建议操作

1. ✅ **click** (只读 - 导航)
   - 命令: opencli browser click 1
   - 目的: {purpose}
   - 导航价值: ⭐⭐⭐

2. ❌ **click** (写入 - 禁止)
   - 目标: [5] 提交订单
   - 原因: 会产生交易

## 写入类入口（禁止操作）

| 元素 | 用途 | 原因 |
|------|------|------|
| [5] 提交订单 | 购买 | 会产生交易 |

## 备注

- {timestamp}: {note}
```

## 使用方法

1. 复制模板到 `states/state-{id}.md`
2. 用实际值替换占位符
3. 页面快照直接粘贴 `opencli browser state` 输出
4. 网络请求直接粘贴 `opencli browser network` 输出
5. 使用 FileOps 按需更新各部分
