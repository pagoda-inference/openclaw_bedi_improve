---
name: market-research-reporter
description: "市场调研报告生成，将分析结果组织成 HTML 报告"
trigger: 当 task_manager 状态为 "processing_completed" 时激活
---

# 报告生成 Skill

## 工作流程

### Step 1: 读取分析结果
读取 data/analysis/ 目录下的分析结果和 plan.json 获取调研主题信息。

### Step 2: 模板选择
使用 LLM 根据用户需求和数据分析结果选择最合适的模板：

**可用模板：**
- industry-overview：市场规模、竞争格局、发展趋势
- competitor-compare：产品/公司对比
- quick-brief：快速了解核心要点
- deep-research：深度主题研究

### Step 3: 内容组织
使用 report_organizer 工具组织内容。

### Step 4: HTML 渲染
使用 report_renderer 工具生成 HTML。

### Step 5: 保存报告
将 HTML 保存到 output/ 目录。

### Step 6: 生成完成
更新 task.json 状态为 "completed"。

## 使用的 Tool

- read: 读取分析结果
- write: 保存报告
- report_organizer: 组织内容
- report_renderer: 渲染 HTML
- task_manager: 更新任务状态

## 输出

- output/report.html：最终报告
- task.json 状态更新为 "completed"

## 报告模板

### industry-overview 模板

```json
{
  "template_id": "industry-overview",
  "sections": [
    {"id": "summary", "title": "核心概述", "required": true},
    {"id": "market_size", "title": "市场规模", "required": true},
    {"id": "competition", "title": "竞争格局", "required": true},
    {"id": "trends", "title": "发展趋势", "required": false},
    {"id": "conclusion", "title": "结论与建议", "required": true}
  ]
}
```

### quick-brief 模板

```json
{
  "template_id": "quick-brief",
  "sections": [
    {"id": "key_findings", "title": "核心结论", "required": true},
    {"id": "key_data", "title": "关键数据", "required": true},
    {"id": "suggestions", "title": "行动建议", "required": true}
  ]
}
```
