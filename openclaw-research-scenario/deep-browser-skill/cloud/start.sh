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
