import streamlit as st
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt

# Sayfa yapılandırması
st.set_page_config(page_title="Battery Health Prediction", layout="wide")


# Özel stil (koyu yeşil + beyaz)
st.markdown("""
<style>
/* Genel arka plan ve içerik rengi */
.block-container {
    background-color: #161E11 !important;
    color: white !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* Üst bar */
header[data-testid="stHeader"] {
    background-color: #161E11 !important;
}

/* Başlık */
.main-title {
    font-size: 3rem !important;
    font-weight: bold !important;
    text-align: center !important;
    margin-bottom: 2rem !important;
}

/* Butonlar */
.stButton > button {
    color: #161E11 !important;
    background-color: white !important;
    font-weight: bold !important;
    border-radius: 5px !important;
    padding: 0.5rem 1rem !important;
}

/* Sağ/sol kutular */
[data-testid="column"] > div {
    background-color: white !important;
    color: #161E11 !important;
    padding: 2rem !important;
    border-radius: 10px !important;
    margin-bottom: 1rem !important;
}

</style>
""", unsafe_allow_html=True)



# Başlık
st.markdown('<div class="main-title">🔋 Battery Health Prediction Dashboard</div>', unsafe_allow_html=True)

# Sayfayı ikiye böl
left, col1, empty, col2, right = st.columns([0.02, 1, 0.08, 1, 0.02])

# ========== SOL: SOH ==========
with col1:
    st.markdown('<div class="column">', unsafe_allow_html=True)
    st.header("📈 SOH Tahmini")

    avg_voltage = st.number_input("🔌 Ortalama Gerilim (V)", value=3.7)
    avg_current = st.number_input("⚡ Ortalama Akım (A)", value=1.5)
    avg_temp = st.number_input("🌡️ Ortalama Sıcaklık (°C)", value=25.0)
    max_temp = st.number_input("🔥 Maksimum Sıcaklık (°C)", value=35.0)

    if st.button("SOH Tahmini Yap"):
        soh_payload = {
            "avg_voltage": avg_voltage,
            "avg_current": avg_current,
            "avg_temperature": avg_temp,
            "max_temperature": max_temp
        }
        response = requests.post("http://localhost:5001/predict-soh", json=soh_payload)

        if response.status_code == 200:
            result = response.json()
            soh_value = result["predicted_soh"]
            st.success(f"🔋 Tahmin Edilen SOH: **{soh_value:.4f}**")

            st.subheader("📊 SOH Tablosu")
            st.table(pd.DataFrame([soh_payload | {"Tahmin SOH": soh_value}]))

        else:
            st.error("Tahmin yapılamadı.")
    st.markdown('</div>', unsafe_allow_html=True)


# ========== SAĞ: SOC ==========
with col2:
    st.markdown('<div class="column">', unsafe_allow_html=True)
    st.header("🔌 SOC Tahmini")

    uploaded_file = st.file_uploader("📄 CSV Yükleyin", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("📋 Veri önizlemesi:")
        st.dataframe(df.head())

        response = requests.post("http://localhost:5001/predict-soc", json={"data": df.to_dict(orient="records")})
        if response.status_code == 200:
            result = response.json()
            predictions = result["predictions"]

            st.success("✅ SOC tahmini tamamlandı!")

            st.subheader("📊 SOC Tablosu")
            result_df = pd.DataFrame({
                "Zaman": df["time"][:len(predictions)],
                "Gerçek SOC": df["soc"][:len(predictions)],
                "Tahmin SOC": predictions
            })
            st.dataframe(result_df.head(20))
        else:
            st.error("SOC tahmini başarısız oldu.")
    st.markdown('</div>', unsafe_allow_html=True)

# Alt bilgi
st.markdown("---")
st.caption("🧪 Demo uygulama - Flask API + Streamlit")
