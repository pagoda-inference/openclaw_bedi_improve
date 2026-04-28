# 市场调研能力扩展

## 概述

本文件定义了 OpenClaw 的市场调研能力，包括任务管理、深度浏览器、数据处理和报告生成。

## 核心工具

### task_manager

任务管理工具，支持创建、查询、更新、恢复市场调研任务。

**操作类型**：
- `create`: 创建新任务，生成任务目录结构
- `get`: 获取任务详情
- `update`: 更新任务状态和数据
- `list`: 列出所有任务
- `recover`: 恢复未完成的任务

**任务状态流转**：
```
pending → planning_completed → collection_completed → processing_completed → completed
```

### deep_browser

深度浏览器工具，基于 OpenCLI 实现网站系统的深度理解、浏览规划和记忆积累。

**七大能力**：

#### 1. understand（深度理解）

分析网站系统结构：

```json
{
  "action": "understand",
  "url": "https://example.com"
}
```

返回：
- `page_type`: 页面类型（listing/product/search/login/form/content）
- `layout_pattern`: 布局模式（three-column/two-column/single-column/fluid）
- `interactive_elements`: 可交互元素列表（带 ref 引用）
- `data_regions`: 数据区域（main/article/aside/table/list）
- `pagination`: 分页机制（click/scroll/load-more）
- `form_purposes`: 表单用途识别
- `network_summary`: API 端点摘要
- `cached_pattern`: 已缓存的网站模式（如有）

#### 2. operate（执行操作）

执行浏览器操作：

```json
{
  "action": "operate",
  "target": 3,           // ref 数字或 CSS 选择器
  "text": "搜索内容",     // type 操作时
  "option": "选项值",     // select 操作时
  "direction": "down",   // scroll 操作时
  "key": "Enter"         // keys 操作时
}
```

支持的操作：
- `click`: 点击元素
- `type`: 输入文本
- `select`: 选择选项
- `scroll`: 滚动页面
- `keys`: 按键操作

#### 3. observe（观察变化）

观察页面状态：

```json
{
  "action": "observe",
  "save_to": "/path/to/screenshot.png"
}
```

返回：
- `url`: 当前 URL
- `title`: 页面标题
- `element_count`: 元素数量
- `interactive_count`: 可交互元素数量
- `scroll_position`: 滚动位置
- `has_more_below`: 是否有更多内容
- `screenshot`: 截图路径

#### 4. remember（记忆积累）

保存网站模式到本地：

```json
{
  "action": "remember",
  "site_pattern_id": "ecommerce-amazon",
  "selector": "product_card=.product-item"
}
```

保存内容：
- 页面类型和指示器
- 数据区域选择器
- 分页机制
- 导航流程
- 数据端点

#### 5. collect（内容采集）

提取页面内容：

```json
{
  "action": "collect",
  "url": "https://example.com",
  "selector": "article",
  "save_to": "/path/to/data.json"
}
```

#### 6. plan（浏览规划）

生成多步骤浏览计划：

```json
{
  "action": "plan",
  "task_context": {
    "task_id": "task-20240101-abc123",
    "sub_topic": "市场规模",
    "depth": 0,
    "max_depth": 3
  }
}
```

返回：
- `plan`: 完整浏览计划
- `suggested_next_step`: 建议的下一步
- `progress`: 进度统计

#### 7. network（网络捕获）

捕获 API 请求：

```json
{
  "action": "network",
  "filter": "data,items",
  "key": "entry-001"  // 获取特定请求详情
}
```

返回：
- `api_endpoints`: API 端点列表
- `data_hints`: 数据结构提示

## 记忆系统

### 网站模式记忆

存储位置：`~/.openclaw/deep-browser/patterns/`

