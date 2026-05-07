import streamlit as st
from API import get_weather, get_activities

st.set_page_config(page_title="SmartTravel - Dashboard", page_icon="👤")

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

if st.button("Return Home", icon="🏠"):
    st.switch_page("TravelPlannerDemo.py")

if "selected_destination" not in st.session_state:
    st.warning("No destination selected yet!")
    if st.button("Go to Questionnaire"):
        st.switch_page("pages/TravelPlannerQuestionnaire.py")
    st.stop()

destination = st.session_state.selected_destination

st.title("Your Travel Dashboard")
st.header("My Trip Itinerary")

st.header("📅 Trip Overview")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.subheader("Destination:")
    st.write(destination["place"])
with col2:
    travel_duration = 7  # default travel duration if no saved preference exists
    if "preferences" in st.session_state:
        travel_duration = st.session_state.preferences.get("travel_duration", travel_duration)  # read duration from saved preferences if available
    elif "travel_duration" in st.session_state:
        travel_duration = st.session_state.travel_duration  # read duration directly from session state if preferences dict is missing
    st.subheader("Duration:")
    if travel_duration == 1:
        st.write(f"{travel_duration} day")  # display singular day label for a one-day trip
    else:
        st.write(f"{travel_duration} days")  # display plural days label for multi-day trips
with col3:
    st.subheader("Country:")
    st.write(destination["country"])
with col4:
    daily_budget = st.session_state.preferences.get("daily_budget", destination["budget_max"]) if "preferences" in st.session_state else destination["budget_max"]
    total_budget = daily_budget * travel_duration
    st.metric("Daily Budget", f"${daily_budget}")
with col4:
    st.metric("Trip Total Est.", f"${total_budget:,}")

#Weather Section
st.header("🌤️ Current Weather")
weather = get_weather(destination["place"])

if weather:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Temperature", f"{weather['temp']}°C")
    with col2:
        st.metric("Humidity", f"{weather['humidity']}%")
    with col3:
        st.metric("Wind Speed", f"{weather['wind_speed']} m/s")
    with col4:
        st.metric("Conditions", weather['description'].capitalize())
else: 
    st.warning("Weather data unavailable for this destination")

# Daily Itinerary Section
st.header("🗺️ Daily Itinerary")

#this sub-section is AI generated, but not too complicated
if "selected_day" not in st.session_state: # Initialize selected_day in session state if it doesn't exist
    st.session_state.selected_day = 1 # Defaults to Day 1 on initial load

#this sub-section is AI generated, but easy to understand
st.subheader("Select a day")
day_cols = st.columns(travel_duration) # Create x columns for each day of the trip (adjust based on trip duration)
for i, col in enumerate(day_cols, 1):
    with col:
        if st.button(f"Day {i}"):
            st.session_state.selected_day = i # Updates selected_day in session state when a day button is clicked


selected_day = st.session_state.selected_day # Gets the selected day from session state
st.subheader(f"Day {selected_day} schedule")
# Fetch activities based on user preferences and selected destination
activities_prefs = st.session_state.preferences.get("activities", []) if "preferences" in st.session_state else []
travel_pace = st.session_state.preferences.get("travel_pace", "Moderate: Balance of activities and rest") if "preferences" in st.session_state else "Moderate: Balance of activities and rest"

all_activities, per_day = get_activities(destination["place"], activities_prefs, travel_pace, travel_duration) or ([], 3)

offset = (selected_day - 1) * per_day
recommended = all_activities[offset:offset + per_day] if all_activities else []

if recommended:
    for i, activity in enumerate(recommended, 1):
        st.markdown(f""" #Design AI-generated
        <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(192,132,252,0.15);
             border-radius:14px; padding:18px 20px; margin-bottom:12px;">
            <div style="display:flex; gap:16px; align-items:flex-start;">
                <div style="background:rgba(138,43,226,0.3); border-radius:10px;
                      width:36px; height:36px; display:flex; align-items:center;
                      justify-content:center; flex-shrink:0;
                      font-family:'Playfair Display',serif; font-weight:900; color:#f59e0b;">
                    {i}
                </div>
                <div>
                    <div style="font-weight:600; color:#ffffff; font-size:1rem; margin-bottom:4px;">
                        {activity['name']}
                    </div>
                    <div style="color:#c084fc; font-size:0.85rem;">📍 {activity['category']}</div>
                    <div style="color:#9ca3af; font-size:0.82rem; margin-top:2px;">🗺️ {activity['address']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning("No activities found for this destination.")

    
