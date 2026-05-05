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

#Chart top 10 destinations
import pandas as pd

sorted_recs = sorted(st.session_state.recommendations, key=lambda x: x["score"], reverse=True)

chart_data = pd.DataFrame({
    "Score": [r["score"] for r in sorted_recs]
}, index=[r["place"] for r in sorted_recs])

st.bar_chart(chart_data, color="#8a2be2") #Design: AI-generated 

#(Design AI-generated)
for rank, destination in enumerate(st.session_state.recommendations, 1):
    score = destination["score"]
    score_color = "#34d399" if score >= 70 else "#f59e0b" if score >= 40 else "#f87171"

    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.05); border:1px solid rgba(192,132,252,0.2);
         border-radius:20px; padding:28px; margin-bottom:8px;">
        <div style="display:flex; align-items:center; gap:16px; margin-bottom:16px; flex-wrap:wrap;">
            <span style="font-family:'Playfair Display',serif; font-size:2rem;
                  font-weight:900; color:rgba(255,255,255,0.2);">#{rank}</span>
            <div style="flex:1;">
                <h3 style="font-family:'Playfair Display',serif; font-size:1.5rem;
                      color:#ffffff; margin:0;">{destination['place']}</h3>
                <p style="color:#c084fc; margin:0; font-size:0.9rem;">
                    🌍 {destination['country']} &nbsp;·&nbsp; 🌤️ {destination['climate']}
                </p>
            </div>
            <div style="background:rgba(255,255,255,0.08); border:1px solid {score_color}50;
                  border-radius:16px; padding:10px 20px; text-align:center;">
                <div style="font-family:'Playfair Display',serif; font-size:1.6rem;
                      font-weight:900; color:{score_color};">{score}</div>
                <div style="font-size:0.7rem; color:#9ca3af; letter-spacing:1px;">/ 100</div>
            </div>
        </div>
        <p style="color:#d8b4fe; font-size:0.9rem; margin:0; font-weight:300;">
            {destination['description_sentence']}
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.image(f"https://en.wikipedia.org/wiki/Special:FilePath/{destination['place']}.jpg", width=300)
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

    col_l, col_btn, col_r = st.columns([2, 2, 2])
    with col_btn:
        if st.button(f"🗺️  Plan this trip", key=f"btn_{rank}", use_container_width=True):
            st.session_state.selected_destination = destination
            st.switch_page("pages/TravelPlannerDashboard.py")
    
    st.markdown("---")
