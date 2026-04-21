import streamlit as st
st.set_page_config(page_title="SmartTravel - Home", page_icon="🌆") #Tab Title & Icon

#Notes: Majority of Markdown Code is AI generated; this formatting looks nicer,
# however I'm not sure if we're allowed to use the complicated ones
# We can change back to the simpler version learned in class if needed, Hallo Yannis

#Page Title & Subheaders
st.markdown("<h2 style='color:#8a2be2;'>✨ AI Powered Travel Planning ✨</h2>", unsafe_allow_html=True) #adds purple subheader
st.title("Discover Your Perfect Destination with SmartTravel 🌍")
st.subheader("Let us guide you to unforgettable adventures tailored specifically to your travel preferences and dreams.")

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

#Website statistics
col1, col2, col3 = st.columns(3) #makes three columns for stats
with col1:
    st.title("🌍")
    st.markdown("<h3 style='color:#8a2be2;'> 500+ Destinations</h3>", unsafe_allow_html=True) #adds purple stat with icon
with col2:
    st.title("🔥")
    st.markdown("<h3 style='color:#8a2be2;'>98% Match Accuracy</h3>", unsafe_allow_html=True) #adds purple stat with icon
with col3:
    st.title("⭐")
    st.markdown("<h3 style='color:#8a2be2;'>50k+ Happy Travelers</h3>", unsafe_allow_html=True) #adds purple stat with icon


#add spacing with 400px distance (AI generated)
st.markdown("<div style='margin-top: 400px;'></div>", unsafe_allow_html=True)

#Discover Your Way Section
st.title("Discover Your Way")
st.subheader("Not sure where to start? Try one of these alternative ways to find your perfect destination:")
col1, col2 = st.columns(2)
with col1: # Code AI generated: Formats the left column with a button and description for "Find by Photos" feature, centered with background and square
    st.markdown("""
        <div style='border: 2px solid #6a0dad; border-radius: 14px; padding: 18px; text-align: center; background: #f8f1ff; max-width: 360px; margin: 0 auto;'>
            <img src='https://cdn-icons-png.flaticon.com/512/3656/3656900.png' width='80' style='display:block; margin: 0 auto 12px;' />
            <h3 style='color:#6a0dad; margin: 0 0 8px;'>Surprise Me!</h3>
            <p style='color:#4c1d95; font-size: 12px; margin: 0 0 12px;'>Feeling adventurous? Let us surprise you with a random destination and discover something unexpected.</p>
            <div style='display:flex; justify-content:center;'>
                <button style='background-color:#6a0dad; color:white; border:none; border-radius:8px; padding:8px 18px; cursor:pointer;'>🎲 Surprise Me!</button>
            </div>
        </div>
    """, unsafe_allow_html=True)
    #Markdown Notes: H3 = Level 3 heading, P = paragraph, div = container for button and description, border = purple border, border-radius = rounded corners, padding = space inside container, text-align = center content, background = light purple background, max-width = limits square width, margin = centers square

with col2: # Code AI generated: Formats the "Find by Photos!" button with a purple border, rounded corners, and an image icon. The button is centered and has a description above it.
    st.markdown("""
        <div style='border: 2px solid #6a0dad; border-radius: 14px; padding: 18px; text-align: center; background: #f8f1ff; max-width: 360px; margin: 0 auto;'>
            <img src='https://www.freeiconspng.com/thumbs/camera-icon/camera-icon-21.png' width='80' style='display:block; margin: 0 auto 12px;' />
            <h3 style='color:#6a0dad; margin: 0 0 8px;'>Find by Photos!</h3>
            <p style='color:#4c1d95; font-size: 12px; margin: 0 0 12px;'>Upload up to 3 photos of places you love and we'll find similar destinations for your next adventure.</p>
            <div style='display:flex; justify-content:center;'>
                <button style='background-color:#6a0dad; color:white; border:none; border-radius:8px; padding:8px 18px; cursor:pointer;'>📷 Find by Photos!</button>
            </div>
        </div>
    """, unsafe_allow_html=True)


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
