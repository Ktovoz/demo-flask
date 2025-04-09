# 使用官方Python基础镜像作为构建阶段
FROM python:3.11-slim as builder

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# 安装Python依赖
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# 最终阶段
FROM python:3.11-slim

# 创建非root用户
RUN useradd -m appuser

WORKDIR /app

# 从builder阶段复制wheels
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# 安装依赖
RUN pip install --no-cache /wheels/*

# 复制项目文件
COPY . .

# 设置权限
RUN chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python", "run.py"] 