import streamlit as st  # Streamlit is the framework we're using to build the web app
import random  # We need this to pick a random destination when user clicks "Try Another"
import sys

# This line is a bit of a workaround - we're telling Python to also look in the current folder
# when searching for modules. This is needed because Streamlit sometimes has trouble finding
# our local files like database.py
sys.path.insert(0, '.')
from database import get_destinations  # Get the list of all possible destinations from our database
from API import get_destination_image  # Function to fetch nice travel photos from Unsplash

# Here we set up how the browser tab looks - title and a dice emoji as the icon
st.set_page_config(page_title="SmartTravel - Surprise!", page_icon="🎲")

# This big block is our custom CSS styling to make the app look good (dark purple theme, nice fonts, etc.)
# CSS is basically just styling rules - we're overriding Streamlit's default look to match our design
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


# Simple back button so users can go back to the main page
if st.button("Return Home", icon="🏠"):
    st.switch_page("TravelPlannerDemo.py")

# Check if the user actually came here through the app properly (not just typing the URL directly)
# If there's no destination saved in the session, we show a warning and send them back home
# This prevents people from landing on a broken page
if "selected_destination" not in st.session_state:
    st.warning("No destination selected. Going back home...")
    st.switch_page("TravelPlannerDemo.py")
    st.stop()  # This stops the page from rendering anything else

# Get the destination that was randomly picked earlier and stored in session state
# Session state is like a temporary memory that keeps data while the user browses around
destination = st.session_state.selected_destination

# This creates the big header at the top of the page with the destination name
# We're using HTML inside the markdown to create a nice gradient text effect and center everything
st.markdown(f"""
<div style="text-align:center; padding:30px 20px 20px;">
    <p style="font-size:0.75rem; letter-spacing:4px; text-transform:uppercase; color:#c084fc; margin-bottom:10px;">
        ✦ Your Surprise ✦
    </p>
    <div style="font-size:3.5rem; margin-bottom:10px;">🎲</div>
    <h1 style="font-family:'Playfair Display',serif; font-size:2.8rem; font-weight:900;
          background:linear-gradient(90deg,#c084fc,#f59e0b);
          -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0 0 8px;">
        {destination['place']}
    </h1>
    <p style="color:#d8b4fe; font-size:1.1rem; font-weight:300;">✈️ {destination['country']}</p>
</div>
""", unsafe_allow_html=True)

# Get a nice travel photo for the destination from Unsplash
# We search Unsplash using "{place} travel landmark" which usually gives good results
# Unsplash is a free photo site with really nice travel pictures
img_url = get_destination_image(destination["place"])

# If we got a photo back from Unsplash, show it (400px wide for the surprise page)
# If the API fails or doesn't find anything, we fall back to grabbing a Wikipedia image instead
if img_url:
    st.image(img_url, width=400)
else:
    st.image(f"https://en.wikipedia.org/wiki/Special:FilePath/{destination['place']}.jpg", width=400)

# Show some quick stats about the destination in three columns
# This gives users an immediate overview: what the climate is like and roughly how expensive it is
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Climate", destination["climate"].capitalize())
with col2:
    st.metric("Daily Budget Min", f"${destination['budget_min']}")
with col3:
    st.metric("Daily Budget Max", f"${destination['budget_max']}")

st.markdown("---")

# A simple subheader and the description sentence we stored for this destination
st.subheader("About this destination")
st.write(destination["description_sentence"])

# Build up a list of interesting tags/details about this destination
# We go through each possible field and only add it to our list if it actually has data
# This way we don't show empty rows with nothing in them
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

# Loop through our tags and display each one as a little row with an emoji and text
# Using HTML divs to make the labels and values line up nicely side by side
for label, value in tags:
    st.markdown(f"""
    <div style="display:flex; gap:12px; margin-bottom:10px; align-items:flex-start;">
        <span style="color:#f59e0b; font-size:0.85rem; font-weight:600; min-width:130px;">{label}</span>
        <span style="color:#d8b4fe; font-size:0.9rem; font-weight:300;">{value}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Two buttons at the bottom of the page so the user can decide what to do next
col1, col2 = st.columns(2)
with col1:
    # This button takes them to the full trip planning dashboard where they can see activities etc.
    if st.button("🗺️ Plan this trip", use_container_width=True):
        st.switch_page("pages/TravelPlannerDashboard.py")
with col2:
    # This button picks a completely new random destination and refreshes the page to show it
    # Uses random.choice() to pick any destination from our database
    if st.button("🎲 Try Another!", use_container_width=True):
        destinations = get_destinations()
        st.session_state.selected_destination = random.choice(destinations)
        st.rerun()  # Refresh the page to show the new destination
