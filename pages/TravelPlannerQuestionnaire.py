import streamlit as st
st.set_page_config(page_title="SmartTravel - Questionnaire", page_icon="❓")

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


#AI-generated
import sys
sys.path.append('..')
from recommender import get_recommendations

#TravelPlanner Questionnaire
#Everything Here is just for testing purposes
# Questions and Answers SHOULD BE CHANGED based on Imported Databases

if st.button("Return Home", icon="🏠"):
    st.switch_page("TravelPlannerDemo.py")

st.title("Travel Planner Questionnaire")
st.subheader("Welcome to the Travel Planner Questionnaire! Please answer the following questions to help us plan your perfect trip.")

#selectboxes Travel Style
st.subheader("1. Travel Style")
tools = ["Luxury Traveler: Premium Experiences & Accommodations", "Adventure Seeker: Thrilling Activities & Outdoor Exploration", "Cultural Explorer: History, Art & Local Traditions", "Relaxation Focused: Beach Resorts & Peaceful Retreats", "Budget Backpacker: Affordable Travel & Authentic Experiences"]
if "preferences" in st.session_state and "travel_style" in st.session_state.preferences:  # check if travel style was previously saved in preferences
    default_travel_style = st.session_state.preferences["travel_style"]  # use the saved travel style from preferences
else:
    default_travel_style = tools[0]  # otherwise use the existing first option as default
travel_style = st.selectbox("What's your travel style?", tools, index=tools.index(default_travel_style) if default_travel_style in tools else 0, key="travel_style")  # restore saved travel style or use the existing default


# Multiselect Travel Interests
st.subheader("2. Your Travel Interests")
interest_options = [
    "Photography",
    "Food & Cuisine",
    "Wildlife",
    "Architecture",
    "Beaches",
    "Mountains",
    "History",
    "Nightlife",
    "Shopping", 
    "Art & Museums",
    "Hiking",
    "Water Sports",
]
if "preferences" in st.session_state and "interests" in st.session_state.preferences:  # check if interests were previously saved in preferences
    default_selected_interests = st.session_state.preferences["interests"]  # use the saved interests list from preferences
else:
    default_selected_interests = []  # otherwise start with empty selection
selected_interests = st.multiselect("Select all that apply", interest_options, default=default_selected_interests, key="selected_interests")  # restore existing interests or use existing default
for interest in selected_interests:
    st.write(f"- {interest}")


#Slider Daily Budget
st.subheader("3. What's your daily budget?")
if "preferences" in st.session_state and "daily_budget" in st.session_state.preferences:  # check if daily budget was previously saved in preferences
    default_daily_budget = st.session_state.preferences["daily_budget"]  # use the saved daily budget from preferences
else:
    default_daily_budget = 50  # otherwise use the existing default value
daily_budget = st.slider("Per Person, including accomodation", min_value=0, max_value=1000, step=10, value=default_daily_budget, key="daily_budget")  # restore saved budget or use existing default
st.write(f"Your daily budget is: ${daily_budget}")


#selectboxes Ideal Climate
st.subheader("4. Ideal Climate")
climates = ["Tropical", "Temperate", "Cold", "Desert"]
if "preferences" in st.session_state and "ideal_climate" in st.session_state.preferences:  # check if climate choice was previously saved in preferences
    default_climate = st.session_state.preferences["ideal_climate"]  # use the saved climate choice from preferences
else:
    default_climate = climates[0]  # otherwise use the existing first option
ideal_climate = st.selectbox("Choose your preferred weather", climates, index=climates.index(default_climate) if default_climate in climates else 0, key="ideal_climate")  # restore saved climate or existing default

#Selectboxes Travel Pace
st.subheader("5. Your Travel Pace")
travel_pace_options = ["Relaxed: Take it slow, enjoy each moment", "Moderate: Balance of activities and rest", "Packed: See and do as much as possible"]
if "preferences" in st.session_state and "travel_pace" in st.session_state.preferences:  # check if travel pace was previously saved in preferences
    default_travel_pace = st.session_state.preferences["travel_pace"]  # use the saved travel pace from preferences
else:
    default_travel_pace = travel_pace_options[0]  # otherwise use the existing first option
travel_pace = st.selectbox("How do you like to experience destinations?", travel_pace_options, index=travel_pace_options.index(default_travel_pace) if default_travel_pace in travel_pace_options else 0, key="travel_pace")  # restore saved travel pace or existing default

#Selectboxes Travel Accommodation
st.subheader("6. Your Travel Accommodation")
accomodation_options = ["Luxury Hotels", "Mid-range Hotels", "Budget Hotels", "Cabins", "Camping", "Hostels", "Vacation Rentals (Airbnb, etc.)", "Boutique Hotels", "Resorts", "Bed & Breakfasts"]
if "preferences" in st.session_state and "accommodation" in st.session_state.preferences:  # check if accommodation choices were previously saved in preferences
    default_accommodation = st.session_state.preferences["accommodation"]  # use the saved accommodation list from preferences
else:
    default_accommodation = []  # otherwise use an empty default list
accommodation = st.multiselect("What type of accommodations do you like most?", accomodation_options, default=default_accommodation, key="accommodation")  # restore saved accommodations or existing default
for accomodation in accommodation:
    st.write(f"- {accomodation}")

#Selectboxes Activities
st.subheader("7. Your Preferred Activities")
activities_options = ["City Tours", "Nature Hikes", "Cultural Experiences (Museums, Local Events)", "Adventure Activities (Ziplining, Rafting)", "Relaxation (Spas, Beach Days)", "Food & Drink Experiences (Cooking Classes, Wine Tasting)", "Nightlife (Bars, Clubs)", "Shopping", "Wildlife Encounters", "Historical Sites"]
if "preferences" in st.session_state and "activities" in st.session_state.preferences:  # check if activities were previously saved in preferences
    default_activities = st.session_state.preferences["activities"]  # use the saved activities list from preferences
else:
    default_activities = []  # otherwise use an empty default list
activities = st.multiselect("What activities do you enjoy most while traveling?", activities_options, default=default_activities, key="activities")  # restore saved activities or existing default
for activity in activities:
    st.write(f"- {activity}")

#Slider Travel Duration
st.subheader("8. How long would you stay?")
if "preferences" in st.session_state and "travel_duration" in st.session_state.preferences:  # check if travel duration was previously saved in preferences
    default_travel_duration = st.session_state.preferences["travel_duration"]  # use the saved duration from preferences
else:
    default_travel_duration = 20  # otherwise use the existing default duration
travel_duration = st.slider("Days", min_value=0, max_value=365, step=1, value=default_travel_duration, key="travel_duration")  # restore saved duration or existing default
st.write(f"Your stay would last: {travel_duration} days")


#add spacing between buttons and stats with 150px distance (AI generated)
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)

#AI-generated
if st.button("View Results✔️"):
    st.session_state.preferences = {  # store all questionnaire answers in session state under preferences
        "travel_style": travel_style,  # save selected travel style to preferences
        "ideal_climate": ideal_climate,  # save preferred climate to preferences
        "interests": selected_interests,  # save chosen interests to preferences
        "daily_budget": daily_budget,  # save daily budget value to preferences
        "activities": activities,  # save selected activities to preferences
        "accommodation": accommodation,  # save selected accommodation types to preferences
        "travel_pace": travel_pace,  # save chosen travel pace to preferences
        "travel_duration": travel_duration,  # save chosen trip duration to preferences
    }
    st.session_state.recommendations = get_recommendations(st.session_state.preferences)  # generate recommendation list from saved preferences
    st.switch_page("pages/TravelPlannerResults.py")  # navigate to the results page after saving preferences
