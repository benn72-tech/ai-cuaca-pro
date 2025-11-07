import streamlit as st
import requests
import pandas as pd
from sklearn.linear_model import LinearRegression

# Konfigurasi halaman
st.set_page_config(page_title="AI Cuaca Pro+ Animasi", page_icon="🌦️", layout="wide")

# Style dasar
st.markdown("""
<style>
body {
  color: white;
  font-family: 'Segoe UI';
  overflow: hidden;
}
.weather-container {
  position: relative;
  height: 100vh;
  background: linear-gradient(to bottom right, #74b9ff, #81ecec);
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
.sun {
  position: absolute;
  top: 10%;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 100px;
  background: radial-gradient(circle, #f9d71c 60%, #f39c12);
  border-radius: 50%;
  box-shadow: 0 0 30px 10px rgba(255, 223, 0, 0.6);
  animation: spin 20s linear infinite;
}
.cloud {
  position: absolute;
  top: 20%;
  width: 200px;
  height: 60px;
  background: #fff;
  border-radius: 50px;
  animation: moveClouds 25s linear infinite;
}
.cloud:before, .cloud:after {
  content: '';
  position: absolute;
  background: #fff;
  width: 100px;
  height: 80px;
  top: -20px;
  left: 10px;
  border-radius: 50%;
}
.cloud:after {
  width: 120px;
  height: 100px;
  top: -30px;
  left: 80px;
}
.rain {
  position: absolute;
  top: 40%;
  width: 2px;
  height: 15px;
  background: rgba(255,255,255,0.7);
  animation: rainDrop 0.5s linear infinite;
}
@keyframes spin {
  from { transform: translateX(-50%) rotate(0deg); }
  to { transform: translateX(-50%) rotate(360deg); }
}
@keyframes moveClouds {
  from { left: -250px; }
  to { left: 100%; }
}
@keyframes rainDrop {
  0% { transform: translateY(0); opacity: 1; }
  100% { transform: translateY(100vh); opacity: 0; }
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align:center;'>🌤️ AI Cuaca Pro+ with Live Animation</h1>", unsafe_allow_html=True)

# Input kota
city = st.text_input("Masukkan nama kota:", "Jakarta")
api_key = "e342c36c5677da82798e5c28c61c7c54"
base_url = "https://api.openweathermap.org/data/2.5/weather"

# Tombol
if st.button("🌦️ Cek Cuaca Sekarang"):
    if api_key == "MASUKKAN_API_KEY_KAMU_DI_SINI":
        st.warning("⚠️ Masukkan API key kamu dulu di kode.")
    else:
        params = {"q": city, "appid": api_key, "units": "metric", "lang": "id"}
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            suhu = data["main"]["temp"]
            kelembapan = data["main"]["humidity"]
            angin = data["wind"]["speed"]
            kondisi = data["weather"][0]["main"].lower()

            # Tentukan animasi sesuai kondisi cuaca
            if "rain" in kondisi:
                animasi = "<div class='rain' style='left:20%;'></div>"*40
            elif "cloud" in kondisi:
                animasi = "<div class='cloud' style='top:25%; animation-duration:20s;'></div>" \
                          "<div class='cloud' style='top:35%; left:30%; animation-duration:35s;'></div>"
            else:
                animasi = "<div class='sun'></div>"

            # Tampilkan cuaca + animasi
            st.markdown(f"""
            <div class="weather-container">
              {animasi}
              <h2>{city.title()}</h2>
              <h3>{suhu}°C | {kondisi.title()}</h3>
              <p>💧 Kelembapan: {kelembapan}% | 🌬️ Angin: {angin} m/s</p>
            </div>
            """, unsafe_allow_html=True)

            # Prediksi suhu besok pakai AI
            df = pd.DataFrame({
                "suhu": [suhu-3, suhu-2, suhu-1, suhu],
                "kelembapan": [kelembapan+5, kelembapan+2, kelembapan, kelembapan-3],
                "angin": [angin+1, angin, angin-0.5, angin-0.3],
                "besok": [suhu-2, suhu-1, suhu+0.5, suhu+1]
            })

            model = LinearRegression().fit(df[["suhu", "kelembapan", "angin"]], df["besok"])
            prediksi = model.predict([[suhu, kelembapan, angin]])[0]

            st.success(f"🤖 Prediksi suhu besok di {city.title()}: {prediksi:.2f}°C")

        else:
            st.error("❌ Kota tidak ditemukan.")
