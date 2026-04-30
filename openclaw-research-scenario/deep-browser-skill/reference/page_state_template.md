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
- **状态**: {pending|analyzing|analyzed|failed}

## 页面元素

| 引用 | 标签 | 文本 | 可见 | 角色 |
|------|------|------|------|------|
| 1 | {tag} | {text} | {✓|✗} | {role} |
| 2 | ... | ... | ... | ... |

## 分析结果

**页面类型**: {page-type} (置信度: {confidence})

**布局模式**: {layout-pattern}

### 数据区域

- `{selector}`: {description}

### 分页机制

- 类型: {pagination-type}
- 选择器: `{selector}`
- 描述: {description}

### 内容摘要

- 主题: {main-topic}
- 语言: {language}
- 实体: {entity-list}

## 建议操作

1. {优先级图标} **{操作类型}**
   - 目标: `{selector}`
   - 目的: {purpose}
   - 优先级: {high|medium|low}

## 网络请求

总计: {count} 个请求

| 方法 | URL | 类型 |
|------|-----|------|
| {method} | {url} | {content-type} |

## 备注

- {timestamp}: {note-content}
```

## 使用方法

1. 复制模板到 `states/state-{id}.md`
2. 用实际值替换占位符
3. 使用FileOps按需更新各部分

## 示例

```markdown
# 页面状态: state-001

> 状态ID: state-001
> 创建时间: 2026-04-28T10:00:00Z
> 更新时间: 2026-04-28T10:30:00Z

## 基本信息

- **URL**: https://example.com/products
- **标题**: 商品列表
- **状态**: analyzed

## 页面元素

| 引用 | 标签 | 文本 | 可见 | 角色 |
|------|------|------|------|------|
| 1 | button | 搜索 | ✓ | button |
| 2 | input | | ✓ | textbox |

## 分析结果

**页面类型**: listing (置信度: 0.95)

**布局模式**: two-column

### 数据区域

- `.product-grid`: 主商品列表

### 分页机制

- 类型: click
- 选择器: `.next-page`
- 描述: 点击加载下一页

## 建议操作

1. 🔴 **click**
   - 目标: `.search-button`
   - 目的: 提交搜索查询
   - 优先级: high

## 网络请求

总计: 15 个请求

| 方法 | URL | 类型 |
|------|-----|------|
| GET | /api/products | application/json |

## 备注

- 10:00:05: 初始页面加载成功
- 10:00:10: 第一页发现50个商品
```
