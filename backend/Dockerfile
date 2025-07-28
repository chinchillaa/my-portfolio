FROM python:3.11-slim

# 作業ディレクトリの設定
WORKDIR /app

# 環境変数の設定
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.1

# システムパッケージの更新とインストール
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Pythonの依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコピー
COPY app ./app

# 非rootユーザーの作成
RUN useradd -m -u 1000 chatbot && chown -R chatbot:chatbot /app
USER chatbot

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# ポートの公開（デフォルト8000、環境変数で上書き可能）
EXPOSE 8000

# アプリケーションの起動（PORT環境変数を使用）
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}