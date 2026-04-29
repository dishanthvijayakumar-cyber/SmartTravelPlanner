import streamlit as st
from API import get_weather

st.set_page_config(page_title="SmartTravel - Results", page_icon="🎯")

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
