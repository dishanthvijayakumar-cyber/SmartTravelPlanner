import streamlit as st #importing streamlit library for building the web app as st shortcut
st.set_page_config(page_title="SmartTravel - Questionnaire", page_icon="❓") #configures tab title and icon for the web app

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

/* Input & selectbox text */
[data-testid="stSelectbox"] label,
[data-testid="stMultiSelect"] label,
[data-testid="stSlider"] label {
    color: #ffffff !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
}

/* Selectbox dropdown text */
[data-testid="stSelectbox"] div[data-baseweb="select"] span {
    color: #ffffff !important;
}

/* Multiselect text */
[data-testid="stMultiSelect"] div[data-baseweb="select"] span {
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)




if st.button("Return Home", icon="🏠"): #adds return home button with house icon
    st.switch_page("TravelPlannerDemo.py") #switches page to the home page when button is clicked

st.title("Travel Planner Questionnaire") #adds the main title of the page
st.subheader("Welcome to the Travel Planner Questionnaire! Please answer the following questions to help us plan your perfect trip.") #adds a subheader with instructions for the questionnaire

#selectboxes Travel Style
st.subheader("1. Travel Style")
tools = ["Luxury Traveler: Premium Experiences & Accommodations", "Adventure Seeker: Thrilling Activities & Outdoor Exploration", "Cultural Explorer: History, Art & Local Traditions", "Relaxation Focused: Beach Resorts & Peaceful Retreats", "Budget Backpacker: Affordable Travel & Authentic Experiences"]
if "preferences" in st.session_state and "travel_style" in st.session_state.preferences:  # check if travel style was previously saved in preferences
    default_travel_style = st.session_state.preferences["travel_style"]  # use the saved travel style from preferences if it exists
else:
    default_travel_style = tools[0]  # otherwise use the placeholder (value 0 in tools list) as default
travel_style = st.selectbox("What's your travel style?", tools, index=tools.index(default_travel_style) if default_travel_style in tools else 0, key="travel_style")  # creates selectbox for travel style with options from tools list, sets default selection based on saved preferences or existing default, and assigns selected value to travel_style variable


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
] #list of travel interest options for the multiselect component
if "preferences" in st.session_state and "interests" in st.session_state.preferences:  # check if interests were previously saved in preferences
    default_selected_interests = st.session_state.preferences["interests"]  # use the saved interests list from preferences if the interests were previously saved
else:
    default_selected_interests = []  # otherwise start with empty selection
selected_interests = st.multiselect("Select all that apply", interest_options, default=default_selected_interests, key="selected_interests")  # creates multiselect component for travel interests with options from interest_options list, sets default selection based on saved preferences or existing default, and assigns selected values to selected_interests variable
for interest in selected_interests: #iterates through the list of selected interests
    st.write(f"- {interest}") #lists the selected interests below the multiselect component with a dash in front of each interest


#Slider Daily Budget
st.subheader("3. What's your daily budget?")
if "preferences" in st.session_state and "daily_budget" in st.session_state.preferences:  # check if daily budget was previously saved in preferences
    default_daily_budget = st.session_state.preferences["daily_budget"]  # use the saved daily budget from preferences if it exists
else:
    default_daily_budget = 50  # otherwise use the existing default value
daily_budget = st.slider("Per Person, including accomodation", min_value=0, max_value=1000, step=10, value=default_daily_budget, key="daily_budget")  # creates a slider for daily budget with a range from 0 to 1000, step of 10, and default value based on saved preferences or existing default, then assigns the selected value to daily_budget variable
st.write(f"Your daily budget is: ${daily_budget}") #writes the selected daily budget below the slider with a dollar sign in front of it


#selectboxes Ideal Climate
st.subheader("4. Ideal Climate")
climates = ["Tropical", "Temperate", "Cold", "Desert"]
if "preferences" in st.session_state and "ideal_climate" in st.session_state.preferences:  # check if climate choice was previously saved in preferences
    default_climate = st.session_state.preferences["ideal_climate"]  # use the saved climate choice from preferences if it exists
else:
    default_climate = climates[0]  # otherwise use the existing first option
ideal_climate = st.selectbox("Choose your preferred weather", climates, index=climates.index(default_climate) if default_climate in climates else 0, key="ideal_climate")  # creates a selectbox for ideal climate with options from the climates list, default value based on saved preferences or existing default, then assigns the selected value to ideal_climate variable

#Selectboxes Travel Pace
st.subheader("5. Your Travel Pace")
travel_pace_options = ["Relaxed: Take it slow, enjoy each moment", "Moderate: Balance of activities and rest", "Packed: See and do as much as possible"]
if "preferences" in st.session_state and "travel_pace" in st.session_state.preferences:  # check if travel pace was previously saved in preferences
    default_travel_pace = st.session_state.preferences["travel_pace"]  # use the saved travel pace from preferences if it exists
else:
    default_travel_pace = travel_pace_options[0]  # otherwise use the existing first option
