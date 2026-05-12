import streamlit as st
import requests  # needed for potential future API calls
from API import get_weather, get_destination_image  # import weather and image functions from API module
from ml_travel_recommender import (
    load_project_destinations,    # loads all destinations from the database
    predict_destination_scores,   # scores each destination based on user preferences
    train_match_model,            # trains the ML model on destination data
)

# ============================================================
# TRAVEL ADVISORY DATA — US State Department (May 2026)
# Levels: 1=Normal precautions, 2=Increased caution, 3=Reconsider, 4=Do not travel
# Risk indicators: C=Crime, T=Terrorism, U=Civil Unrest, H=Health,
#                  N=Natural Disaster, K=Kidnapping, D=Wrongful Detention, O=Other
# ============================================================
TRAVEL_ADVISORIES = {
    # Level 1 — Exercise normal precautions
    "Australia":        (1, "Exercise normal precautions", []),
    "New Zealand":      (1, "Exercise normal precautions", []),
    "Japan":            (1, "Exercise normal precautions", []),
    "South Korea":      (1, "Exercise normal precautions", []),
    "Singapore":        (1, "Exercise normal precautions", []),
    "Switzerland":      (1, "Exercise normal precautions", []),
    "Norway":           (1, "Exercise normal precautions", []),
    "Denmark":          (1, "Exercise normal precautions", []),
    "Finland":          (1, "Exercise normal precautions", []),
    "Iceland":          (1, "Exercise normal precautions", []),
    "Canada":           (1, "Exercise normal precautions", []),
    "Ireland":          (1, "Exercise normal precautions", []),
    "Portugal":         (1, "Exercise normal precautions", []),
    "Austria":          (1, "Exercise normal precautions", []),
    "Slovenia":         (1, "Exercise normal precautions", []),
    "Estonia":          (1, "Exercise normal precautions", []),
    "Latvia":           (1, "Exercise normal precautions", []),
    "Lithuania":        (1, "Exercise normal precautions", []),
    "Czech Republic":   (1, "Exercise normal precautions", []),
    "Czechia":          (1, "Exercise normal precautions", []),
    "Slovakia":         (1, "Exercise normal precautions", []),
    "Hungary":          (1, "Exercise normal precautions", []),
    "Croatia":          (1, "Exercise normal precautions", []),
    "Greece":           (1, "Exercise normal precautions", []),
    "Poland":           (1, "Exercise normal precautions", []),
    "Romania":          (1, "Exercise normal precautions", []),
    "Bulgaria":         (1, "Exercise normal precautions", []),
    "Malta":            (1, "Exercise normal precautions", []),
    "Luxembourg":       (1, "Exercise normal precautions", []),
    "Taiwan":           (1, "Exercise normal precautions", []),
    "Bhutan":           (1, "Exercise normal precautions", []),
    "Chile":            (1, "Exercise normal precautions", []),
    "Uruguay":          (1, "Exercise normal precautions", []),
    "Botswana":         (1, "Exercise normal precautions", []),
    "Namibia":          (1, "Exercise normal precautions", []),
    "Rwanda":           (1, "Exercise normal precautions", []),
    "Monaco":           (1, "Exercise normal precautions", []),
    "Andorra":          (1, "Exercise normal precautions", []),
    "Seychelles":       (1, "Exercise normal precautions", []),
    "Mauritius":        (1, "Exercise normal precautions", []),
    "Cape Verde":       (1, "Exercise normal precautions", []),
    "Samoa":            (1, "Exercise normal precautions", []),
    "New Caledonia":    (1, "Exercise normal precautions", []),
    "Aruba":            (1, "Exercise normal precautions", []),
    "Curaçao":          (1, "Exercise normal precautions", []),
    "Bonaire":          (1, "Exercise normal precautions", []),

    # Level 2 — Exercise increased caution
    "USA":                      (2, "Exercise increased caution", ["C", "T"]),
    "United States":            (2, "Exercise increased caution", ["C", "T"]),
    "United States of America": (2, "Exercise increased caution", ["C", "T"]),
    "UK":                       (2, "Exercise increased caution", ["T"]),
    "United Kingdom":           (2, "Exercise increased caution", ["T"]),
    "France":                   (2, "Exercise increased caution", ["T", "U"]),
    "Germany":                  (2, "Exercise increased caution", ["T"]),
    "Italy":                    (2, "Exercise increased caution", ["T"]),
    "Spain":                    (2, "Exercise increased caution", ["T"]),
    "Netherlands":              (2, "Exercise increased caution", ["T"]),
    "Belgium":                  (2, "Exercise increased caution", ["T"]),
    "Sweden":                   (2, "Exercise increased caution", ["T", "C"]),
    "Serbia":                   (2, "Exercise increased caution", ["C"]),
    "Albania":                  (2, "Exercise increased caution", ["C"]),
    "Montenegro":               (2, "Exercise increased caution", ["C"]),
    "North Macedonia":          (2, "Exercise increased caution", ["C"]),
    "Bosnia and Herzegovina":   (2, "Exercise increased caution", ["C", "U"]),
    "Kosovo":                   (2, "Exercise increased caution", ["C", "U"]),
    "Moldova":                  (2, "Exercise increased caution", ["C"]),
    "China":                    (2, "Exercise increased caution", ["D", "O"]),
    "Hong Kong":                (2, "Exercise increased caution", ["D", "O"]),
    "India":                    (2, "Exercise increased caution", ["T", "C", "N"]),
    "Thailand":                 (2, "Exercise increased caution", ["T", "C"]),
    "Vietnam":                  (2, "Exercise increased caution", ["C"]),
    "Indonesia":                (2, "Exercise increased caution", ["T", "N"]),
    "Malaysia":                 (2, "Exercise increased caution", ["C", "T"]),
    "Philippines":              (2, "Exercise increased caution", ["C", "T", "N"]),
    "Sri Lanka":                (2, "Exercise increased caution", ["T", "C"]),
    "Nepal":                    (2, "Exercise increased caution", ["C", "N"]),
    "Morocco":                  (2, "Exercise increased caution", ["T", "C"]),
    "Tunisia":                  (2, "Exercise increased caution", ["T", "C"]),
    "Egypt":                    (2, "Exercise increased caution", ["T", "C"]),
    "Kenya":                    (2, "Exercise increased caution", ["T", "C"]),
    "Tanzania":                 (2, "Exercise increased caution", ["T", "C"]),
    "South Africa":             (2, "Exercise increased caution", ["C"]),
    "Brazil":                   (2, "Exercise increased caution", ["C"]),
    "Argentina":                (2, "Exercise increased caution", ["C"]),
    "Peru":                     (2, "Exercise increased caution", ["C", "U"]),
    "Colombia":                 (2, "Exercise increased caution", ["C", "T", "K"]),
    "Mexico":                   (2, "Exercise increased caution", ["C", "K"]),
    "Turkey":                   (2, "Exercise increased caution", ["T", "C"]),
    "Türkiye":                  (2, "Exercise increased caution", ["T", "C"]),
    "Jordan":                   (2, "Exercise increased caution", ["T"]),
    "Oman":                     (2, "Exercise increased caution", ["T", "O"]),
    "Saudi Arabia":             (2, "Exercise increased caution", ["T", "C"]),
    "Maldives":                 (2, "Exercise increased caution", ["C"]),
    "Fiji":                     (2, "Exercise increased caution", ["C"]),
    "Cambodia":                 (2, "Exercise increased caution", ["C"]),
    "Laos":                     (2, "Exercise increased caution", ["C"]),
    "Mongolia":                 (2, "Exercise increased caution", ["C"]),
    "Cuba":                     (2, "Exercise increased caution", ["C", "D"]),
    "Jamaica":                  (2, "Exercise increased caution", ["C"]),
    "Costa Rica":               (2, "Exercise increased caution", ["C"]),
    "Panama":                   (2, "Exercise increased caution", ["C"]),
    "Ecuador":                  (2, "Exercise increased caution", ["C", "K"]),
    "Bolivia":                  (2, "Exercise increased caution", ["C", "U"]),
    "Paraguay":                 (2, "Exercise increased caution", ["C"]),
    "Ghana":                    (2, "Exercise increased caution", ["C", "T"]),
    "Senegal":                  (2, "Exercise increased caution", ["C", "T"]),
    "Ethiopia":                 (2, "Exercise increased caution", ["C", "U", "T"]),
    "Uganda":                   (2, "Exercise increased caution", ["C", "T"]),
    "Zimbabwe":                 (2, "Exercise increased caution", ["C"]),
    "Mozambique":               (2, "Exercise increased caution", ["C", "T"]),
    "Georgia":                  (2, "Exercise increased caution", ["C"]),
    "Armenia":                  (2, "Exercise increased caution", ["C"]),
    "Kazakhstan":               (2, "Exercise increased caution", ["C", "T"]),
    "Uzbekistan":               (2, "Exercise increased caution", ["C", "T"]),
    "Azerbaijan":               (2, "Exercise increased caution", ["C", "U"]),
    "Ivory Coast":              (2, "Exercise increased caution", ["C", "T"]),
    "Madagascar":               (2, "Exercise increased caution", ["C"]),
    "Vanuatu":                  (2, "Exercise increased caution", ["C", "N"]),
    "Dominican Republic":       (2, "Exercise increased caution", ["C"]),
    "Tibet":                    (2, "Exercise increased caution", ["D", "O"]),
    "Malawi":                   (2, "Exercise increased caution", ["C"]),
    "Burundi":                  (2, "Exercise increased caution", ["C", "U"]),
    "Greenland":                (2, "Exercise increased caution", ["N"]),
    "Argentina/Chile":          (2, "Exercise increased caution", ["C"]),

    # Level 3 — Reconsider travel
    "Pakistan":                     (3, "Reconsider travel", ["T", "C", "K"]),
    "Bangladesh":                   (3, "Reconsider travel", ["T", "C", "U"]),
    "Nigeria":                      (3, "Reconsider travel", ["C", "T", "K"]),
    "Algeria":                      (3, "Reconsider travel", ["T", "C"]),
    "Cameroon":                     (3, "Reconsider travel", ["C", "T", "U"]),
    "Myanmar":                      (3, "Reconsider travel", ["C", "T", "U"]),
    "Venezuela":                    (3, "Reconsider travel", ["C", "K", "T"]),
    "Honduras":                     (3, "Reconsider travel", ["C", "K"]),
    "El Salvador":                  (3, "Reconsider travel", ["C"]),
    "Guatemala":                    (3, "Reconsider travel", ["C", "K"]),
    "Nicaragua":                    (3, "Reconsider travel", ["C", "D"]),
    "Haiti":                        (3, "Reconsider travel", ["C", "K", "U"]),
    "Papua New Guinea":             (3, "Reconsider travel", ["C", "K"]),
    "Congo":                        (3, "Reconsider travel", ["C", "T", "U"]),
    "Democratic Republic of Congo": (3, "Reconsider travel", ["C", "T", "U"]),
    "DRC":                          (3, "Reconsider travel", ["C", "T", "U"]),
    "Niger":                        (3, "Reconsider travel", ["T", "C", "K"]),
    "Burkina Faso":                 (3, "Reconsider travel", ["T", "C", "K"]),
    "Guinea":                       (3, "Reconsider travel", ["C", "U"]),
    "Tajikistan":                   (3, "Reconsider travel", ["T", "C"]),
    "Libya":                        (3, "Reconsider travel", ["T", "C", "U", "K"]),
    "Lebanon":                      (3, "Reconsider travel", ["T", "C", "U"]),
    "Iran":                         (3, "Reconsider travel", ["T", "D", "K"]),
    "Iraq":                         (3, "Reconsider travel", ["T", "C", "K"]),

    # Level 4 — Do not travel
    "Afghanistan":              (4, "Do not travel", ["T", "C", "K", "U"]),
    "Syria":                    (4, "Do not travel", ["T", "C", "K", "U"]),
    "Yemen":                    (4, "Do not travel", ["T", "C", "K", "U"]),
    "Somalia":                  (4, "Do not travel", ["T", "C", "K"]),
    "Sudan":                    (4, "Do not travel", ["T", "C", "U", "K"]),
    "South Sudan":              (4, "Do not travel", ["T", "C", "K", "U"]),
    "North Korea":              (4, "Do not travel", ["D", "K", "C"]),
    "Russia":                   (4, "Do not travel", ["T", "C", "D", "U"]),
    "Ukraine":                  (4, "Do not travel", ["T", "U"]),
    "Belarus":                  (4, "Do not travel", ["D", "U"]),
    "Mali":                     (4, "Do not travel", ["T", "C", "K"]),
    "Central African Republic": (4, "Do not travel", ["T", "C", "K", "U"]),
    "Eritrea":                  (4, "Do not travel", ["D", "C"]),
    "Israel":                   (4, "Do not travel", ["T", "U"]),
    "Palestine":                (4, "Do not travel", ["T", "U"]),
    "Bahrain":                  (4, "Do not travel", ["T", "U"]),
    "Kuwait":                   (4, "Do not travel", ["T"]),
    "United Arab Emirates":     (4, "Do not travel", ["T"]),
    "UAE":                      (4, "Do not travel", ["T"]),
    "Qatar":                    (4, "Do not travel", ["T"]),
}

