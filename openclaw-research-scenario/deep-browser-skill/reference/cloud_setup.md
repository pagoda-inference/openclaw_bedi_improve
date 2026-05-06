# 云端 OpenCLI 配置参考文档

本文档说明如何在云端/容器环境中配置 OpenCLI，无需 Chrome 扩展。

## 两种连接模式

OpenCLI 支持两种浏览器连接模式：

| 模式 | 需要扩展 | 需要 daemon | 连接方式 | 适用场景 |
|------|---------|------------|---------|---------|
| **BrowserBridge** | ✅ 需要 | ✅ 需要 | daemon + Chrome 扩展 | 本地开发，复用用户浏览器 |
| **CDPBridge** | ❌ 不需要 | ❌ 不需要 | 直接 CDP WebSocket | 云端/容器，无头模式 |

云端推荐使用 **CDPBridge 模式**。

## CDPBridge 原理

CDPBridge 直接通过 WebSocket 连接 Chrome DevTools Protocol (CDP)，不需要 daemon 和 Chrome 扩展：

```
┌─────────────────────────────────────────────────────┐
│                  容器/云服务器                        │
│  ┌─────────────┐          ┌─────────────┐           │
│  │ Chromium    │   CDP    │ OpenCLI     │           │
│  │ (Headless)  │◄────────►│ CDPBridge   │           │
│  │ :9222       │  WebSocket│             │           │
│  └─────────────┘          └─────────────┘           │
└─────────────────────────────────────────────────────┘
```

## 快速配置

### 1. 启动 Chromium（headless + CDP）

```bash
chromium \
  --headless \
  --no-sandbox \
  --disable-gpu \
  --disable-dev-shm-usage \
  --remote-debugging-port=9222 \
  --remote-debugging-address=0.0.0.0 \
  --user-data-dir=/tmp/chrome-profile &

# 等待启动
sleep 3

# 验证 CDP 可用
curl -s http://localhost:9222/json/version
```

### 2. 设置环境变量

```bash
export OPENCLI_CDP_ENDPOINT="http://localhost:9222"
```

### 3. 使用 OpenCLI

```bash
opencli browser open "https://example.com"
opencli browser state
opencli browser network
```

## Docker 部署

### Dockerfile

```dockerfile
FROM node:20-slim

# 安装 Chromium 和依赖
RUN apt-get update && apt-get install -y \
    chromium \
    fonts-wqy-zenhei \
    fonts-ipafont-gothic \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# 设置 Chromium 路径
ENV CHROMIUM_PATH=/usr/bin/chromium

# 安装 OpenCLI
RUN npm install -g @jackwener/opencli

# 创建工作目录
WORKDIR /app

# 复制启动脚本
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# 暴露 CDP 端口
EXPOSE 9222

# 启动
CMD ["/app/start.sh"]
```

### start.sh

```bash
#!/bin/bash

# 启动 Chromium (headless + CDP)
chromium \
  --headless \
  --no-sandbox \
  --disable-gpu \
  --disable-dev-shm-usage \
  --remote-debugging-port=9222 \
  --remote-debugging-address=0.0.0.0 \
  --disable-background-networking \
  --disable-default-apps \
  --disable-extensions \
  --disable-sync \
  --no-first-run \
  --enable-automation \
  --password-store=basic \
  --use-mock-keychain \
  --user-data-dir=/tmp/chrome-profile &

# 等待 Chromium 启动
sleep 3

# 验证 CDP 可用
if curl -s http://localhost:9222/json/version > /dev/null 2>&1; then
    echo "✓ Chromium CDP ready at localhost:9222"
else
    echo "✗ Chromium CDP failed to start"
    exit 1
fi

# 设置 OpenCLI 环境变量
export OPENCLI_CDP_ENDPOINT="http://localhost:9222"

# 保持容器运行
tail -f /dev/null
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  opencli-browser:
    build: .
    container_name: opencli-browser
    ports:
      - "9222:9222"
    environment:
      - OPENCLI_CDP_ENDPOINT=http://localhost:9222
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    shm_size: '2gb'
```

### 使用

```bash
# 构建并启动
docker-compose up -d

# 测试
docker exec opencli-browser opencli browser open "https://example.com"
docker exec opencli-browser opencli browser state
```

## Kubernetes 部署

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: opencli-browser
spec:
  replicas: 1
  selector:
    matchLabels:
      app: opencli-browser
  template:
    metadata:
      labels:
        app: opencli-browser
    spec:
      containers:
      - name: opencli-browser
        image: opencli-cloud:latest
        ports:
        - containerPort: 9222
        resources:
          limits:
            memory: "4Gi"
            cpu: "2"
          requests:
            memory: "2Gi"
            cpu: "1"
        env:
        - name: OPENCLI_CDP_ENDPOINT
          value: "http://localhost:9222"
        volumeMounts:
        - name: dshm
          mountPath: /dev/shm
      volumes:
      - name: dshm
        emptyDir:
          medium: Memory
          sizeLimit: "2Gi"
```

### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: opencli-browser
spec:
  selector:
    app: opencli-browser
  ports:
  - port: 9222
    targetPort: 9222
  type: ClusterIP
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OPENCLI_CDP_ENDPOINT` | CDP 端点 URL | 无（BrowserBridge 模式） |
| `OPENCLI_CDP_TARGET` | 目标页面匹配模式 | 自动选择 |
| `OPENCLI_BROWSER_CONNECT_TIMEOUT` | 连接超时（秒） | 30 |
| `OPENCLI_BROWSER_COMMAND_TIMEOUT` | 命令超时（秒） | 60 |

## 安全考虑

1. **网络隔离**：CDP 端口不对外暴露，仅内部访问
2. **认证**：可在上层添加代理进行认证
3. **会话隔离**：每次任务使用独立的浏览器 profile
4. **资源限制**：设置内存和 CPU 限制，防止资源耗尽

## 常见问题

### Q: CDPBridge 和 BrowserBridge 功能一样吗？

A: 大部分功能相同，但有以下差异：

| 功能 | BrowserBridge | CDPBridge |
|------|--------------|-----------|
| 页面操作 | ✅ | ✅ |
| 网络分析 | ✅ | ✅ |
| 截图 | ✅ | ✅ |
| 标签页管理 | ✅ | ❌（单标签） |
| 登录态复用 | ✅（用户浏览器） | ❌（独立实例） |

### Q: 如何处理需要登录的网站？

A: CDPBridge 模式下，每次启动都是全新的浏览器实例，没有登录态。解决方案：

1. 使用持久化的 user-data-dir
2. 通过脚本自动登录
3. 注入 cookie

### Q: 如何调试？

A: 启用详细日志：

```bash
export OPENCLI_VERBOSE=1
opencli browser open "https://example.com"
```

## 相关参考

- [浏览器操作参考](browser_operations_reference.md) — OpenCLI 命令详解
- [站点侦察](site_recon.md) — Pattern 分类