travel_pace = st.selectbox("How do you like to experience destinations?", travel_pace_options, index=travel_pace_options.index(default_travel_pace) if default_travel_pace in travel_pace_options else 0, key="travel_pace")  # creates a selectbox for travel pace with options from the travel_pace_options list, default value based on saved preferences or existing default, then assigns the selected value to travel_pace variable

#Selectboxes Travel Accommodation
st.subheader("6. Your Travel Accommodation")
accomodation_options = ["Luxury Hotels", "Mid-range Hotels", "Budget Hotels", "Cabins", "Camping", "Hostels", "Vacation Rentals (Airbnb, etc.)", "Boutique Hotels", "Resorts", "Bed & Breakfasts"]
if "preferences" in st.session_state and "accommodation" in st.session_state.preferences:  # check if accommodation choices were previously saved in preferences
    default_accommodation = st.session_state.preferences["accommodation"]  # use the saved accommodation list from preferences if it exists
else:
    default_accommodation = []  # otherwise use an empty default list
accommodation = st.multiselect("What type of accommodations do you like most?", accomodation_options, default=default_accommodation, key="accommodation")  # creates a multiselect for accommodation with options from the accomodation_options list, default value based on saved preferences or existing default, then assigns the selected values to accommodation variable
for accomodation in accommodation: #iterates through the list of selected accommodation types
    st.write(f"- {accomodation}") #lists the selected accommodation types below the multiselect component with a dash in front of each type

#Selectboxes Activities
st.subheader("7. Your Preferred Activities")
activities_options = ["City Tours", "Nature Hikes", "Cultural Experiences (Museums, Local Events)", "Adventure Activities (Ziplining, Rafting)", "Relaxation (Spas, Beach Days)", "Food & Drink Experiences (Cooking Classes, Wine Tasting)", "Nightlife (Bars, Clubs)", "Shopping", "Wildlife Encounters", "Historical Sites"]
if "preferences" in st.session_state and "activities" in st.session_state.preferences:  # check if activities were previously saved in preferences
    default_activities = st.session_state.preferences["activities"]  # use the saved activities list from preferences if it exists
else:
    default_activities = []  # otherwise use an empty default list
activities = st.multiselect("What activities do you enjoy most while traveling?", activities_options, default=default_activities, key="activities")  # creates a multiselect for activities with options from the activities_options list, default value based on saved preferences or existing default, then assigns the selected values to activities variable
for activity in activities: #iterates through the list of selected activities
    st.write(f"- {activity}") #lists the selected activities below the multiselect component with a dash in front of each activity

#Slider Travel Duration
st.subheader("8. How long would you stay?")

duration_options = [1, 2, 3, 4, 5, 6, 7, 10, 14] #the different duration options in days for the travel duration slider
labels = ["1d","2d","3d","4d","5d","6d","1w","10d","2w"] #labels for each duration option that will be shownon the slider instead of the days

if "preferences" in st.session_state and "travel_duration" in st.session_state.preferences: # check if travel duration was previously saved in preferences
    saved = st.session_state.preferences["travel_duration"] # use the saved travel duration from preferences if it exists
    default_index = min(range(len(duration_options)), key=lambda i: abs(duration_options[i] - saved)) # finds the index of the duration option that is closest to the saved travel duration and uses that as the default index for the slider
else:
    default_index = 6  # 1 week by default

selected_index = st.select_slider("Number of days", options=list(range(len(duration_options))), value=default_index, format_func=lambda i: labels[i], key="travel_duration_index") # creates a select slider for travel duration with options corresponding to the indexes of the duration_options list, default index based on saved preferences or existing default, and labels from the labels list, then assigns the selected index to selected_index variable
travel_duration = duration_options[selected_index] # sets the travel_duration variable to the value from the duration_options list that corresponds to the selected index from the slider

# Badge
if travel_duration < 7: #if the selected travel duration is less than 7 days,
    dur_label = f"{travel_duration} days" #the dur_label variable is set to the number of days followed by "days"
else: #if the selected travel duration is 7 days or more,
    weeks = round(travel_duration / 7, 1) #the number of weeks is calculated by dividing the travel duration in days by 7 and rounding to 1 decimal place, 
    dur_label = f"{weeks} weeks" # then the dur_label variable is set to the number of weeks followed by "weeks"

#goal of the label + badge code is to have all possible travel durations displayed in a more user-friendly format (not just a linear number of days)


#Design: AI-generated
st.markdown(f""" 
<div style="margin-top:12px; display:flex; align-items:center; gap:12px;">
    <span style="font-family:'Playfair Display',serif; font-size:1.8rem; font-weight:900; color:#ffffff;">{travel_duration}</span>
    <span style="color:#9ca3af; font-size:0.9rem;">days —</span>
    <span style="background:rgba(245,158,11,0.15); color:#f59e0b; padding:4px 14px;
          border-radius:20px; font-size:0.85rem; font-weight:600;
          border:1px solid rgba(245,158,11,0.35);">{dur_label}</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True) #add spacing between buttons and stats with 150px distance (AI generated)





if st.button("View Results✔️"): #sets a view results button with a checkmark icon at the bottom of the page
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
    st.switch_page("pages/TravelPlannerResults.py")  # navigate to the results page after saving preferences


