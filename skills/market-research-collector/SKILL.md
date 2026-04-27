---
name: market-research-collector
description: "市场调研数据采集，通过 Deep Browser 收集网页内容"
trigger: 当 task_manager 状态为 "planning_completed" 时激活
---

# 数据采集 Skill

## 工作流程

### Step 1: 读取调研计划
读取 plan.json 获取需要采集的子主题。

### Step 2: 采集前准备
确保任务目录结构存在：
- data/raw/
- memory/visited.json

### Step 3: 数据采集循环

对于每个 priority=1 且 status=pending 的子主题：

#### 3.1 搜索阶段
使用 web_search 工具搜索关键词。

#### 3.2 页面理解（Deep Browser）
使用 deep_browser 的 understand 能力：

```
action: "understand"
url: "目标页面 URL"
```

返回：
- 页面类型（电商、搜索结果、文章等）
- 布局模式
- 交互元素
- 数据区域
- 分页机制

#### 3.3 内容采集（Deep Browser）
使用 deep_browser 的 collect 能力：

```
action: "collect"
url: "目标页面 URL"
selectors: {
  title: "h1",
  content: "article, .content",
  list_items: ".item, .product",
  metadata: ".meta, time"
}
save_to: "{TASK_DIR}/data/raw/{sub_topic_name}-{index}.json"
```

#### 3.4 复杂页面操作（Deep Browser）

如果页面需要交互（翻页、筛选等）：

**操作**：
```
action: "operate"
operation_type: "click"
selector: ".pagination-next"
```

**观察**：
```
action: "observe"
expected_change: "new content loaded"
```

**继续采集**：
```
action: "collect"
...
```

#### 3.5 记忆积累（Deep Browser）
对于有规律的网站，保存模式：

```
action: "remember"
site_pattern_id: "{domain}-{page-type}"
url: "页面 URL"
selectors: { ... }
```

#### 3.6 记录访问
更新 memory/visited.json：
```json
{
  "visited_urls": [
    {
      "url": "https://...",
      "visited_at": "2024-01-01T00:00:00Z",
      "sub_topic": "市场规模",
      "data_points": 5
    }
  ]
}
```

### Step 4: 更新进度
每个子主题完成后，更新 plan.json 的状态。

### Step 5: 采集完成
更新 task.json 状态为 "collection_completed"。

## 使用的 Tool

| Tool | 用途 |
|------|------|
| read | 读取 plan.json |
| write | 保存数据、更新状态 |
| web_search | 搜索关键词 |
| deep_browser | 页面理解、操作、采集、记忆 |
| task_manager | 更新任务状态 |

## Deep Browser 使用策略

### 页面类型识别

| 页面类型 | 采集策略 |
|---------|---------|
| ecommerce-product | 采集标题、价格、规格、评论 |
| search-results | 遍历结果列表，采集详情页 |
| article | 采集标题、正文、作者、日期 |
| listing | 采集列表项，处理分页 |
| documentation | 采集目录和内容 |

### 分页处理

**点击分页**：
```
operate: { operation_type: "click", selector: ".next" }
observe: { expected_change: "page change" }
collect: { ... }
```

**滚动加载**：
```
operate: { operation_type: "scroll", direction: "bottom" }
observe: { expected_change: "new items loaded" }
collect: { ... }
```

### 记忆利用

如果 understand 返回 `source: "memory"`，直接使用缓存的 selectors：

```
action: "collect"
url: "..."
selectors: { 使用缓存的 selectors }
```

## 输出

- data/raw/：原始采集数据
- memory/visited.json：已访问 URL 记录
- plan.json：更新子主题状态
- task.json：状态更新为 "collection_completed"

## 触发下一个 Skill

当 task.json 状态变为 "collection_completed" 后，market-research-processor Skill 将自动激活。
