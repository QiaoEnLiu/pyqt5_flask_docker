# 使用基於 Linux 的基礎映像
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /api

# 複製應用程式代碼到容器中
COPY flask-api.py .

# 安裝 Flask
RUN pip install flask

# 指定容器啟動時執行的命令
CMD ["python3", "flask-api.py"]

# 暴露應用程式的端口
EXPOSE 5000
