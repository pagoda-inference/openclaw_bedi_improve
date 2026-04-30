# 网络分析参考文档

本文档提供网络请求分析的方法论和框架，帮助智能体识别数据源和API模式，以只读方式获取数据。

## 分析目标

网络分析的核心目标是理解：
1. **请求用途** - 为什么发起这个请求
2. **数据类型** - 交换了什么数据
3. **API模式** - 如何直接调用（只读方式）
4. **数据源** - 数据从哪里来
5. **安全性** - 该请求是读取还是写入

## 分析维度

### 1. 请求用途识别

**常见请求用途：**

| 用途类型 | 特征 | 安全性 | 示例 |
|---------|------|--------|------|
| data-fetch | 获取展示数据 | ✅ 只读 | 商品列表、用户信息 |
| auth | 认证授权 | ❌ 写入 | 登录、token刷新 |
| tracking | 行为追踪 | ⚠️ 需判断 | 页面访问、点击事件 |
| analytics | 数据统计 | ✅ 只读 | 性能监控、用户分析 |
| config | 配置加载 | ✅ 只读 | 应用设置、功能开关 |
| asset | 资源加载 | ✅ 只读 | 图片、CSS、JS文件 |

**识别方法：**
- 查看请求URL路径（/api/, /auth/, /track/）
- 检查请求方法（GET通常获取数据，POST通常提交数据）
- 分析请求参数和响应内容
- 观察请求时机（页面加载、用户操作后）

### 2. 数据类型判断

**常见数据类型：**

| 数据类型 | URL特征 | 响应特征 | 安全性 |
|---------|---------|---------|--------|
| product | /products, /items | 商品信息、价格、库存 | ✅ 只读 |
| user | /users, /profile | 用户信息、权限、设置 | ✅ 只读 |
| content | /articles, /posts | 文章、评论、媒体 | ✅ 只读 |
| config | /config, /settings | 配置项、功能开关 | ✅ 只读 |
| analytics | /analytics, /metrics | 统计数据、指标 | ✅ 只读 |
| search | /search, /query | 搜索结果、筛选条件 | ✅ 只读 |

**判断方法：**
- 分析URL路径关键词
- 查看响应JSON结构
- 识别数据字段名称
- 理解业务上下文

### 3. API模式发现

**常见API模式：**

**RESTful API:**
```
GET    /api/products        # 获取列表 ✅ 只读
GET    /api/products/123    # 获取详情 ✅ 只读
POST   /api/products        # 创建 ❌ 写入
PUT    /api/products/123    # 更新 ❌ 写入
DELETE /api/products/123    # 删除 ❌ 写入
```

**GraphQL:**
```
POST /graphql
{
  "query": "{ products { id name price } }"  # 查询 ✅ 只读
}

POST /graphql
{
  "query": "mutation { createProduct(...) }"  # 变更 ❌ 写入
}
```

**搜索API:**
```
GET /api/search?q=keyword&category=1&page=1  # ✅ 只读
```

**分页模式:**
```
# 页码分页 ✅ 只读
?page=1&limit=20

# 偏移分页 ✅ 只读
?offset=0&limit=20

# 游标分页 ✅ 只读
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
| 安全性 | 是否为只读操作 | 检查HTTP方法和URL模式 |

**调用可行性：**

```
✅ 可直接调用（只读）
├─ 无认证或简单认证
├─ 参数明确且稳定
├─ 无严格速率限制
├─ 返回数据完整
└─ GET请求或只读POST（如搜索）

⚠️ 需要处理
├─ 需要登录获取token
├─ 参数需要计算或加密
├─ 有速率限制但可接受
└─ 需要多次请求组合数据

