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
}
[data-testid="stHeader"] { background: transparent !important; }


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
#add spacing between buttons and stats with 150px distance (AI generated)
st.markdown("<div style='margin-top: 150px;'></div>", unsafe_allow_html=True)

#Website statistics (AI-generated)
st.markdown("""
<div style="display:flex; justify-content:center; gap:60px; flex-wrap:wrap;
     padding:30px 20px; background:rgba(255,255,255,0.05); border-radius:20px;
     border:1px solid rgba(192,132,252,0.2); max-width:800px; margin:0 auto;">
    <div style="text-align:center;">
        <div style="font-family:'Playfair Display',serif; font-size:2.2rem; font-weight:900; color:#f59e0b;">500+</div>
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

#add spacing with 400px distance (AI generated)
st.markdown("<div style='margin-top: 400px;'></div>", unsafe_allow_html=True)

#Discover Your Way Section
st.title("Discover Your Way")
st.subheader("Not sure where to start? Try an alternative way to find your perfect destination:")

col1, col2, col3 = st.columns([1,2,1]) #makes three columns for features, with middle column being larger
with col2: 
    with st.container(border=True):
        st.image("https://cdn-icons-png.flaticon.com/512/3656/3656900.png", width=80) #adds icon for "Surprise Me" feature
        st.subheader("Surprise Me!")
        st.write("Feeling adventurous? Let us surprise you with a random destination and discover something unexpected.")
        if st.button("🎲 Surprise Me!", use_container_width=False):
            destinations = get_destinations()
            random_destination = random.choice(destinations)
            st.session_state.selected_destination = random_destination
            st.switch_page("pages/TravelPlannerSurprise.py")
    


#add spacing with 400px distance (AI generated)
st.markdown("<div style='margin-top: 400px;'></div>", unsafe_allow_html=True)

#Why Choose SmartTravel Section
st.title("Why Choose SmartTravel?")
st.subheader("Experience the future of travel planning with our Intelligent platform")
col1, col2, col3 = st.columns(3)
with col1: # Code AI generated: Formats the first column with a purple border, rounded corners, and an image icon. The column is centered and has a description below the title.
    st.markdown("""
        <div style='border: 2px solid #6a0dad; border-radius: 14px; padding: 18px; text-align: center; background: #f8f1ff; max-width: 360px; margin: 0 auto;'>
            <img src='https://static.thenounproject.com/png/1568674-200.png' width='80' style='display:block; margin: 0 auto 12px;' />
            <h3 style='color:#6a0dad; margin: 0 0 8px;'>Detailed Insights</h3>
            <p style='color:#4c1d95; font-size: 12px; margin: 0;'>Explore activities, budget breakdowns, and weather data for every destination.</p>
        </div>
    """, unsafe_allow_html=True)
with col2: # Code AI generated: Formats the second column with a purple border, rounded corners, and an image icon. The column is centered and has a description below the title.
    st.markdown("""
        <div style='border: 2px solid #6a0dad; border-radius: 14px; padding: 18px; text-align: center; background: #f8f1ff; max-width: 360px; margin: 0 auto;'>
            <img src='https://cdn-icons-png.flaticon.com/512/861/861377.png' width='80' style='display:block; margin: 0 auto 12px;' />
            <h3 style='color:#6a0dad; margin: 0 0 8px;'>Trusted Information</h3>
            <p style='color:#4c1d95; font-size: 12px; margin: 0;'>Curated recommendations from verified travel experts and real travelers.</p>
        </div>
    """, unsafe_allow_html=True)
with col3: # Code AI generated: Formats the third column with a purple border, rounded corners, and an image icon. The column is centered and has a description below the title.    
    st.markdown("""
        <div style='border: 2px solid #6a0dad; border-radius: 14px; padding: 18px; text-align: center; background: #f8f1ff; max-width: 360px; margin: 0 auto;'>
            <img src='https://cdn-icons-png.flaticon.com/512/657/657104.png' width='80' style='display:block; margin: 0 auto 12px;' />
            <h3 style='color:#6a0dad; margin: 0 0 8px;'>Instant Results</h3>
            <p style='color:#4c1d95; font-size: 12px; margin: 0;'>Get your personalized travel recommendations in seconds, not hours.</p>
        </div>
    """, unsafe_allow_html=True) 
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True) #spacing between rows (AI generated)
col1, col2, col3 = st.columns(3)
with col1: # Code AI generated: Formats the first column with a purple border, rounded corners, and an image icon. The column is centered and has a description below the title.
    st.markdown("""
        <div style='border: 2px solid #6a0dad; border-radius: 14px; padding: 18px; text-align: center; background: #f8f1ff; max-width: 360px; margin: 0 auto;'>
            <img src='https://png.pngtree.com/png-clipart/20240725/original/pngtree-yellow-star-scribble-png-image_15635162.png' width='80' style='display:block; margin: 0 auto 12px;' />
            <h3 style='color:#6a0dad; margin: 0 0 8px;'>AI-Powered Recommendations</h3>
            <p style='color:#4c1d95; font-size: 12px; margin: 0;'>Get personalized destination suggestions based on your unique preferences and travel style.</p>
        </div>
    """, unsafe_allow_html=True)
with col2: # Code AI generated: Formats the second column with a purple border, rounded corners, and an image icon. The column is centered and has a description below the title.
    st.markdown("""
        <div style='border: 2px solid #6a0dad; border-radius: 14px; padding: 18px; text-align: center; background: #f8f1ff; max-width: 360px; margin: 0 auto;'>
            <img src='https://endlessicons.com/wp-content/uploads/2012/10/arrow-up-icon.png' width='80' style='display:block; margin: 0 auto 12px;' />
            <h3 style='color:#6a0dad; margin: 0 0 8px;'>Smart Match Scores</h3>
            <p style='color:#4c1d95; font-size: 12px; margin: 0;'>See how well each destination aligns with your interests with our intelligent scoring system.</p>
        </div>
    """, unsafe_allow_html=True)
with col3: # Code AI generated: Formats the third column with a purple border, rounded corners, and an image icon. The column is centered and has a description below the title.    
    st.markdown("""
        <div style='border: 2px solid #6a0dad; border-radius: 14px; padding: 18px; text-align: center; background: #f8f1ff; max-width: 360px; margin: 0 auto;'>
            <img src='https://cdn-icons-png.flaticon.com/512/554/554975.png' width='80' style='display:block; margin: 0 auto 12px;' />
            <h3 style='color:#6a0dad; margin: 0 0 8px;'>Drag & Drop Planning</h3>
            <p style='color:#4c1d95; font-size: 12px; margin: 0;'>Build your perfect itinerary with our intuitive drag-and-drop trip planner.</p>
        </div>
    """, unsafe_allow_html=True)

#spacing (AI generated)
st.markdown("<div style='margin-top: 400px;'></div>", unsafe_allow_html=True) 
col1, col2, col3 = st.columns(3)

#Ready to explore section
st.markdown("""
        <div style='border: 2px solid #6a0dad; border-radius: 14px; padding: 18px; text-align: center; background: #f8f1ff; max-width: 1000px; margin: 0 auto;'>
            <h3 style='color:#6a0dad; margin: 0 0 8px;'>Ready to Explore?</h3>
            <p style='color:#4c1d95; font-size: 12px; margin: 0;'>Answer a few quick questions and let us guide you to your perfect destination match in seconds.</p>
        </div>
    """, unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("Start Questionnaire"):
        st.switch_page("pages/TravelPlannerQuestionnaire.py")
