FROM node:20-slim

# 安装 Chromium 和依赖
RUN apt-get update && apt-get install -y \
    chromium \
    fonts-wqy-zenhei \
    fonts-ipafont-gothic \
    curl \
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
