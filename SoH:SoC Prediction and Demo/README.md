
# 🔋 Battery Prediction(SoH and SoC)

Bu proje, lityum-iyon pillerin sağlık durumunu (SOH - State of Health) ve şarj durumunu (SOC - State of Charge) tahmin etmeye yönelik bir makine öğrenimi uygulamasıdır.

## 🚀 Proje Yapısı

```
battery-health-prediction/
│
├── data/
│   └── processed/                # İşlenmiş veriler (CSV dosyaları)
│
├── models/                       # Eğitilmiş modeller (.pkl, .h5)
│
├── demo/
│   └── streamlit_app.py          # Streamlit arayüzü
│   └── App.js                    # React arayüzü
│
├── app/                          # Flask API uygulaması
│   ├── main.py
│   └── ...
│
├── Dockerfile                    # Docker yapılandırması
├── docker-compose.yml            # (Opsiyonel) Genişletilmiş yapılandırma
│
└── README.md
```

## ⚙️ Kullanılan Teknolojiler

- Python
- Scikit-learn
- TensorFlow / Keras
- Streamlit
- Flask
- Docker
- React

## 🧪 Özellikler

- 🔧 SOH tahmini (Random Forest ile)
- 📈 SOC tahmini (LSTM ile)
- 🌐 Flask REST API
- 🖥️ Streamlit tabanlı demo arayüzü
- 🖥️ React tabanlı demo arayüzü
- 🐳 Docker uyumluluğu

## 💡 Kullanım

### 1. Gerekli kütüphaneleri yükle
```
pip install -r requirements.txt
```

### 2. Streamlit Arayüzünü Başlat
```
cd demo
streamlit run streamlit_app.py
```

### 3. Streamlit Arayüzünü Başlat
```
cd demo
npm install
npm start
```

### 4. Flask API'yi Başlat (İsteğe bağlı)
```
cd app
python main.py
```

### 5. Docker ile çalıştır
```
docker build -t battery-app .
docker run -p 8501:8501 battery-app
```

## 📊 Model Performansı

- ✅ SOH (Random Forest)
  - R²: 0.98
  - MSE: 0.00025

- ✅ SOC (LSTM)
  - MAE: 0.026

## 📎 Notlar

- Model dosyaları `models/` altında yer alır.
- Uygulama hem lokal hem Docker ortamında çalışacak şekilde yapılandırılmıştır.

---

**Hazırlayan:** Banu 
