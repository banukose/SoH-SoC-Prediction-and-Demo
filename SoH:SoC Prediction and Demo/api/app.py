from flask import Flask, request, jsonify
import joblib
import numpy as np
import tensorflow.keras.models as keras_models
from flask_cors import CORS  

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  

# 🔋 SOH Modeli Yükle (sklearn)
soh_model = joblib.load("models/soh_model.pkl")

# 🔌 SOC Modeli Yükle (Keras)
soc_model = keras_models.load_model("models/soc_model.h5")

# -------------------------------
# ✅ Root Endpoint: /
# -------------------------------
@app.route('/')
def index():
    return (
        "📡 Flask API Aktif!<br>"
        "Kullanılabilir endpoint'ler:<br>"
        "🔋 POST /predict-soh<br>"
        "🔌 POST /predict-soc"
    )

# -------------------------------
# /predict-soh endpoint'i
# -------------------------------
@app.route('/predict-soh', methods=['POST'])
def predict_soh():
    data = request.json
    try:
        input_data = np.array([
            data['avg_voltage'],
            data['avg_current'],
            data['max_temperature']
        ]).reshape(1, -1)

        prediction = soh_model.predict(input_data)[0]
        return jsonify({'predicted_soh': round(float(prediction), 4)})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# -------------------------------
# /predict-soc endpoint'i
# -------------------------------
import pandas as pd  # 📌 CSV dosyasını okumak için gerekli

@app.route('/predict-soc', methods=['POST'])
def predict_soc():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'CSV dosyası bulunamadı.'}), 400

        file = request.files['file']
        df = pd.read_csv(file)

        # 📌 Giriş şekli: 50 zaman adımı, 3 özellik (voltage, current, temperature)
        if df.shape != (50, 3):
            return jsonify({'error': 'CSV dosyası 50x3 boyutunda olmalı (50 satır, 3 sütun).'}), 400

        input_sequence = df.to_numpy().reshape(1, 50, 3)
        prediction = soc_model.predict(input_sequence)[0][0]

        return jsonify({'soc': round(float(prediction), 4)})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Ana uygulama çalıştır
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
