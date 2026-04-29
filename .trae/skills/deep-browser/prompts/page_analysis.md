# 页面结构分析提示词

你是一个网页结构分析专家。分析以下页面内容，返回 JSON 格式的分析结果。

页面内容：
{PAGE_CONTENT}

请深入分析页面结构，返回以下 JSON 格式：
{
  "page_type": "页面类型（listing/product/search/login/form/content/checkout/generic）",
  "page_type_confidence": 0.95,
  "layout_pattern": "布局模式（single-column/two-column/three-column/dashboard/fluid）",
  "semantic_regions": [
    {
      "name": "区域名称（header/navigation/main-content/sidebar/footer/breadcrumb）",
      "selector": "CSS选择器",
      "importance": "重要性（high/medium/low）"
    }
  ],
  "data_regions": [
    {
      "selector": "CSS选择器",
      "type": "数据类型（product-list/article/table/form/sidebar）",
      "description": "这个区域包含什么内容",
      "data_structure": {
        "fields": ["字段1", "字段2"],
        "item_count": 10
      }
    }
  ],
  "pagination": {
    "type": "分页类型（click/scroll/load-more/none）",
    "selector": "分页元素的选择器",
    "description": "如何翻到下一页",
    "current_page": 1,
    "total_pages": 10
  },
  "forms": [
    {
      "purpose": "表单用途（search/login/filter/contact）",
      "selectors": {
        "form": "表单选择器",
        "inputs": ["输入框选择器数组"],
        "submit": "提交按钮选择器"
      },
      "required_fields": ["必填字段"]
    }
  ],
  "navigation_hints": [
    {
      "path": "导航路径描述",
      "target": "目标页面类型",
      "importance": "重要性"
    }
  ],
  "suggested_actions": [
    {
      "action": "操作类型（click/scroll/input/wait）",
      "target": "目标元素",
      "purpose": "操作目的",
      "priority": "优先级（high/medium/low）"
    }
  ],
  "content_summary": {
    "main_topic": "页面主要内容主题",
    "key_entities": ["关键实体1", "关键实体2"],
    "language": "页面语言"
  }
}

只返回 JSON，不要其他内容。确保 JSON 格式正确，可以被解析。