# Human-readable descriptions for each risk indicator code
RISK_DESCRIPTIONS = {
    "C": "🔴 Crime",
    "T": "💣 Terrorism",
    "U": "⚡ Civil Unrest",
    "H": "🏥 Health Risks",
    "N": "🌊 Natural Disasters",
    "K": "⚠️ Kidnapping Risk",
    "D": "🚫 Wrongful Detention Risk",
    "O": "⚠️ Other Risks"
}

def get_advisory_from_dict(country):
    """Look up travel advisory level and risk indicators for a given country"""
    if country in TRAVEL_ADVISORIES:  # try exact match first
        level, message, risks = TRAVEL_ADVISORIES[country]
        return {"level_text": message, "color": level, "risks": risks}
    for key, (level, message, risks) in TRAVEL_ADVISORIES.items():  # try case insensitive match
        if key.lower() == country.lower():
            return {"level_text": message, "color": level, "risks": risks}
    return None  # return None if country not found in dictionary

# ============================================================
# PAGE DESIGN — AI-generated
# ============================================================
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
# end of Design

# check if preferences exist in session state — redirect to questionnaire if not
if "preferences" not in st.session_state:
    st.warning("Please complete the questionnaire first!")
    if st.button("Go to Questionnaire"):
        st.switch_page("pages/TravelPlannerQuestionnaire.py")
    st.stop()  # stop the rest of the page from loading

