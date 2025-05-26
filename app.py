import streamlit as st
import requests

st.set_page_config(page_title="Free Astrology Bot", page_icon="🔮")
st.title("🔮 Astrology Horoscope Chatbot")

st.markdown("Ask about your zodiac sign to get your daily horoscope!")

zodiac_signs = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
]

sign = st.selectbox("Choose your zodiac sign:", zodiac_signs)

if st.button("Get Horoscope"):
    with st.spinner("Consulting the stars..."):
        url = f"https://aztro.sameerkumar.website/?sign={sign}&day=today"
        response = requests.post(url)
        if response.status_code == 200:
            data = response.json()
            st.subheader(f"✨ Today's Horoscope for {sign.capitalize()}")
            st.write(data['description'])
            st.info(f"⭐ Lucky Number: {data['lucky_number']}")
            st.info(f"❤️ Compatibility: {data['compatibility']}")
            st.info(f"💡 Mood: {data['mood']}")
        else:
            st.error("Failed to fetch horoscope. Please try again.")
