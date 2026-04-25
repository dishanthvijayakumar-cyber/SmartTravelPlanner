import streamlit as st
import random
import sys
sys.path.insert(0, '.')
from database import get_destinations

st.set_page_config(page_title="SmartTravel - Surprise!", page_icon="🎲")

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
