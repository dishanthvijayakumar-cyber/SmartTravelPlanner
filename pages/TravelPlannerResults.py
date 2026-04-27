import streamlit as st
st.set_page_config(page_title="SmartTravel - Results", page_icon="🎯")

#If user haven't completed the questionnaire, redirect him
if "recommendations" not in st.session_state:
    st.warning("Please complete the questionnaire first!")
    if st.button ("Go to Questionnaire"):
        st.switch_page("pages/TravelPlannerQuestionnaire.py")
    st. stop()

#Navigation button to return to the home page
if st.button("Return Home", icon="🏠"):
    st.switch_page("TravelPlannerDemo.py")

st.title("🎯 Your Top 10 Destinations")

#Build a dictionary of destination names & scores for the bar chart
chart_data = {r["place"]: r["score"] for r in st.session_state.recommendations}
#Display a bar chart comparing the match scores of top 10 destinations
st.bar_chart(chart_data)


#Look through each recommended destination & display its details
for rank, destination in enumerate(st.session_state.recommendations, 1):
    #Dispaly rank, destination name and match score
    st.subheader(f"#{rank} - {destination['place']} - {destination['score']}/100")
    #Display destination image reported from Wikipedia --> to be improved
    st.image(f"https://en.wikipedia.org/wiki/Special:FilePath/{destination['place']}.jpg", width=300)
    st.write(f"🌍 {destination['country']} | 🌤️ {destination['climate']}")
    st.write(f"📖 {destination['description_sentence']}")

    #Button to select this destination & go to the dashboard
    #key=f"btn_{rank}" AI-generated: ensures each button has a unique identifier
    if st.button(f"Plan this trip", key=f"btn_{rank}"):
        st.session_state.selected_destination = destination
        st.switch_page("pages/TravelPlannerDashboard.py")
    
    st.markdown("---")
