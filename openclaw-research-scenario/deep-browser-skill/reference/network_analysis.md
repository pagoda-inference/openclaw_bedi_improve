# 网络分析参考文档

本文档提供网络请求分析的方法论和框架，帮助智能体识别数据源和API模式。

## 分析目标

网络分析的核心目标是理解：
1. **请求用途** - 为什么发起这个请求
2. **数据类型** - 交换了什么数据
3. **API模式** - 如何直接调用
4. **数据源** - 数据从哪里来

## 分析维度

### 1. 请求用途识别

**常见请求用途：**

| 用途类型 | 特征 | 示例 |
|---------|------|------|
| data-fetch | 获取展示数据 | 商品列表、用户信息 |
| auth | 认证授权 | 登录、token刷新 |
| tracking | 行为追踪 | 页面访问、点击事件 |
| analytics | 数据统计 | 性能监控、用户分析 |
| config | 配置加载 | 应用设置、功能开关 |
| asset | 资源加载 | 图片、CSS、JS文件 |

**识别方法：**
- 查看请求URL路径（/api/, /auth/, /track/）
- 检查请求方法（GET通常获取数据，POST通常提交数据）
- 分析请求参数和响应内容
- 观察请求时机（页面加载、用户操作后）

### 2. 数据类型判断

**常见数据类型：**

| 数据类型 | URL特征 | 响应特征 |
|---------|---------|---------|
| product | /products, /items | 商品信息、价格、库存 |
| user | /users, /profile | 用户信息、权限、设置 |
| content | /articles, /posts | 文章、评论、媒体 |
| config | /config, /settings | 配置项、功能开关 |
| analytics | /analytics, /metrics | 统计数据、指标 |
| search | /search, /query | 搜索结果、筛选条件 |

**判断方法：**
- 分析URL路径关键词
- 查看响应JSON结构
- 识别数据字段名称
- 理解业务上下文

### 3. API模式发现

**常见API模式：**

**RESTful API:**
```
GET    /api/products        # 获取列表
GET    /api/products/123    # 获取详情
POST   /api/products        # 创建
PUT    /api/products/123    # 更新
DELETE /api/products/123    # 删除
```

**GraphQL:**
```
POST /graphql
{
  "query": "{ products { id name price } }"
}
```

**搜索API:**
```
GET /api/search?q=keyword&category=1&page=1
```

**分页模式:**
```
# 页码分页
?page=1&limit=20

# 偏移分页
?offset=0&limit=20

# 游标分页
?cursor=abc123&limit=20
```

### 4. 直接调用评估

**评估要点：**

| 评估项 | 检查内容 | 方法 |
|--------|---------|------|
| 认证要求 | 是否需要token | 查看请求头、测试无认证访问 |
| 参数要求 | 必需参数有哪些 | 分析请求参数、测试缺失参数 |
| 速率限制 | 是否有频率限制 | 查看响应头、快速多次请求 |
| 数据完整性 | 响应是否包含所需数据 | 分析响应结构、字段完整性 |

**调用可行性：**

```
✅ 可直接调用
├─ 无认证或简单认证
├─ 参数明确且稳定
├─ 无严格速率限制
└─ 返回数据完整

⚠️ 需要处理
├─ 需要登录获取token
├─ 参数需要计算或加密
├─ 有速率限制但可接受
└─ 需要多次请求组合数据

❌ 不建议直接调用
├─ 复杂的认证流程
├─ 严格的反爬机制
├─ 严格的速率限制
└─ 数据不完整或加密
```

## 分析工具

### 浏览器开发工具

**Network面板：**
```
1. 打开开发工具 (F12)
2. 切换到Network标签
3. 筛选XHR/Fetch请求
4. 查看请求详情
```

**请求分析：**
```javascript
// 查看请求URL
request.url

// 查看请求方法
request.method

// 查看请求头
request.headers

// 查看请求参数
request.postData

// 查看响应内容
response.body
```

