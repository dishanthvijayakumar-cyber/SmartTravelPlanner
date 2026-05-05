import streamlit as st
import random
import sys
sys.path.insert(0, '.')
from database import get_destinations

st.set_page_config(page_title="SmartTravel - Surprise!", page_icon="🎲")

#Design: AI-generated
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
    st.warning("No destination selected. Going back home...")
    st.switch_page("TravelPlannerDemo.py")
    st.stop()

destination = st.session_state.selected_destination

st.markdown("<h2 style='color:#8a2be2;'>🎲 Your Surprise Destination!</h2>", unsafe_allow_html=True)
st.title(f"✈️ {destination['place']}, {destination['country']}")

st.image(
    f"https://en.wikipedia.org/wiki/Special:FilePath/{destination['place']}.jpg",
    width=400,
)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Climate", destination["climate"].capitalize())
with col2:
    st.metric("Daily Budget Min", f"${destination['budget_min']}")
with col3:
    st.metric("Daily Budget Max", f"${destination['budget_max']}")

st.markdown("---")
st.subheader("About this destination")
st.write(destination["description_sentence"])

if destination.get("best_for"):
    st.write(f"**Best for:** {destination['best_for']}")

if destination.get("activities"):
    st.write(f"**Activities:** {', '.join(destination['activities'])}")

if destination.get("interests"):
    st.write(f"**Interests:** {', '.join(destination['interests'])}")

if destination.get("styles"):
    st.write(f"**Travel styles:** {', '.join(destination['styles'])}")

if destination.get("accommodation"):
    st.write(f"**Accommodation:** {', '.join(destination['accommodation'])}")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    if st.button("🗺️ Plan this trip", use_container_width=True):
        st.switch_page("pages/TravelPlannerDashboard.py")
with col2:
    if st.button("🎲 Try Another!", use_container_width=True):
        destinations = get_destinations()
        st.session_state.selected_destination = random.choice(destinations)
        st.rerun()
