import streamlit as st  # Streamlit framework for building the web app
import random  # Used to pick random destinations
import sys  # Needed to adjust import paths
import textwrap  # Removes indentation from multiline HTML strings

# Make sure local modules like database.py can be found
sys.path.insert(0, ".")

from database import get_destinations  # Loads all available travel destinations
from API import get_destination_image  # Fetches images from Unsplash API

# Set page title and browser tab icon
st.set_page_config(page_title="SmartTravel - Surprise!", page_icon="🎲")

# Design Improvement
st.markdown(
    textwrap.dedent("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #1a0030 0%, #2d0057 40%, #0d001a 100%) !important;
        font-family: 'DM Sans', sans-serif;
        color: #ffffff;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #6a0dad, #8a2be2) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(138, 43, 226, 0.4) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(138, 43, 226, 0.6) !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricLabel"] {
        color: #c084fc !important;
    }
    </style>
    """),
    unsafe_allow_html=True
)

# Back button to home page
if st.button("Return Home", icon="🏠"):
    st.switch_page("TravelPlannerDemo.py")

# Prevent direct access without selected destination
if "selected_destination" not in st.session_state:
    st.warning("No destination selected. Redirecting back home...")
    st.switch_page("TravelPlannerDemo.py")
    st.stop()

# Load selected destination from session memory
destination = st.session_state.selected_destination

# Header section
st.markdown(
    textwrap.dedent(f"""
    <div style="text-align:center; padding:30px 20px 20px;">
        <p style="font-size:0.75rem; letter-spacing:4px; text-transform:uppercase; color:#c084fc; margin-bottom:10px;">
            ✦ Your Surprise ✦
        </p>

        <div style="font-size:3.5rem; margin-bottom:10px;">🎲</div>

        <h1 style="font-family:'Playfair Display',serif; font-size:2.8rem; font-weight:900; background:linear-gradient(90deg,#c084fc,#f59e0b); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0 0 8px;">
            {destination['place']}
        </h1>

        <p style="color:#d8b4fe; font-size:1.1rem; font-weight:300;">
            ✈️ {destination['country']}
        </p>
    </div>
    """),
    unsafe_allow_html=True
)

# Fetch image for destination
img_url = get_destination_image(destination["place"])

# Show image, with fallback if API fails
if img_url:
    st.image(img_url, width=400)
else:
    st.image(
        f"https://en.wikipedia.org/wiki/Special:FilePath/{destination['place']}.jpg",
        width=400
    )

# Quick overview metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Climate", destination["climate"].capitalize())

with col2:
    st.metric("Daily Budget Min", f"${destination['budget_min']}")

with col3:
    st.metric("Daily Budget Max", f"${destination['budget_max']}")

st.markdown("---")

# Description section
st.subheader("About this destination")
st.write(destination["description_sentence"])

# Collect optional metadata into structured tags
tags = []

if destination.get("best_for"):
    tags.append(("🏆 Best for", destination["best_for"]))

if destination.get("activities"):
    tags.append(("🎯 Activities", ", ".join(destination["activities"])))

if destination.get("interests"):
    tags.append(("💡 Interests", ", ".join(destination["interests"])))

if destination.get("styles"):
    tags.append(("✈️ Travel styles", ", ".join(destination["styles"])))

if destination.get("accommodation"):
    tags.append(("🏨 Accommodation", ", ".join(destination["accommodation"])))

# Render tags
for label, value in tags:
    st.markdown(
        textwrap.dedent(f"""
        <div style="display:flex; gap:12px; margin-bottom:10px; align-items:flex-start;">
            <span style="color:#f59e0b; font-size:0.85rem; font-weight:600; min-width:130px;">
                {label}
            </span>

            <span style="color:#d8b4fe; font-size:0.9rem; font-weight:300;">
                {value}
            </span>
        </div>
        """),
        unsafe_allow_html=True
    )

st.markdown("---")

# Action buttons section
col1, col2 = st.columns(2)

with col1:
    if st.button("🗺️ Plan this trip", use_container_width=True):
        st.switch_page("pages/TravelPlannerDashboard.py")

with col2:
    if st.button("🎲 Try Another!", use_container_width=True):
        destinations = get_destinations()
        st.session_state.selected_destination = random.choice(destinations)
        st.rerun()

