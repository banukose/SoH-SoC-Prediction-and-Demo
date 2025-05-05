# Base image: Python 3.10
FROM python:3.10-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gereken dosyaları container içine kopyala
COPY demo/streamlit_app.py .
COPY models/ ./models/
COPY data/ ./data/
COPY requirements.txt .

# Paketleri yükle
RUN pip install --no-cache-dir -r requirements.txt

# portunu expose et
EXPOSE 8000

# Streamlit uygulamasını başlat
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.enableCORS=false"]
