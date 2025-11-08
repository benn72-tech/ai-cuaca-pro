import streamlit as st
import requests
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime
import plotly.express as px

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

st.set_page_config(page_title="AI Cuaca Pro++", page_icon="🌤️", layout="centered")

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
        footer {{visibility: hidden;}}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# 🧠 Judul Aplikasi
# ---------------------------
st.title("🌦️ AI Cuaca Pro++")
st.caption("Dibuat oleh **Beni Siswanto** — dengan grafik tren suhu 7 hari 📊")

# ---------------------------
# 🌍 Input Kota
# ---------------------------
city = st.text_input("Masukkan nama kota:", "Jakarta")

# ---------------------------
# 🌐 Ambil Data Cuaca Sekarang
# ---------------------------
api_key = "e342c36c5677da82798e5c28c61c7c54"
url_current = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=id"

res_now = requests.get(url_current)

if res_now.status_code == 200:
    data_now = res_now.json()
    suhu = data_now["main"]["temp"]
    deskripsi = data_now["weather"][0]["description"]
    kelembapan = data_now["main"]["humidity"]
    kecepatan_angin = data_now["wind"]["speed"]

    st.subheader(f"🌍 Cuaca Sekarang di {city.title()}")
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
    # 📊 Grafik Prakiraan 7 Hari ke Depan
    # ---------------------------
    st.subheader("📊 Grafik Tren Suhu 7 Hari ke Depan")
    url_forecast = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=id"
    res_forecast = requests.get(url_forecast)

    if res_forecast.status_code == 200:
        data_forecast = res_forecast.json()
        temps = []
        dates = []

        for item in data_forecast["list"][::8]:  # ambil tiap 24 jam (3 jam * 8)
            temps.append(item["main"]["temp"])
            dates.append(item["dt_txt"].split(" ")[0])

        df_forecast = pd.DataFrame({"Tanggal": dates, "Suhu (°C)": temps})
        fig = px.line(
            df_forecast,
            x="Tanggal",
            y="Suhu (°C)",
            markers=True,
            title=f"Perkiraan Suhu Harian di {city.title()}",
            template="plotly_dark" if theme == "dark" else "plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Data prakiraan 7 hari tidak tersedia untuk kota ini.")

    # ---------------------------
    # 🤖 Prediksi AI Suhu
    # ---------------------------
    st.subheader("🤖 Prediksi AI Berdasarkan Kelembapan")
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
