# 浏览器操作参考文档

本文档提供浏览器操作的详细说明和使用模式，帮助智能体正确操作浏览器。

## 核心操作

### 导航操作

**open(url)**
- 在浏览器中打开URL
- 等待页面加载完成
- 返回：`{"status": "opened", "url": url}`

**get_url()**
- 获取当前页面URL
- 返回：URL字符串

**get_title()**
- 获取当前页面标题
- 返回：标题字符串

### 页面状态

**get_state()**
- 捕获当前页面状态
- 返回：`{"elements": [...], "element_count": n, "has_more_below": bool}`
- 元素包括：ref, tag, text, visible, role

**extract()**
- 提取页面内容
- 返回：结构化内容对象

### 交互操作

**click(target)**
- 通过引用编号点击元素
- 等待结果变化
- 返回：`{"status": "clicked", "target": ref}`

**type_text(target, text)**
- 在输入元素中输入文本
- Target: 元素引用编号
- 返回：`{"status": "typed", "target": ref, "text": text}`

**scroll(direction, amount)**
- 在指定方向滚动页面
- Direction: "up" 或 "down"
- Amount: 滚动像素数
- 返回：`{"status": "scrolled", ...}`

### 数据提取

**get_text(selector)**
- 获取元素的文本内容
- Selector: CSS选择器字符串
- 返回：文本内容字符串

**screenshot(save_path)**
- 截取当前页面截图
- Save path: 保存图片的文件路径
- 返回：`{"status": "captured", "path": path}`

### 网络监控

**network(filter_type)**
- 捕获网络请求
- Filter type: 可选的过滤字符串
- 返回：网络请求列表

## 使用模式

### 模式1：基本导航

```
1. open(url)
2. get_state()
3. 分析状态
4. 决定下一步操作
```

### 模式2：表单交互

```
1. get_state()
2. 识别表单元素
3. type_text(input_ref, value)
4. click(submit_ref)
5. get_state() 验证结果
```

### 模式3：分页处理

```
1. get_state()
2. 提取当前页数据
3. 识别下一页元素
4. click(next_page_ref)
5. 等待加载
6. 重复直到完成
```

### 模式4：搜索操作

```
1. get_state()
2. 查找搜索输入框
3. type_text(search_input, query)
4. click(search_button)
5. get_state() 分析结果
```

## 错误处理

### 常见错误

**元素未找到**
- 原因：元素引用不存在
- 解决：使用get_state()刷新状态

**超时**
- 原因：页面加载或操作耗时过长
- 解决：增加超时时间或检查网络

**浏览器无响应**
- 原因：浏览器崩溃或冻结
- 解决：重启浏览器会话

### 恢复策略

1. **状态刷新**：调用get_state()获取当前元素引用
2. **重试**：使用新状态重试失败的操作
3. **降级**：如果浏览器不可用，使用web-fetch

## 最佳实践

1. **交互前始终检查状态**
   - 页面更新后元素可能改变
   - 使用get_state()刷新引用

2. **等待页面稳定**
   - 点击后等待页面稳定
   - 检查加载指示器

3. **使用特定选择器**
   - 优先使用ID和唯一类名
   - 避免可能匹配多个元素的通用选择器

4. **处理动态内容**
   - 滚动以加载更多内容
   - 等待AJAX请求完成

5. **验证操作**
   - 交互后验证预期结果
   - 使用get_state()或get_url()确认

## 限制

- 无法与系统级对话框交互
- 对浏览器设置的控制有限
- 可能无法处理所有反爬措施
- 需要启用JavaScript的浏览器

## 相关参考

- [页面分析参考](page_analysis.md)
- [元素分析参考](element_analysis.md)
- [网络分析参考](network_analysis.md)