# return home button
if st.button("Return Home", icon="🏠"):
    st.switch_page("TravelPlannerDemo.py")

st.title("🎯 Your Top 10 Destinations")  # page title

# ============================================================
# ML MODEL — load destinations and score them
# ============================================================
import plotly.express as px  # import plotly for bar chart visualization

destinations = load_project_destinations()  # load all destinations from the database
model_bundle = train_match_model(destinations)  # train the ML model on destination data

# score each destination based on user preferences using the ML model
ml_scores = predict_destination_scores(
    st.session_state.preferences,
    destinations,
    model_bundle,
)

# create a dictionary mapping destination name to its ML score for quick lookup
score_map = dict(zip(ml_scores["destination"], ml_scores["ml_match_score"]))

# add ML scores to each destination dictionary
sorted_recs = []
for destination in destinations:
    place = destination["place"]
    ml_score = score_map.get(place, 0)  # get score from map, default to 0 if not found
    destination["score"] = ml_score
    destination["ml_match_score"] = ml_score
    sorted_recs.append(destination)

# sort destinations by score descending and take top 10
sorted_recs = sorted(sorted_recs, key=lambda x: x["ml_match_score"], reverse=True)[:10]

# ============================================================
# BAR CHART — visualize top 10 destination scores
# ============================================================
fig = px.bar(
    x=[r["place"] for r in sorted_recs],   # x axis: destination names
    y=[r["score"] for r in sorted_recs],   # y axis: match scores
    color_discrete_sequence=["#8a2be2"]    # purple bars to match design
)
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",   # transparent background
    paper_bgcolor="rgba(0,0,0,0)",  # transparent paper
    font_color="#ffffff",            # white text
    xaxis_title="",                  # no x axis label needed
    yaxis_title="Score",             # y axis label
)
st.plotly_chart(fig, use_container_width=True)  # display chart full width

