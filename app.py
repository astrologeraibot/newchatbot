import streamlit as st
import swisseph as swe
import datetime
import matplotlib.pyplot as plt
import os
import pandas as pd

# Set the path to the Swiss Ephemeris data
swe.set_ephe_path("ephe")

st.title("🪐 Natal (Birth) Chart Generator - Offline")

# Form inputs
name = st.text_input("Your Name")
birth_date = st.date_input("Birth Date")
birth_time = st.time_input("Birth Time")

if st.button("Generate Natal Chart"):
    # Convert to Julian Day
    dt = datetime.datetime.combine(birth_date, birth_time)
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60)

    # Calculate positions
    planets = {
        0: "Sun", 1: "Moon", 2: "Mercury", 3: "Venus",
        4: "Mars", 5: "Jupiter", 6: "Saturn",
        7: "Uranus", 8: "Neptune", 9: "Pluto"
    }

    st.subheader(f"Planetary Positions for {name}")
    positions = []

    for pid in planets.keys():
        lon, lat_, dist = swe.calc_ut(jd, pid)[0]
        sign = int(lon // 30)
        sign_names = ['♈ Aries', '♉ Taurus', '♊ Gemini', '♋ Cancer', '♌ Leo',
                      '♍ Virgo', '♎ Libra', '♏ Scorpio', '♐ Sagittarius', '♑ Capricorn',
                      '♒ Aquarius', '♓ Pisces']
        positions.append((planets[pid], lon, sign_names[sign]))
        st.write(f"🌟 {planets[pid]}: {lon:.2f}° in {sign_names[sign]}")

    # Plot simple natal wheel
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')

    # Draw circle and zodiac lines
    circle = plt.Circle((0, 0), 1, color='black', fill=False)
    ax.add_artist(circle)
    for i in range(12):
        angle = i * 30
        x = [0, 1 * swe.cos(angle)]
        y = [0, 1 * swe.sin(angle)]
        ax.plot(x, y, color='gray')

    # Plot planet positions
    for planet, deg, sign in positions:
        angle_rad = (360 - deg + 90) % 360 * 3.14159 / 180
        x = 0.8 * swe.cos(angle_rad)
        y = 0.8 * swe.sin(angle_rad)
        ax.text(x, y, planet[0], ha='center', va='center', fontsize=10, color='blue')

    st.pyplot(fig)

@st.cache_data
def load_city_data():
    return pd.read_csv("worldcities.csv")

cities_df = load_city_data()
selected_city = st.selectbox("Choose your city", cities_df["city"].unique())
