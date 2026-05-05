import streamlit as st
import streamlit as st
import random
import sys
from database import get_destinations

st.set_page_config(page_title="SmartTravel - Home", page_icon="🌆") #Tab Title & Icon

#Design (AI-generated)
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

#Notes: Majority of Markdown Code is AI generated; this formatting looks nicer,
# however I'm not sure if we're allowed to use the complicated ones
# We can change back to the simpler version learned in class if needed

#Page Title & Subheaders (AI-generated)
st.markdown("""
<div style="text-align:center; padding:60px 20px 20px;">
    <p style="font-family:'DM Sans',sans-serif; font-size:0.8rem; letter-spacing:4px;
       text-transform:uppercase; color:#c084fc; margin-bottom:14px;">
        ✦ AI-Powered Travel Planning ✦
    </p>
    <h1 style="font-family:'Playfair Display',serif; font-size:clamp(2.4rem,6vw,4.5rem);
       font-weight:900; line-height:1.1; color:#ffffff; margin:0 0 20px;">
        Discover Your<br>
        <span style="background:linear-gradient(90deg,#c084fc,#f59e0b);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
            Perfect Destination
        </span>
    </h1>
    <p style="font-family:'DM Sans',sans-serif; font-size:1.1rem; color:#d8b4fe;
       max-width:540px; margin:0 auto 40px; font-weight:300; line-height:1.7;">
        Answer a few questions and let our smart engine match you with your ideal travel experience.
    </p>
</div>
""", unsafe_allow_html=True)

#Buttons to start journey -- no feature yet, just for show
col1, col2 = st.columns(2) #makes two columns for buttons --> positions them next to eachother
with col1:
    if st.button("Start Your Journey", icon="✈️"): #places button in first column, with icon
        st.switch_page("pages/TravelPlannerQuestionnaire.py")
with col2:
    if st.button("View Dashboard", icon="📊"): #places button in second column, with icon
        st.switch_page("pages/TravelPlannerDashboard.py") 
#add spacing between buttons and stats with 40px distance (AI generated)
st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)

#Website statistics (AI-generated)
st.markdown("""
<div style="display:flex; justify-content:center; gap:60px; flex-wrap:wrap;
     padding:30px 20px; background:rgba(255,255,255,0.05); border-radius:20px;
     border:1px solid rgba(192,132,252,0.2); max-width:800px; margin:0 auto;">
    <div style="text-align:center;">
        <div style="font-family:'Playfair Display',serif; font-size:2.2rem; font-weight:900; color:#f59e0b;">250+</div>
        <div style="font-size:0.75rem; letter-spacing:2px; text-transform:uppercase; color:#c084fc; margin-top:4px;">Destinations</div>
    </div>
    <div style="text-align:center;">
        <div style="font-family:'Playfair Display',serif; font-size:2.2rem; font-weight:900; color:#f59e0b;">98%</div>
        <div style="font-size:0.75rem; letter-spacing:2px; text-transform:uppercase; color:#c084fc; margin-top:4px;">Match Accuracy</div>
    </div>
    <div style="text-align:center;">
        <div style="font-family:'Playfair Display',serif; font-size:2.2rem; font-weight:900; color:#f59e0b;">50k+</div>
        <div style="font-size:0.75rem; letter-spacing:2px; text-transform:uppercase; color:#c084fc; margin-top:4px;">Happy Travelers</div>
    </div>
</div>
""", unsafe_allow_html=True)

#add spacing with 60px distance (AI generated)
st.markdown("<div style='margin-top: 60px;'></div>", unsafe_allow_html=True)

#Discover Your Way Section
st.title("Discover Your Way")
st.subheader("Not sure where to start? Try an alternative way to find your perfect destination:")

#Surprise Me button (AI-generated design)
col_l, col_c, col_r = st.columns([2, 2, 2])
with col_c:
    st.markdown("""
    <div style="background:rgba(255,255,255,0.06); border:1px solid rgba(192,132,252,0.3);
         border-radius:24px; padding:36px 28px; text-align:center; backdrop-filter:blur(12px);">
        <div style="font-size:3rem; margin-bottom:16px;">🎲</div>
        <h3 style="font-family:'Playfair Display',serif; color:#fff; margin:0 0 10px;">Surprise Me!</h3>
        <p style="color:#c084fc; font-size:0.9rem; margin:0 0 24px; font-weight:300;">
            Feeling adventurous? Discover something unexpected.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🎲  Surprise Me!", use_container_width=True):
        destinations = get_destinations()
        st.session_state.selected_destination = random.choice(destinations)
        st.switch_page("pages/TravelPlannerSurprise.py")


#add spacing with 60px distance (AI generated)
st.markdown("<div style='margin-top: 60px;'></div>", unsafe_allow_html=True)

#Why Choose SmartTravel Section (Design AI-generated)
st.markdown("""
<div style="text-align:center; margin-bottom:40px;">
    <h2 style="font-family:'Playfair Display',serif; font-size:2.2rem; color:#fff;">Why Choose SmartTravel?</h2>
    <p style="color:#d8b4fe; font-weight:300; font-size:1rem;">The smarter way to plan unforgettable trips</p>
</div>
""", unsafe_allow_html=True)

features = [
    ("🔍", "Detailed Insights", "Explore activities, budget breakdowns, and live weather for every destination."),
    ("✅", "Trusted Information", "Curated picks from verified travel experts and real travelers."),
    ("⚡", "Instant Results", "Get personalised travel matches in seconds, not hours."),
    ("🤖", "AI-Powered", "Smart suggestions based on your unique preferences and travel style."),
    ("📊", "Match Scores", "See exactly how well each destination fits your interests."),
    ("🗺️", "Easy Planning", "Build your perfect itinerary with a clean, intuitive dashboard."),
]

cols = st.columns(3)
for i, (icon, title, desc) in enumerate(features):
    with cols[i % 3]:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.06); border:1px solid rgba(192,132,252,0.2);
             border-radius:20px; padding:28px 22px; margin-bottom:20px; backdrop-filter:blur(8px);">
            <div style="font-size:2rem; margin-bottom:14px;">{icon}</div>
            <h4 style="font-family:'Playfair Display',serif; font-size:1.05rem; color:#fff; margin:0 0 10px;">{title}</h4>
            <p style="color:#c084fc; font-size:0.85rem; margin:0; font-weight:300; line-height:1.6;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

#spacing (AI generated)
st.markdown("<div style='margin-top: 60px;'></div>", unsafe_allow_html=True) 
col1, col2, col3 = st.columns(3)

#Ready to explore section (Design AI-generated)
st.markdown("""
<div style="background:linear-gradient(135deg, rgba(106,13,173,0.6), rgba(138,43,226,0.4));
     border:1px solid rgba(192,132,252,0.3); border-radius:24px;
     padding:50px 40px; text-align:center; backdrop-filter:blur(10px);">
    <h2 style="font-family:'Playfair Display',serif; font-size:2rem; color:#fff; margin:0 0 12px;">
        Ready to Explore?
    </h2>
    <p style="color:#d8b4fe; font-size:1rem; font-weight:300; margin:0 0 30px;">
        Answer a few quick questions and find your perfect destination in seconds.
    </p>
</div>
""", unsafe_allow_html=True)
col_l, col_c, col_r = st.columns([3, 2, 3])
with col_c:
    if st.button("Start Questionnaire →", use_container_width=True):
        st.switch_page("pages/TravelPlannerQuestionnaire.py")
