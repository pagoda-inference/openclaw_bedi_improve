# 元素交互性分析提示词

你是一个网页交互专家。分析以下页面元素，判断哪些元素是可交互的，以及它们的交互用途。

页面元素列表：
{ELEMENTS}

请分析并返回以下 JSON 格式：
{
  "interactive_elements": [
    {
      "ref": 元素编号,
      "interaction_type": "交互类型（click/type/select/scroll/hover/drag）",
      "purpose": "这个元素的交互目的",
      "importance": "重要性（high/medium/low）",
      "expected_outcome": "预期交互结果"
    }
  ],
  "element_groups": [
    {
      "refs": [元素编号数组],
      "group_type": "分组类型（form/navigation/list/menu）",
      "purpose": "这组元素的共同目的"
    }
  ]
}

只返回 JSON，不要其他内容。

## 分析要点

1. **交互类型判断**：
   - click: 按钮、链接、可点击元素
   - type: 输入框、文本域
   - select: 下拉选择框
   - scroll: 滚动区域
   - hover: 鼠标悬停触发
   - drag: 拖拽元素

2. **重要性评估**：
   - high: 主要操作按钮、关键导航、表单提交
   - medium: 次要操作、辅助导航
   - low: 装饰性元素、可选操作

3. **元素分组**：
   - form: 表单相关元素
   - navigation: 导航相关元素
   - list: 列表项
   - menu: 菜单项

4. **预期结果**：
   - 描述交互后可能发生的变化
   - 页面跳转、内容更新、状态改变等
