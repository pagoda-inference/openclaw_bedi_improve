# 浏览器操作参考文档

本文档提供 OpenCLI browser 命令的详细说明，帮助智能体正确操作浏览器。

## 核心原则

1. **先检查再操作** — 每次操作前获取 state，操作后重新获取
2. **链式调用** — 用 `&&` 连接命令，保持会话上下文
3. **只读约束** — 只执行导航/展示/搜索类操作，禁止写入
4. **network 优先** — API 数据比 DOM 抓取更可靠

## 环境检查

```bash
# 检查 OpenCLI 环境
opencli doctor

# 检查 OpenCLI 是否可用
which opencli
```

## 站点分析

```bash
# 一步完成站点分类 + 反爬检测 + 建议下一步
opencli browser analyze <url>
```

返回 Pattern 分类（A/B/C/D/E）、反爬检测结果、SSR 全局变量、最近适配器匹配。

## 页面操作

### 打开页面

```bash
opencli browser open "https://example.com"
```

### 获取页面快照

```bash
opencli browser state
```

返回文本树，带 `[N]` 数字引用。每个交互元素标注 ref，后续操作用 ref 定位。

快照包含：
- `[N]` 元素引用（用于 click/type/select）
- `compounds (N):` sidecar（日期/选择/文件控件的结构化信息）
- 滚动提示
- 隐藏交互元素提示

### 查找元素

```bash
opencli browser find --css "button.submit" --limit 5
```

返回匹配元素的 `{nth, ref, tag, role, text, attrs, visible, compound?}`。

### 点击

```bash
opencli browser click 3
```

返回 `{clicked, target, matches_n, match_level}`。

### 输入文本

```bash
opencli browser type 5 "搜索关键词"
```

返回 `{typed, text, target, matches_n, match_level, autocomplete}`。

`autocomplete: true` 表示出现了自动补全弹窗，需要 `keys Enter` 或点击建议项。

### 选择下拉选项

```bash
opencli browser select 12 "选项文本"
```

### 按键

```bash
opencli browser keys Enter
opencli browser keys Escape
opencli browser keys "Control+a"
```

### 滚动

```bash
opencli browser scroll down
opencli browser scroll down --amount 500
opencli browser scroll up
```

## 数据获取

### 获取页面信息

```bash
opencli browser get title
opencli browser get url
```

### 获取元素数据

```bash
opencli browser get text 3
opencli browser get value 5
opencli browser get attributes 3
```

返回 `{value, matches_n, match_level}`。

### 提取页面内容

```bash
opencli browser extract --chunk-size 8000
```

返回 `{url, title, content, total_chars, next_start_char}`。循环 `next_start_char` 直到 `null`。

### 获取 HTML

```bash
opencli browser get html --selector ".content" --as json --depth 3 --children-max 20
```

注意：HTML 输出可能很大，务必加 `--selector` 和预算参数。

## 网络分析

### 列出网络请求

```bash
opencli browser network
```

返回每个请求的 `{key, method, status, url, ct, size, shape}`。

- `key`：稳定引用（用于 `--detail`）
- `shape`：响应体的路径→类型映射（不含原 body，省 token）
- 默认过滤静态资源/埋点/追踪

### 按字段过滤

```bash
opencli browser network --filter "title,price,author"
```

AND 语义：必须每个字段都作为 shape 路径出现才保留。

### 获取完整响应

```bash
opencli browser network --detail <key>
```

### 包含所有请求

```bash
opencli browser network --all
```

## 等待

```bash
# 等待元素出现
opencli browser wait selector ".content" --timeout 10000

# 等待文本出现
opencli browser wait text "搜索结果" --timeout 10000

# 硬等待（最后手段）
opencli browser wait time 3
```

默认超时 10000ms。SPA 路由、登录跳转、懒加载列表需要 wait。

## 标签页管理

```bash
opencli browser tab list          # 列出标签页
opencli browser tab new [url]     # 新建标签页
opencli browser tab select [id]   # 切换标签页
opencli browser tab close [id]    # 关闭标签页
opencli browser close             # 释放当前自动化标签页
```

## match_level 容错

| level | 含义 | 处理 |
|-------|------|------|
| `exact` | 完全匹配 | 直接继续 |
| `stable` | 软属性漂移 | 操作仍有效，建议验证 |
| `reidentified` | 原引用消失，找到替代 | 需要二次确认 |

## Compound 表单控件

state 快照的 `compounds` sidecar 提供结构化信息：

**日期控件**：
```json
{ "control": "date", "format": "YYYY-MM-DD", "current": "2026-04-29" }
```

**选择控件**：
```json
{ "control": "select", "options": [{ "label": "选项1", "value": "1" }], "options_total": 50 }
```

**文件控件**：
```json
{ "control": "file", "accept": "image/*", "multiple": false }
```

不要用正则猜测格式，直接用 compound 信息。

## 结构化错误码

| code | 含义 | 处理 |
|------|------|------|
| `not_found` | 数字引用不在 DOM 中 | 重新 state |
| `stale_ref` | 引用存在但元素已变化 | 重新 state |
| `selector_not_found` | CSS 匹配 0 元素 | 换选择器 |
| `selector_ambiguous` | CSS 匹配多个元素 | 加 `--nth` |

## 常见模式

### 探索新页面

```bash
opencli browser open "https://example.com" \
  && opencli browser state \
  && opencli browser network
```

### 交互后重新获取

```bash
opencli browser click 3 \
  && opencli browser wait selector ".content" \
  && opencli browser state
```

### 搜索

```bash
opencli browser type 5 "关键词" \
  && opencli browser keys Enter \
  && opencli browser wait text "结果" \
  && opencli browser state \
  && opencli browser network
```

### 分页遍历

```bash
opencli browser click 8 \
  && opencli browser wait time 2 \
  && opencli browser state
```

### API 发现

```bash
opencli browser network \
  && opencli browser network --filter "title,price" \
  && opencli browser network --detail <key>
```

## 降级方案

当 OpenCLI 不可用时，使用 OpenClaw browser tool：

| OpenCLI | OpenClaw browser tool |
|---------|----------------------|
| `opencli browser open <url>` | `action="open"` |
| `opencli browser state` | `action="snapshot"` |
| `opencli browser click <ref>` | `action="act", kind="click"` |
| `opencli browser type <ref> <text>` | `action="act", kind="type"` |
| `opencli browser network` | `action="snapshot"` + 观察 |

OpenClaw browser tool 无 network 分析和 analyze 功能，能力受限。

## 注意事项

- 不要跨页面复用 ref — 导航后必须重新 state
- 不要用 `eval` 执行写入操作 — 用结构化 click/type/select
- 截图消耗大量 token — 优先用 state
- `network` 默认过滤静态资源 — 缺失时用 `--all`
- `type` 后检查 `autocomplete` — 可能需要额外操作
