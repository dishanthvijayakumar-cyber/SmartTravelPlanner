import streamlit as st
st.set_page_config(page_title="SmartTravel - Questionnaire", page_icon="❓")

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
travel_style = st.selectbox("What's your travel style?", tools)


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
selected_interests = st.multiselect("Select all that apply", interest_options)
for interest in selected_interests:
    st.write(f"- {interest}")


#Slider Daily Budget
st.subheader("3. What's your daily budget?")
daily_budget = st.slider("Per Person, including accomodation", min_value=0, max_value=1000, step=10, value=50)
st.write(f"Your daily budget is: ${daily_budget}")


#selectboxes Ideal Climate
st.subheader("4. Ideal Climate")
climates = ["Tropical", "Temperate", "Cold", "Desert"]
ideal_climate = st.selectbox("Choose your preferred weather", climates)

#Selectboxes Travel Pace
st.subheader("5. Your Travel Pace")
travel_pace = ["Relaxed: Take it slow, enjoy each moment", "Moderate: Balance of activities and rest", "Packed: See and do as much as possible"]
travel_pace = st.selectbox("How do you like to experience destinations?", travel_pace)

#Selectboxes Travel Accommodation
st.subheader("6. Your Travel Accommodation")
accomodation_options = ["Luxury Hotels", "Mid-range Hotels", "Budget Hotels", "Cabins", "Camping", "Hostels", "Vacation Rentals (Airbnb, etc.)", "Boutique Hotels", "Resorts", "Bed & Breakfasts"]

accommodation = st.multiselect("What type of accommodations do you like most?", accomodation_options) 
for accomodation in accommodation:
    st.write(f"- {accomodation}")

#Selectboxes Activities
st.subheader("7. Your Preferred Activities")
activities_options = ["City Tours", "Nature Hikes", "Cultural Experiences (Museums, Local Events)", "Adventure Activities (Ziplining, Rafting)", "Relaxation (Spas, Beach Days)", "Food & Drink Experiences (Cooking Classes, Wine Tasting)", "Nightlife (Bars, Clubs)", "Shopping", "Wildlife Encounters", "Historical Sites"]
activities = st.multiselect("What activities do you enjoy most while traveling?", activities_options)
for activity in activities:
    st.write(f"- {activity}")

#Slider Travel Duration
st.subheader("8. How long would you stay?")
travel_duration = st.slider("Days", min_value=0, max_value=365, step=10, value=1)
st.write(f"Your stay would last: {travel_duration} days")


#add spacing between buttons and stats with 150px distance (AI generated)
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)

#AI-generated
if st.button("View Results✔️"):
    st.session_state.preferences = { 
        "travel_style": travel_style,
        "ideal_climate": ideal_climate,
        "interests": selected_interests,
        "daily_budget": daily_budget,
        "activities": activities,
        "accommodation": accommodation,
        "travel_pace": travel_pace,
    }
    st.session_state.recommendations = get_recommendations(st.session_state.preferences)
    st.switch_page("pages/TravelPlannerResults.py")
