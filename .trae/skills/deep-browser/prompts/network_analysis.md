# 网络请求分析提示词

你是一个网络请求分析专家。分析以下网络请求，判断它们的用途和数据类型。

网络请求列表：
{NETWORK_ENTRIES}

请分析并返回以下 JSON 格式：
{
  "api_endpoints": [
    {
      "url": "请求URL",
      "method": "HTTP方法",
      "purpose": "请求用途（data-fetch/auth/tracking/analytics/unknown）",
      "data_type": "返回数据类型（product/user/config/unknown）",
      "importance": "重要性（high/medium/low）",
      "suggested_use": "建议如何使用这个API"
    }
  ],
  "data_sources": [
    {
      "pattern": "URL模式",
      "description": "数据源描述",
      "example_url": "示例URL"
    }
  ]
}

只返回 JSON，不要其他内容。

## 分析要点

1. **请求用途判断**：
   - data-fetch: 数据获取请求
   - auth: 认证相关请求
   - tracking: 用户行为追踪
   - analytics: 数据分析统计
   - unknown: 无法确定用途

2. **数据类型识别**：
   - product: 产品数据
   - user: 用户信息
   - config: 配置数据
   - content: 内容数据
   - unknown: 未知类型

3. **重要性评估**：
   - high: 核心业务数据、关键API
   - medium: 辅助功能、次要数据
   - low: 统计、追踪、非必要请求

4. **使用建议**：
   - 是否可以直接调用
   - 需要的参数和认证
   - 返回数据的结构
   - 潜在的使用场景

5. **数据源模式**：
   - 识别API的URL模式
   - 发现可复用的数据端点
   - 提取通用的请求参数
