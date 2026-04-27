# 市场调研能力扩展

## 概述

本文件定义了 OpenClaw 的市场调研能力，包括任务管理、数据采集、数据处理和报告生成。

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

深度浏览器工具，提供四大能力：

**understand（理解页面）**：
- 分析页面类型（电商、搜索结果、文章等）
- 识别页面布局模式
- 检测交互元素和数据区域
- 自动识别分页机制

**operate（执行操作）**：
- navigate: 导航到 URL
- click: 点击元素
- type: 输入文本
- scroll: 滚动页面
- wait: 等待元素出现

**observe（观察变化）**：
- 获取当前页面内容
- 截图
- 检测预期变化

**remember（记忆积累）**：
- 保存网站模式到本地
- 积累选择器知识
- 提高后续访问效率

**collect（采集内容）**：
- 根据选择器提取内容
- 支持批量采集列表项
- 自动保存到指定路径

### report_renderer

报告渲染工具，将分析结果生成 HTML 报告。

**支持的模板**：
- `industry-overview`: 行业概览报告
- `quick-brief`: 快速简报
- `competitor-compare`: 竞品对比
- `deep-research`: 深度研究

## 使用指南

### 发起市场调研

当用户请求市场调研、行业分析、竞品研究时：

1. **创建任务**
```
使用 task_manager 创建任务：
- action: "create"
- user_input: 用户原始需求
- config: 调研配置（深度、输出格式等）
```

2. **规划调研**
```
读取 market-research-planner Skill
分解主题，生成 plan.json
更新状态为 planning_completed
```

3. **采集数据**
```
读取 market-research-collector Skill
使用 deep_browser 采集网页内容
存储到 data/raw/
更新状态为 collection_completed
```

4. **处理数据**
```
读取 market-research-processor Skill
清理、验证、分析数据
存储到 data/analysis/
更新状态为 processing_completed
```

5. **生成报告**
```
读取 market-research-reporter Skill
选择模板，组织内容
渲染 HTML 报告
更新状态为 completed
```

### 任务恢复

当会话中断后恢复：

```
使用 task_manager 恢复任务：
- action: "recover"
- task_id: 任务 ID

根据恢复的状态，继续执行对应的 Skill。
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

## Deep Browser 记忆

```
~/.openclaw/deep-browser/
├── patterns/              # 网站模式记忆
│   └── {pattern-id}.json
└── sessions/              # 会话记录
```

网站模式记忆示例：
```json
{
  "id": "ecommerce-amazon",
  "domain": "amazon.com",
  "page_type": "ecommerce-product",
  "selectors": {
    "title": "#productTitle",
    "price": ".a-price .a-offscreen",
    "reviews": "#reviews-medley-footer"
  },
  "pagination": {
    "type": "click",
    "selector": ".s-pagination-next"
  },
  "success_count": 5
}
```

## 注意事项

1. **任务隔离**：每个任务独立存储，互不干扰
2. **状态驱动**：根据 task.json 的状态自动触发对应 Skill
3. **记忆积累**：Deep Browser 会积累网站模式，提高效率
4. **错误恢复**：支持从中断点恢复任务