**响应分析：**
```javascript
// 查看响应状态
response.status

// 查看响应头
response.headers

// 查看响应数据
response.json()
```

### 请求拦截

**修改请求：**
```javascript
// 使用Chrome DevTools Override
// 或使用代理工具（Charles, Fiddler）

// 测试不同参数
fetch('/api/products', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer token'
  },
  params: {
    page: 1,
    limit: 20
  }
})
```

## 分析输出

### API端点列表格式

分析结果应保存为Markdown格式的API列表：

```markdown
## Network Requests

Total: 15 requests

| Method | URL | Purpose | Data Type | Importance |
|--------|-----|---------|-----------|------------|
| GET | /api/products | data-fetch | product | high |
| POST | /api/search | data-fetch | search | high |
| GET | /api/user/profile | data-fetch | user | medium |

## API Endpoints

### 商品列表API
- **URL**: `/api/products`
- **Method**: GET
- **Purpose**: 获取商品列表
- **Auth**: 不需要
- **Parameters**:
  - page: 页码（可选）
  - limit: 每页数量（可选）
  - category: 分类ID（可选）
- **Response**:
  ```json
  {
    "products": [...],
    "total": 100,
    "page": 1
  }
  ```
- **Direct Call**: ✅ 可直接调用
```

### 数据源模式格式

```markdown
## Data Sources

### 商品数据源
- **Pattern**: `/api/products*`
- **Description**: 商品相关数据
- **Example URLs**:
  - `/api/products` - 商品列表
  - `/api/products/123` - 商品详情
  - `/api/products/search` - 商品搜索

### 用户数据源
- **Pattern**: `/api/user/*`
- **Description**: 用户相关数据
- **Example URLs**:
  - `/api/user/profile` - 用户信息
  - `/api/user/orders` - 用户订单
```

## 分析流程

### 标准流程

```
1. 请求捕获
   ├─ 打开Network面板
   ├─ 清空请求列表
   ├─ 执行页面操作
   └─ 筛选XHR/Fetch

2. 请求分类
   ├─ 按用途分类
   ├─ 按数据类型分类
   └─ 按重要性排序

3. 详细分析
   ├─ 查看请求详情
   ├─ 分析参数结构
   └─ 检查响应数据

4. 模式提取
   ├─ 识别URL模式
   ├─ 提取参数规则
   └─ 记录认证方式

5. 可行性评估
   ├─ 测试直接调用
   ├─ 验证参数要求
   └─ 记录限制条件
```

### 特殊情况处理

**加密请求：**
- 查找加密函数
- 分析加密参数
- 尝试复现加密逻辑

**动态参数：**
- 查找参数生成位置
- 分析生成逻辑
- 记录生成规则

**WebSocket：**
- 切换到WS标签
- 查看消息格式
- 记录通信协议

## 最佳实践

1. **优先级排序**
   - 优先分析数据获取请求
   - 关注核心业务API
   - 不要忽略辅助API

2. **完整性验证**
   - 测试不同参数组合
   - 验证边界情况
   - 检查错误响应

3. **模式识别**
   - 提取URL模式
   - 识别参数规律
   - 记录通用规则

4. **合规考虑**
   - 检查robots.txt
   - 遵守服务条款
   - 控制请求频率

## 常见问题

**Q: 如何找到隐藏的API？**
A: 执行各种页面操作，观察Network面板中的请求

**Q: 如何处理需要登录的API？**
A: 先获取认证token，然后在请求头中添加认证信息

**Q: 如何绕过反爬机制？**
A: 模拟正常用户行为，设置合理的请求间隔，使用正确的请求头

**Q: API返回数据不完整怎么办？**
A: 检查是否有分页，或需要多次请求组合数据

## 相关参考

- [页面分析参考](page_analysis.md)
- [元素分析参考](element_analysis.md)
- [浏览器操作参考](browser_operations_reference.md)