❌ 不建议直接调用
├─ 复杂的认证流程
├─ 严格的反爬机制
├─ 严格的速率限制
├─ 数据不完整或加密
└─ 写入类API（POST/PUT/DELETE非搜索类）
```

### 5. API安全性分类

**只读API（允许调用）：**

| API类型 | HTTP方法 | 特征 | 示例 |
|---------|---------|------|------|
| 数据获取 | GET | 获取展示数据 | GET /api/products |
| 搜索 | GET/POST | 获取搜索结果 | POST /api/search |
| 配置获取 | GET | 获取配置信息 | GET /api/config |
| 列表查询 | GET | 获取列表数据 | GET /api/users |

**写入API（禁止调用）：**

| API类型 | HTTP方法 | 特征 | 示例 |
|---------|---------|------|------|
| 创建数据 | POST | 创建新资源 | POST /api/products |
| 更新数据 | PUT/PATCH | 修改已有资源 | PUT /api/products/123 |
| 删除数据 | DELETE | 删除资源 | DELETE /api/products/123 |
| 认证操作 | POST | 登录/注册 | POST /api/auth/login |
| 提交操作 | POST | 提交表单数据 | POST /api/contact |

**注意**：同样是POST请求，搜索类API（如 POST /api/search）是只读操作，而创建类API（如 POST /api/products）是写入操作。需要根据业务上下文判断。

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
request.url
request.method
request.headers
request.postData
response.body
```

**响应分析：**
```javascript
response.status
response.headers
response.json()
```

### 请求拦截

**修改请求：**
```javascript
// 测试只读API
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

分析结果应保存为Markdown格式的API列表，**必须包含安全性判断**：

```markdown
## 网络请求

总计: 15 个请求

| 方法 | URL | 用途 | 数据类型 | 安全性 | 重要性 |
|------|-----|------|---------|--------|--------|
| GET | /api/products | data-fetch | product | ✅ 只读 | high |
| POST | /api/search | data-fetch | search | ✅ 只读 | high |
| GET | /api/user/profile | data-fetch | user | ✅ 只读 | medium |
| POST | /api/auth/login | auth | auth | ❌ 写入 | - |
| POST | /api/contact | submit | contact | ❌ 写入 | - |

## API端点

### 商品列表API
- **URL**: `/api/products`
- **方法**: GET
- **用途**: 获取商品列表
- **安全性**: ✅ 只读
- **认证**: 不需要
- **参数**:
  - page: 页码（可选）
  - limit: 每页数量（可选）
  - category: 分类ID（可选）
- **响应**:
  ```json
  {
    "products": [...],
    "total": 100,
    "page": 1
  }
  ```
- **直接调用**: ✅ 可直接调用

### 登录API
- **URL**: `/api/auth/login`
- **方法**: POST
- **用途**: 用户登录
- **安全性**: ❌ 写入
- **直接调用**: ❌ 禁止调用
```

### 数据源模式格式

```markdown
## 数据源

### 商品数据源
- **模式**: `/api/products*`
- **描述**: 商品相关数据
- **安全性**: ✅ 只读
- **示例URL**:
  - `/api/products` - 商品列表
  - `/api/products/123` - 商品详情
  - `/api/products/search` - 商品搜索

### 用户认证
- **模式**: `/api/auth/*`
- **描述**: 认证相关API
- **安全性**: ❌ 写入
- **注意**: 禁止调用
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
   ├─ 按安全性分类（只读/写入）
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
   ├─ 判断安全性（只读才可调用）
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
   - 只关注只读API

2. **安全性判断**
   - 每个API必须判断只读/写入
   - GET请求通常是只读
   - POST请求需要根据业务判断
   - PUT/DELETE请求通常是写入

3. **完整性验证**
   - 测试不同参数组合
   - 验证边界情况
   - 检查错误响应

4. **模式识别**
   - 提取URL模式
   - 识别参数规律
   - 记录通用规则

5. **合规考虑**
   - 检查robots.txt
   - 遵守服务条款
   - 控制请求频率

## 常见问题

**Q: 如何找到隐藏的API？**
A: 执行各种页面操作，观察Network面板中的请求

**Q: 如何处理需要登录的API？**
A: 记录该API入口，标注需要认证。不建议尝试登录。

**Q: POST请求一定是写入操作吗？**
A: 不一定。搜索类API通常使用POST方法但属于只读操作。需要根据业务上下文判断。

**Q: API返回数据不完整怎么办？**
A: 检查是否有分页，或需要多次请求组合数据

**Q: 如何区分只读API和写入API？**
A: 判断API调用的目的是获取数据还是修改数据。GET请求通常是只读；POST请求如果是搜索/查询类则为只读，如果是创建/提交类则为写入。

## 相关参考

- [页面分析参考](page_analysis.md)
- [元素分析参考](element_analysis.md)
- [浏览器操作参考](browser_operations_reference.md)