# ============================================================
# DESTINATION LOOP — display each recommended destination
# ============================================================
for rank, destination in enumerate(sorted_recs, 1):  # loop through top 10, starting rank at 1
    score = destination["score"]  # get match score for this destination
    score_color = "#34d399" if score >= 70 else "#f59e0b" if score >= 40 else "#f87171"  # green/yellow/red based on score

    # destination card — AI-generated design
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

    # fetch and display destination photo from Unsplash API
    img_url = get_destination_image(destination["place"])  # search Unsplash for destination photo
    if img_url:  # only show image if one was found
        st.image(img_url, width=300)

    # weather section — fetches live data from OpenWeatherMap API
    weather = get_weather(destination["place"])  # call get_weather with destination city name
    if weather:  # only display if weather data was successfully retrieved
        col1, col2, col3, col4 = st.columns(4)  # 4 columns for weather metrics
        with col1:  # temperature
            st.markdown(f"""<div style="color:#c084fc; font-size:0.8rem;">Temperature</div>
            <div style="color:#ffffff; font-size:1rem; font-weight:600;">{weather['temp']}°C</div>""",
            unsafe_allow_html=True)
        with col2:  # humidity
            st.markdown(f"""<div style="color:#c084fc; font-size:0.8rem;">Humidity</div>
            <div style="color:#ffffff; font-size:1rem; font-weight:600;">{weather['humidity']}%</div>""",
            unsafe_allow_html=True)
        with col3:  # wind speed
            st.markdown(f"""<div style="color:#c084fc; font-size:0.8rem;">Wind Speed</div>
            <div style="color:#ffffff; font-size:1rem; font-weight:600;">{weather['wind_speed']} m/s</div>""",
            unsafe_allow_html=True)
        with col4:  # conditions
            st.markdown(f"""<div style="color:#c084fc; font-size:0.8rem;">Conditions</div>
            <div style="color:#ffffff; font-size:1rem; font-weight:600;">{weather['description'].capitalize()}</div>""",
            unsafe_allow_html=True)

    # travel advisory section — looks up safety level from hardcoded US State Department data
    advisory = get_advisory_from_dict(destination["country"])  # look up advisory for this country

    if advisory:  # only display if advisory data was found
        level = advisory["color"]         # severity: 1=normal, 2=caution, 3=reconsider, 4=do not travel
        message = advisory["level_text"]  # advisory message e.g. "Exercise increased caution"
        risks = advisory["risks"]         # list of risk indicator codes e.g. ["C", "T"]

        # color map — each level gets a distinct color for clear visual communication
        colors = {
            1: "#34d399",  # green — normal precautions
            2: "#f59e0b",  # yellow — increased caution
            3: "#f97316",  # orange — reconsider travel
            4: "#f87171"   # red — do not travel
        }
        color = colors.get(level, "#9ca3af")  # get color, grey as fallback

        # build risk indicator tags from the risks list
        risk_tags = " ".join([
            f'<span style="background:rgba(255,255,255,0.1); border-radius:6px; padding:2px 8px; font-size:0.75rem; margin-right:4px;">{RISK_DESCRIPTIONS[r]}</span>'
            for r in risks
        ])

        # display advisory card with color border and risk tags — AI-generated design
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.04); border:1px solid {color}50;
             border-radius:12px; padding:12px 16px; margin-top:8px;">
            <div style="color:{color}; font-weight:600; font-size:0.9rem;">
                🛡️ Travel Advisory: {message}
            </div>
            <div style="margin-top:6px;">{risk_tags}</div>
            <div style="color:#9ca3af; font-size:0.75rem; margin-top:6px;">
                Source: US State Department
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # show neutral placeholder if no advisory found for this country
        st.markdown("""
        <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(156,163,175,0.3);
             border-radius:12px; padding:12px 16px; margin-top:8px;">
            <div style="color:#9ca3af; font-size:0.9rem;">
                🛡️ Travel Advisory: No advisory data available
            </div>
            <div style="color:#9ca3af; font-size:0.75rem; margin-top:4px;">
                Source: US State Department
            </div>
        </div>
        """, unsafe_allow_html=True)

    # plan this trip button — saves destination to session state and navigates to dashboard
    col_l, col_btn, col_r = st.columns([2, 2, 2])  # 3 columns to center the button
    with col_btn:  # place button in middle column
        if st.button(f"🗺️  Plan this trip", key=f"btn_{rank}", use_container_width=True):  # unique key per destination
            st.session_state.selected_destination = destination  # save selected destination to session state
            st.switch_page("pages/TravelPlannerDashboard.py")  # navigate to dashboard

    st.markdown("---")  # divider between destination cards
