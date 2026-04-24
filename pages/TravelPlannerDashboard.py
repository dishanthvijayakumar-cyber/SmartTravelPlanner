import streamlit as st
st.set_page_config(page_title="SmartTravel - Dashboard", page_icon="👤")

if st.button("Return Home", icon="🏠"):
    st.switch_page("TravelPlannerDemo.py")

st.title("Your Travel Dashboard") #dashboard title
st.header("My Trip Itinerary")


# Trip Overview Section
st.header("📅 Trip Overview")
col1, col2, col3, col4 = st.columns(4) 
with col1:
    st.subheader("Destination:")
    st.write("Kyoto, Japan") # This should be dynamically generated based on user input
with col2:
    travel_duration = 5 # Connect this to the actual travel_duration from the questionnaire etc.
    st.subheader("Duration:")
    if travel_duration == 1:
        st.write(f"{travel_duration} day")  
    else:
        st.write(f"{travel_duration} days")
with col3:
    st.subheader("Travel Dates:")
    st.write("2026-04-15 - 2026-04-19") # This should be dynamically generated based on user input, pot. from questionnaire
    st.button("Edit", icon="✏️")
with col4:
    daily_budget = 500 # Connect this to the actual daily_budget from the questionnaire etc.
    st.subheader("Daily Budget:")
    st.write(f"${daily_budget}")



# Daily Itinerary Section
st.header("🗺️ Daily Itinerary")

travel_duration = 7 # Connect this to the actual travel_duration from the questionnaire etc.
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
st.write(f"Details for Day {selected_day} go here.") # Adapt this to show actual itinerary

    
