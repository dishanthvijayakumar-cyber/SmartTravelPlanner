import streamlit as st
from API import get_weather, get_activities #imports from API module to get weather and activity data for the dashboard

st.set_page_config(page_title="SmartTravel - Dashboard", page_icon="👤") #sets a tab title and icon

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

if st.button("Return Home", icon="🏠"): #creates return home button with an icon
    st.switch_page("TravelPlannerDemo.py") #switches to the home page when the button is clicked

if "selected_destination" not in st.session_state: #check if a destination has been selected in the session state, 
    st.warning("No destination selected yet!") # if not, show a warning
    if st.button("Go to Questionnaire"): #and a button to go to the questionnaire page
        st.switch_page("pages/TravelPlannerQuestionnaire.py") #switches to the questionnaire page when the button is clicked
    st.stop() #stops the rest of the dashboard from loading if no destination is selected

destination = st.session_state.selected_destination #gets the selected destination from session state (set in the questionnaire page) and stores it in destination variable for use in the dashboard

st.title("Your Travel Dashboard") #sets dashboard title
st.header("My Trip Itinerary") #sets dashboard subtitle as header

st.header("📅 Trip Overview") #sets another subtitle
col1, col2, col3, col4 = st.columns(4) #sets four columns for the trip overview
with col1: #defines column 1 content
    st.subheader("Destination:")
    st.write(destination["place"])
with col2: #defines column 2 content
    travel_duration = 7  # default travel duration if no saved preference exists
    if "preferences" in st.session_state: #check if preferences exists in session state (set in questionnaire page)
        travel_duration = st.session_state.preferences.get("travel_duration", travel_duration)  # read duration from saved preferences if available
    elif "travel_duration" in st.session_state: #if preferences is missing, check if travel_duration exists directly in session state and read from there
        travel_duration = st.session_state.travel_duration  # reads duration directly from session state if preferences is missing
    st.subheader("Duration:") #sets a duration subheader within column 2
    if travel_duration == 1: # if the trip duration is 1 day,
        st.write(f"{travel_duration} day")  # display singular day label for a one-day trip
    else: #if travel is multiple days
        st.write(f"{travel_duration} days")  # display plural days label for multi-day trips
with col3: #defines column 3 content
    st.subheader("Country:")
    st.write(destination["country"]) #displays the country of the selected destination (read from session state) in column 3 under a country subheader
with col4: #defines column 4 content
    daily_budget = st.session_state.preferences.get("daily_budget", destination["budget_max"]) if "preferences" in st.session_state else destination["budget_max"] # gets the daily budget from user preferences if it exists, otherwise uses the destination's max budget as a default
    total_budget = daily_budget * travel_duration #calculates the total trip budget 
    st.metric("Daily Budget", f"${daily_budget}") #displays the daily budget in column 4 under a metric component, formatted as the budget with a dollar sign
with col4: #adds on to the bottom of column 4 to show the total trip budget
    st.metric("Trip Total Est.", f"${total_budget:,}") #displays the total trip budget in column 4 under a metric component, formatted as the total budget with a dollar sign and comma separators for thousands

#Weather Section
st.header("🌤️ Current Weather")
weather = get_weather(destination["place"]) #gets the weather for the selected destination using the get_weather function from the API module, giving the place name from the selected destination stored in session state. Saved in weather variable for use in dashboard

if weather:
    col1, col2, col3, col4 = st.columns(4) #creates four columns to display different weather metrics
    with col1: #defines column 1 content
        st.metric("Temperature", f"{weather['temp']}°C") # displays the temperature in column 1 under a metric component, formatted as the temperature with a degree Celsius symbol
    with col2: #defines column 2 content
        st.metric("Humidity", f"{weather['humidity']}%") # displays the humidity in column 2 under a metric component, formatted as the humidity with a percentage symbol
    with col3: #defines column 3 content
        st.metric("Wind Speed", f"{weather['wind_speed']} m/s") # displays the wind speed in column 3 under a metric component, formatted as the wind speed with m/s for meters per second
    with col4: #defines column 4 content
        st.metric("Conditions", weather['description'].capitalize()) # displays the weather conditions in column 4 under a metric component, with the description text capitalized for better formatting
else: 
    st.warning("Weather data unavailable for this destination") # if the weather variable is empty or none, shows a warning that weather data is unavailable for the destination

# Daily Itinerary Section
st.header("🗺️ Daily Itinerary")

if "selected_day" not in st.session_state: # checks if selected_day exists in session state
    st.session_state.selected_day = 1 # Defaults to Day 1 on initial load if no day has been selected yet + saves this default value in session state

st.subheader("Select a day")
day_cols = st.columns(travel_duration) # Create x columns for each day of the trip (adjusts based on trip duration)
for i, col in enumerate(day_cols, 1): # Loops through each day column and create a button for it, starting the index at 1 for user-friendly day numbering
    with col: #defines content for each day column
        if st.button(f"Day {i}"): #creates a button for each day with the label "Day X" where X is the day number, and when clicked
            st.session_state.selected_day = i # Updates selected_day in session state when a day button is clicked

selected_day = st.session_state.selected_day # Gets the selected day from session state
st.subheader(f"Day {selected_day} schedule") # Displays a subheader for the selected day, showing "Day X schedule" where X is the selected day number

# Fetch activities based on user preferences and selected destination
activities_prefs = st.session_state.preferences.get("activities", []) if "preferences" in st.session_state else []
travel_pace = st.session_state.preferences.get("travel_pace", "Moderate: Balance of activities and rest") if "preferences" in st.session_state else "Moderate: Balance of activities and rest"

all_activities, per_day = get_activities(destination["place"], travel_pace) or ([], 3)

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

    
