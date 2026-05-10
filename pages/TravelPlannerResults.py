import streamlit as st
from API import get_weather, get_destination_image, get_travel_advisory
from ml_streamlit_integration import show_ml_results_page

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
import plotly.express as px

sorted_recs = sorted(st.session_state.recommendations, key=lambda x: x["score"], reverse=True)

fig = px.bar(
    x=[r["place"] for r in sorted_recs],
    y=[r["score"] for r in sorted_recs],
    color_discrete_sequence=["#8a2be2"]
)
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#ffffff",
    xaxis_title="", yaxis_title="Score",
)
st.plotly_chart(fig, use_container_width=True)


#(Design AI-generated)
for rank, destination in enumerate(st.session_state.recommendations, 1):  # loop through all recommended destinations, starting rank at 1
    score = destination["score"]  # get the match score for this destination
    score_color = "#34d399" if score >= 70 else "#f59e0b" if score >= 40 else "#f87171"  # green if high score, yellow if medium, red if low

    # Destination card — AI-generated design
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

    # Fetch and display a destination photo from Unsplash API
    img_url = get_destination_image(destination["place"])  # search Unsplash for a photo of the destination
    if img_url:  # only display if an image was found
        st.image(img_url, width=300)

    # Weather section — fetches live weather data from OpenWeatherMap API for each destination
    weather = get_weather(destination["place"])  # call get_weather function with the destination city name
    if weather:  # only display if weather data was successfully retrieved
        col1, col2, col3, col4 = st.columns(4)  # create 4 columns for weather metrics
        with col1:  # temperature column
            st.markdown(f"""<div style="color:#c084fc; font-size:0.8rem;">Temperature</div>
            <div style="color:#ffffff; font-size:1rem; font-weight:600;">{weather['temp']}°C</div>""",
            unsafe_allow_html=True)
        with col2:  # humidity column
            st.markdown(f"""<div style="color:#c084fc; font-size:0.8rem;">Humidity</div>
            <div style="color:#ffffff; font-size:1rem; font-weight:600;">{weather['humidity']}%</div>""",
            unsafe_allow_html=True)
        with col3:  # wind speed column
            st.markdown(f"""<div style="color:#c084fc; font-size:0.8rem;">Wind Speed</div>
            <div style="color:#ffffff; font-size:1rem; font-weight:600;">{weather['wind_speed']} m/s</div>""",
            unsafe_allow_html=True)
        with col4:  # conditions column
            st.markdown(f"""<div style="color:#c084fc; font-size:0.8rem;">Conditions</div>
            <div style="color:#ffffff; font-size:1rem; font-weight:600;">{weather['description'].capitalize()}</div>""",
            unsafe_allow_html=True)

    # Travel advisory section — fetches official safety level from Australian Government Smartraveller API
    advisory = get_travel_advisory(destination["country"])  # call get_travel_advisory with the destination country name
    if advisory:  # only display if advisory data was successfully retrieved
        level = advisory["color"]        # severity number: 1=safe, 2=caution, 3=reconsider, 4=do not travel
        message = advisory["level_text"] # advisory text e.g. "Exercise a high degree of caution"

        # Color map — each severity level gets a different color for clear visual communication
        colors = {
            1: "#34d399",  # green — normal precautions
            2: "#f59e0b",  # yellow — high degree of caution
            3: "#f97316",  # orange — reconsider travel
            4: "#f87171"   # red — do not travel
        }
        color = colors.get(level, "#9ca3af")  # get color for this level, grey as fallback if level not found

        # Display advisory as a colored card — AI-generated design
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.04); border:1px solid {color}50;
             border-radius:12px; padding:12px 16px; margin-top:8px;">
            <div style="color:{color}; font-weight:600; font-size:0.9rem;">
                🛡️ Travel Advisory: {message}
            </div>
            <div style="color:#9ca3af; font-size:0.75rem; margin-top:4px;">
                Source: Australian Government Smartraveller
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # If no advisory found for this country, show a neutral placeholder instead of nothing
        st.markdown("""
        <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(156,163,175,0.3);
             border-radius:12px; padding:12px 16px; margin-top:8px;">
            <div style="color:#9ca3af; font-size:0.9rem;">
                🛡️ Travel Advisory: No advisory data available for this destination
            </div>
            <div style="color:#9ca3af; font-size:0.75rem; margin-top:4px;">
                Source: Australian Government Smartraveller
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Plan this trip button — saves selected destination to session state and navigates to dashboard
    col_l, col_btn, col_r = st.columns([2, 2, 2])  # create 3 columns to center the button
    with col_btn:  # place button in the middle column
        if st.button(f"🗺️  Plan this trip", key=f"btn_{rank}", use_container_width=True):  # unique key per destination to avoid conflicts
            st.session_state.selected_destination = destination  # save chosen destination to session state for use in dashboard
            st.switch_page("pages/TravelPlannerDashboard.py")  # navigate to the dashboard page

    st.markdown("---")  # divider line between each destination card
