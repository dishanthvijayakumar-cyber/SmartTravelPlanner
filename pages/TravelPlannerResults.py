import streamlit as st
from API import get_weather

st.set_page_config(page_title="SmartTravel - Results", page_icon="🎯")

# Design: AI-generated
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1a0030 0%, #2d0057 40%, #0d001a 100%) !important;
    font-family: 'DM Sans', sans-serif;
    color: #ffffff;
}
[data-testid="stHeader"] { background: transparent !important; }

h1, h2, h3 { font-family: 'Playfair Display', serif !important; }

.stButton > button {
    background: linear-gradient(135deg, #6a0dad, #8a2be2) !important;
    color: white !important; border: none !important;
    border-radius: 50px !important; padding: 0.6rem 2rem !important;
    font-weight: 600 !important; transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(138,43,226,0.4) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(138,43,226,0.6) !important;
}

[data-testid="stMetricValue"] { color: #ffffff !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: #c084fc !important; }
</style>
""", unsafe_allow_html=True)
#end of Design

if "recommendations" not in st.session_state:
    st.warning("Please complete the questionnaire first!")
    if st.button ("Go to Questionnaire"):
        st.switch_page("pages/TravelPlannerQuestionnaire.py")
    st. stop()

if st.button("Return Home", icon="🏠"):
    st.switch_page("TravelPlannerDemo.py")

st.title("🎯 Your Top 10 Destinations")

chart_data = {r["place"]: r["score"] for r in st.session_state.recommendations}
st.bar_chart(chart_data)

for rank, destination in enumerate(st.session_state.recommendations, 1):
    st.subheader(f"#{rank} - {destination['place']} - {destination['score']}/100")
    st.image(f"https://en.wikipedia.org/wiki/Special:FilePath/{destination['place']}.jpg", width=300)
    st.write(f"🌍 {destination['country']} | 🌤️ {destination['climate']}")
    st.write(f"📖 {destination['description_sentence']}")
    weather = get_weather(destination["place"])
    if weather: 
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Temperature", str(weather["temp"]) + "°C")
        with col2:
            st.metric("Humidity", str(weather["humidity"]) + "%")
        with col3:
            st.metric("Wind Speed", str(weather["wind_speed"]) + "m/s")  
        with col4:
            st.metric("Conditions", weather["description"].capitalize())

    if st.button(f"Plan this trip", key=f"btn_{rank}"):
        st.session_state.selected_destination = destination
        st.switch_page("pages/TravelPlannerDashboard.py")
    
    st.markdown("---")
