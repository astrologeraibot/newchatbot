import streamlit as st
import swisseph as swe
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import math

# Set path to Swiss Ephemeris data (your "ephe" folder)
swe.set_ephe_path("ephe")

st.title("🪐 Natal (Birth) Chart Generator - Offline")

# --- FORM INPUTS ---
name = st.text_input("Your Name")
birth_date = st.date_input("Birth Date")
birth_time = st.time_input("Birth Time")

@st.cache_data
def load_city_data():
    return pd.read_excel("worldcities.csv")  # You uploaded this file earlier

cities_df = load_city_data()

# Place of birth input (manual)
place_input = st.text_input("Enter your Place of Birth (City Name)")

# Check if city exists
lat = None
lng = None
if place_input:
    match = cities_df[cities_df['city'].str.lower() == place_input.lower()]
    if not match.empty:
        city = match.iloc[0]
        lat = city["lat"]
        lng = city["lng"]
        st.success(f"Found: {city['city']}, {city['country']} (Lat: {lat}, Lng: {lng})")
    else:
        st.warning("City not found in dataset.")

# --- GENERATE BUTTON ---
if st.button("Generate Natal Chart"):
    if lat is None or lng is None:
        st.error("Please enter a valid city name.")
    else:
        # Compute Julian Day
        dt = datetime.datetime.combine(birth_date, birth_time)
        jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60)

        # Define planets
        planets = {
            0: "Sun", 1: "Moon", 2: "Mercury", 3: "Venus",
            4: "Mars", 5: "Jupiter", 6: "Saturn",
            7: "Uranus", 8: "Neptune", 9: "Pluto"
        }

        sign_names = ['♈ Aries', '♉ Taurus', '♊ Gemini', '♋ Cancer', '♌ Leo',
                      '♍ Virgo', '♎ Libra', '♏ Scorpio', '♐ Sagittarius', '♑ Capricorn',
                      '♒ Aquarius', '♓ Pisces']

        st.subheader(f"🌌 Planetary Positions for {name}")
        positions = []

        for pid in planets.keys():
            result, _ = swe.calc_ut(jd, pid)
            lon, lat_, dist = result
            sign = int(lon // 30)
            positions.append((planets[pid], lon, sign_names[sign]))
            st.write(f"🌟 {planets[pid]}: {lon:.2f}° in {sign_names[sign]}")

        # --- DRAW NATAL CHART ---
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_aspect('equal')
        ax.axis('off')

        # Draw zodiac circle
        circle = plt.Circle((0, 0), 1, color='black', fill=False)
        ax.add_artist(circle)

        for i in range(12):
            angle = i * 30 * math.pi / 180
            x = [0, math.cos(angle)]
            y = [0, math.sin(angle)]
            ax.plot(x, y, color='gray')

        # Draw planets
        for planet, deg, sign in positions:
            angle_rad = (360 - deg + 90) % 360 * math.pi / 180
            x = 0.85 * math.cos(angle_rad)
            y = 0.85 * math.sin(angle_rad)
            ax.text(x, y, planet[0], ha='center', va='center', fontsize=10, color='blue')

        st.pyplot(fig)
