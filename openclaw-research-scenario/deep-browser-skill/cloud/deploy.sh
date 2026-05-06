#!/bin/bash

set -e

echo "=== OpenCLI Cloud Deployment ==="

# 构建镜像
echo "Building Docker image..."
docker build -t opencli-cloud:latest .

# 启动容器
echo "Starting container..."
docker-compose up -d

# 等待服务就绪
echo "Waiting for CDP to be ready..."
for i in {1..30}; do
  if curl -s http://localhost:9222/json/version > /dev/null 2>&1; then
    echo "✓ CDP is ready"
    break
  fi
  sleep 1
done

# 验证 OpenCLI
echo "Verifying OpenCLI..."
docker exec opencli-browser opencli --version

echo "=== Deployment Complete ==="
echo "CDP endpoint: http://localhost:9222"
echo ""
echo "Test commands:"
echo "  docker exec opencli-browser opencli browser open https://example.com"
echo "  docker exec opencli-browser opencli browser state"
echo "  docker exec opencli-browser opencli browser network"
