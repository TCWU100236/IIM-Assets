# 使用 Python Image
FROM python:3.12

# 安裝必要的系統函式庫（包含 zbar）
RUN apt-get update && apt-get install -y \
    libzbar0 \
    libglib2.0-0 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 複製專案環境與相關檔案
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir --verbose
COPY . .

# 啟動 Django 開發伺服器
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]