```json
{
  "id": "ecommerce-amazon",
  "domain": "amazon.com",
  "page_types": {
    "listing": {
      "type": "listing",
      "indicators": ["products", "results"],
      "data_regions": [
        { "selector": ".s-result-list", "type": "product-list" }
      ],
      "pagination": { "type": "click", "selector": ".s-pagination-next" }
    },
    "product": {
      "type": "product",
      "indicators": ["price", "buy"],
      "data_regions": [
        { "selector": "#productTitle", "type": "title" },
        { "selector": ".a-price", "type": "price" }
      ]
    }
  },
  "navigation_flows": [
    {
      "name": "search-to-product",
      "steps": [
        { "action": "type", "target": "#twotabsearchtextbox", "expected_change": "search input filled" },
        { "action": "click", "target": "#nav-search-submit-button", "expected_change": "search results loaded" }
      ],
      "purpose": "搜索商品"
    }
  ],
  "data_endpoints": [
    {
      "url_pattern": "/api/product/*",
      "method": "GET",
      "shape": "{product: {id, title, price}}",
      "purpose": "商品详情"
    }
  ],
  "selectors": {
    "search_input": "#twotabsearchtextbox",
    "product_card": ".s-result-item"
  },
  "success_count": 15,
  "failure_count": 2
}
```

### 浏览计划记忆

存储位置：`~/.openclaw/deep-browser/plans/`

```json
{
  "goal": "采集 AI Agent 市场规模数据",
  "current_depth": 1,
  "max_depth": 3,
  "steps": [
    {
      "id": "step-1",
      "description": "Collect current page items",
      "action": "collect",
      "params": { "selector": "main" },
      "dependencies": [],
      "status": "completed",
      "retry_count": 0,
      "expected_outcome": "Items collected from current page"
    },
    {
      "id": "step-2",
      "description": "Navigate to next page via click",
      "action": "operate",
      "params": { "target": "[5]", "operation_type": "click" },
      "dependencies": ["step-1"],
      "status": "in_progress",
      "retry_count": 0,
      "expected_outcome": "Next page loaded"
    }
  ],
  "completed_steps": ["step-1"],
  "current_step": "step-2",
  "collected_data": [
    { "step": "step-1", "data": { "items": [...] } }
  ]
}
```

## 使用指南

### 深度浏览流程

1. **理解页面**
```
deep_browser action: "understand", url: "目标 URL"
→ 返回页面分析 + 缓存模式（如有）
```

2. **检查记忆**
```
如果返回 source: "memory"，直接使用缓存的 selectors
如果返回 source: "analysis"，继续探索
```

3. **规划浏览**
```
deep_browser action: "plan", task_context: { ... }
→ 生成多步骤浏览计划
```

4. **执行步骤**
```
按计划执行：
- operate: 执行操作
- observe: 观察变化
- collect: 采集数据
- network: 捕获 API
```

5. **积累记忆**
```
deep_browser action: "remember", site_pattern_id: "..."
→ 保存网站模式供下次使用
```

### 多层深度采集

对于需要多次交互才能获取深层数据的场景：

```
depth=0: 首页/列表页
  ↓ operate (点击/搜索)
depth=1: 详情页/搜索结果
  ↓ operate (筛选/翻页)
depth=2: 深层详情/更多数据
  ↓
...
max_depth: 达到最大深度停止
```

### API 优先策略

优先使用 API 而非 DOM 抓取：

```
1. understand → network_summary
2. network → api_endpoints
3. 如果有合适的 API，直接调用
4. 否则使用 DOM 抓取
```

## 任务目录结构

```
~/.openclaw/tasks/{task-id}/
├── task.json              # 任务元信息 + 状态
├── config.json            # 任务配置
├── plan.json              # 调研计划
├── data/
│   ├── raw/               # 原始数据
│   ├── processed/         # 处理后数据
│   └── analysis/          # 分析结果
├── memory/
│   ├── operations.json    # 操作历史
│   └── visited.json       # 已访问 URL
├── output/
│   └── report.html        # 最终报告
└── logs/
    └── task.log
```

## 注意事项

1. **Selector-first 原则**：优先使用 `state` 返回的 ref 数字，比 CSS 选择器更稳定
2. **记忆优先**：先检查缓存模式，避免重复分析
3. **API 优先**：优先捕获和使用 API 端点，比 DOM 抓取更可靠
4. **深度控制**：设置合理的 max_depth，避免无限递归
5. **错误恢复**：每个步骤都有 retry 机制，失败后可从断点恢复
