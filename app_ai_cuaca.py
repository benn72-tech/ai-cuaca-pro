import streamlit as st
import requests
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime

# ---------------------------
# 🌗 Tema Otomatis Berdasarkan Waktu
# ---------------------------
current_hour = datetime.now().hour
if 6 <= current_hour < 18:
    theme = "light"
    bg_color = "#f7f9fc"
    text_color = "#1a1a1a"
else:
    theme = "dark"
    bg_color = "#0e1117"
    text_color = "#fafafa"

st.set_page_config(page_title="AI Cuaca Pro+ 🌦️", page_icon="🌤️", layout="centered")

# ---------------------------
# 🌟 Custom CSS untuk Tema
# ---------------------------
st.markdown(
    f"""
    <style>
        body {{
            background-color: {bg_color};
            color: {text_color};
            font-family: 'Segoe UI', sans-serif;
        }}
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        .stTextInput > div > div > input {{
            background-color: #1c1f26 if theme == "dark" else #ffffff;
            color: {text_color};
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {text_color};
        }}
        footer {{
            visibility: hidden;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# 🧠 Judul Aplikasi
# ---------------------------
st.title("🌦️ AI Cuaca Pro+")
st.caption("Dibuat oleh **Beni Siswanto** — dengan mode gelap otomatis ✨")

# ---------------------------
# 🌍 Input Kota
# ---------------------------
city = st.text_input("Masukkan nama kota:", "Jakarta")

# ---------------------------
# 🌐 Ambil Data Cuaca
# ---------------------------
api_key = "e342c36c5677da82798e5c28c61c7c54"
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=id"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    suhu = data["main"]["temp"]
    deskripsi = data["weather"][0]["description"]
    kelembapan = data["main"]["humidity"]
    kecepatan_angin = data["wind"]["speed"]

    st.subheader(f"🌍 Cuaca di {city.title()}")
    st.write(f"**Deskripsi:** {deskripsi.capitalize()}")
    st.write(f"🌡️ **Suhu:** {suhu}°C")
    st.write(f"💧 **Kelembapan:** {kelembapan}%")
    st.write(f"💨 **Kecepatan Angin:** {kecepatan_angin} m/s")

    # ---------------------------
    # 🌦️ Animasi Cuaca
    # ---------------------------
    if "hujan" in deskripsi.lower():
        st.image("https://i.gifer.com/7scX.gif", caption="Hujan 🌧️", use_container_width=True)
    elif "awan" in deskripsi.lower():
        st.image("https://i.gifer.com/VgFi.gif", caption="Berawan ☁️", use_container_width=True)
    elif "cerah" in deskripsi.lower() or "clear" in deskripsi.lower():
        st.image("https://i.gifer.com/3M79.gif", caption="Cerah ☀️", use_container_width=True)
    else:
        st.image("https://i.gifer.com/5eKX.gif", caption="Cuaca tidak menentu 🌈", use_container_width=True)

    # ---------------------------
    # 🤖 Prediksi AI
    # ---------------------------
    st.subheader("🤖 Prediksi Suhu oleh AI")
    data_latih = pd.DataFrame({
        "kelembapan": [30, 40, 50, 60, 70, 80, 90],
        "suhu": [33, 32, 31, 29, 27, 26, 25]
    })

    X = data_latih[["kelembapan"]]
    y = data_latih["suhu"]

    model = LinearRegression()
    model.fit(X, y)

    suhu_prediksi = model.predict(np.array([[kelembapan]]))[0]
    st.write(f"🤖 Berdasarkan AI, suhu diperkirakan: **{suhu_prediksi:.1f}°C**")

    waktu = datetime.now().strftime("%d %B %Y, %H:%M:%S")
    st.caption(f"⏰ Data diperbarui: {waktu}")

else:
    st.error("❌ Kota tidak ditemukan atau API key salah. Silakan cek kembali.")
