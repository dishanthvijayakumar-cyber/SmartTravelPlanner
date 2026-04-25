import streamlit as st
import random
from database import get_destinations

st.set_page_config(page_title="SmartTravel - Home", page_icon="🌆", layout="wide")

# ── AI-ASSISTED REDESIGN ────────────────────────────────────────────────────
# Visual design and CSS were generated with the help of Claude (Anthropic AI).
# All Python logic, page structure, and routing written by the team.
# ────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #f0ece4 !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] > .main { background: transparent !important; }
[data-testid="stHeader"] { background: transparent !important; }
section[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Hero ── */
.hero {
    position: relative;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    overflow: hidden;
    padding: 80px 24px;
    background:
        radial-gradient(ellipse 80% 60% at 50% 0%, rgba(255,160,60,0.18) 0%, transparent 70%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(70,130,180,0.15) 0%, transparent 60%),
        #0a0a0f;
}

.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        radial-gradient(circle, rgba(255,255,255,0.08) 1px, transparent 1px);
    background-size: 40px 40px;
    mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 30%, transparent 100%);
    pointer-events: none;
}

.eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #f0a040;
    margin-bottom: 24px;
    opacity: 0;
    animation: fadeUp 0.8s ease 0.1s forwards;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(52px, 8vw, 110px);
    font-weight: 900;
    line-height: 0.95;
    color: #f0ece4;
    margin-bottom: 32px;
    opacity: 0;
    animation: fadeUp 0.9s ease 0.25s forwards;
}

.hero-title em {
    font-style: italic;
    color: #f0a040;
}

.hero-subtitle {
    font-size: clamp(15px, 2vw, 18px);
    font-weight: 300;
    color: #a09a90;
    max-width: 520px;
    line-height: 1.7;
    margin-bottom: 52px;
    opacity: 0;
    animation: fadeUp 1s ease 0.4s forwards;
}

.hero-cta {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    justify-content: center;
    opacity: 0;
    animation: fadeUp 1s ease 0.55s forwards;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(28px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Stats bar ── */
.stats-bar {
    display: flex;
    justify-content: center;
    gap: 0;
    padding: 0 24px;
    margin: 0;
    background: #111118;
    border-top: 1px solid rgba(255,255,255,0.06);
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

.stat-item {
    flex: 1;
    max-width: 260px;
    padding: 36px 24px;
    text-align: center;
    border-right: 1px solid rgba(255,255,255,0.06);
}
.stat-item:last-child { border-right: none; }

.stat-number {
    font-family: 'Playfair Display', serif;
    font-size: 42px;
    font-weight: 700;
    color: #f0a040;
    line-height: 1;
    margin-bottom: 6px;
}

.stat-label {
    font-size: 12px;
    font-weight: 400;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6a6560;
}

/* ── Section ── */
.section {
    padding: 120px 48px;
    max-width: 1200px;
    margin: 0 auto;
}

.section-eyebrow {
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: #f0a040;
    margin-bottom: 16px;
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(36px, 5vw, 60px);
    font-weight: 700;
    line-height: 1.1;
    color: #f0ece4;
    margin-bottom: 20px;
}

.section-sub {
    font-size: 16px;
    font-weight: 300;
    color: #7a746e;
    max-width: 480px;
    line-height: 1.7;
}

/* ── Feature grid ── */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2px;
    margin-top: 72px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    overflow: hidden;
}

.feature-card {
    background: #0e0e16;
    padding: 40px 32px;
    transition: background 0.3s ease;
}

.feature-card:hover { background: #14141e; }

.feature-icon {
    font-size: 32px;
    margin-bottom: 20px;
    display: block;
}

.feature-name {
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    font-weight: 700;
    color: #f0ece4;
    margin-bottom: 10px;
}

.feature-desc {
    font-size: 13px;
    font-weight: 300;
    color: #6a6560;
    line-height: 1.7;
}

/* ── Surprise card ── */
.surprise-section {
    background: linear-gradient(135deg, #111118 0%, #16101a 100%);
    border-top: 1px solid rgba(255,255,255,0.06);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding: 100px 48px;
    text-align: center;
}

.surprise-badge {
    display: inline-block;
    background: rgba(240,160,64,0.12);
    border: 1px solid rgba(240,160,64,0.3);
    color: #f0a040;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    padding: 6px 18px;
    border-radius: 999px;
    margin-bottom: 28px;
}

/* ── CTA section ── */
.cta-section {
    background: #f0ece4;
    padding: 100px 48px;
    text-align: center;
}

.cta-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(36px, 5vw, 64px);
    font-weight: 900;
    color: #0a0a0f;
    margin-bottom: 16px;
    line-height: 1.05;
}

.cta-sub {
    font-size: 16px;
    color: #6a6560;
    margin-bottom: 48px;
    font-weight: 300;
}

/* ── Button overrides ── */
.stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    border-radius: 6px !important;
    padding: 14px 32px !important;
    transition: all 0.2s ease !important;
    border: none !important;
    cursor: pointer !important;
}

/* Primary button (first button per section) */
.hero .stButton > button,
.primary-btn .stButton > button {
    background: #f0a040 !important;
    color: #0a0a0f !important;
}

.hero .stButton > button:hover,
.primary-btn .stButton > button:hover {
    background: #e8943a !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(240,160,64,0.3) !important;
}

/* Ghost button */
.ghost-btn .stButton > button {
    background: transparent !important;
    color: #f0ece4 !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}

.ghost-btn .stButton > button:hover {
    border-color: rgba(255,255,255,0.5) !important;
    background: rgba(255,255,255,0.04) !important;
}

/* Dark button (on light bg) */
.dark-btn .stButton > button {
    background: #0a0a0f !important;
    color: #f0ece4 !important;
}
.dark-btn .stButton > button:hover {
    background: #1a1a24 !important;
    transform: translateY(-2px) !important;
}

/* Divider */
.divider {
    height: 1px;
    background: rgba(255,255,255,0.06);
    margin: 0;
}

/* Footer */
.footer {
    background: #0a0a0f;
    padding: 32px 48px;
    text-align: center;
    color: #3a3a40;
    font-size: 12px;
    border-top: 1px solid rgba(255,255,255,0.04);
}
</style>
""", unsafe_allow_html=True)


# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <p class="eyebrow">✦ AI-Powered Travel Planning ✦</p>
    <h1 class="hero-title">Your next<br><em>adventure</em><br>awaits.</h1>
    <p class="hero-subtitle">
        SmartTravel matches your personality with destinations you'll love —
        in seconds, not hours.
    </p>
</div>
""", unsafe_allow_html=True)

# Hero buttons
col_gap, col_a, col_b, col_gap2 = st.columns([3, 1, 1, 3])
with col_a:
    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
    if st.button("Start Your Journey ✈️", use_container_width=True):
        st.switch_page("pages/TravelPlannerQuestionnaire.py")
    st.markdown('</div>', unsafe_allow_html=True)
with col_b:
    st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
    if st.button("View Dashboard 📊", use_container_width=True):
        st.switch_page("pages/TravelPlannerDashboard.py")
    st.markdown('</div>', unsafe_allow_html=True)


# ── STATS BAR ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-bar">
    <div class="stat-item">
        <div class="stat-number">500+</div>
        <div class="stat-label">Destinations</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">98%</div>
        <div class="stat-label">Match Accuracy</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">50k+</div>
        <div class="stat-label">Happy Travelers</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── FEATURES SECTION ─────────────────────────────────────────────────────────
st.markdown("""
<div class="section">
    <p class="section-eyebrow">Why SmartTravel</p>
    <h2 class="section-title">Built different.<br>By design.</h2>
    <p class="section-sub">Every feature was crafted to make finding your perfect trip effortless and genuinely exciting.</p>

    <div class="feature-grid">
        <div class="feature-card">
            <span class="feature-icon">🤖</span>
            <div class="feature-name">AI Recommendations</div>
            <div class="feature-desc">Personalized destination matches based on your unique travel style, budget, and interests.</div>
        </div>
        <div class="feature-card">
            <span class="feature-icon">🎯</span>
            <div class="feature-name">Smart Match Scores</div>
            <div class="feature-desc">See exactly how well each destination aligns with your preferences — no guesswork.</div>
        </div>
        <div class="feature-card">
            <span class="feature-icon">⚡</span>
            <div class="feature-name">Instant Results</div>
            <div class="feature-desc">From a few quick questions to a full recommendation list in under 10 seconds.</div>
        </div>
        <div class="feature-card">
            <span class="feature-icon">🗺️</span>
            <div class="feature-name">Detailed Insights</div>
            <div class="feature-desc">Activities, budget breakdowns, best seasons, and weather data for every destination.</div>
        </div>
        <div class="feature-card">
            <span class="feature-icon">✅</span>
            <div class="feature-name">Trusted Information</div>
            <div class="feature-desc">Curated recommendations from verified travel experts and real traveler reviews.</div>
        </div>
        <div class="feature-card">
            <span class="feature-icon">🧩</span>
            <div class="feature-name">Drag & Drop Planning</div>
            <div class="feature-desc">Build the perfect itinerary visually with our intuitive trip-planning board.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ── SURPRISE ME SECTION ───────────────────────────────────────────────────────
st.markdown("""
<div class="surprise-section">
    <div class="surprise-badge">✦ Feeling Lucky? ✦</div>
    <h2 style="font-family:'Playfair Display',serif; font-size:clamp(32px,5vw,56px); font-weight:700; color:#f0ece4; margin-bottom:16px; line-height:1.1;">
        Let fate choose<br><em style="color:#f0a040;">your destination.</em>
    </h2>
    <p style="font-size:16px; font-weight:300; color:#6a6560; max-width:420px; margin:0 auto 44px; line-height:1.7;">
        Skip the browsing. Hit one button and we'll drop you somewhere unexpected — and unforgettable.
    </p>
</div>
""", unsafe_allow_html=True)

_, col_center, _ = st.columns([2, 1, 2])
with col_center:
    st.markdown('<div style="background:#111118; padding:0 0 60px; text-align:center;">', unsafe_allow_html=True)
    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
    if st.button("🎲  Surprise Me!", use_container_width=True):
        destinations = get_destinations()
        random_destination = random.choice(destinations)
        st.session_state.selected_destination = random_destination
        st.switch_page("pages/TravelPlannerDashboard.py")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ── FINAL CTA SECTION ─────────────────────────────────────────────────────────
st.markdown("""
<div class="cta-section">
    <h2 class="cta-title">Ready to find<br>your place?</h2>
    <p class="cta-sub">Answer a few quick questions — we'll handle the rest.</p>
</div>
""", unsafe_allow_html=True)

_, col_cta, _ = st.columns([2, 1, 2])
with col_cta:
    st.markdown('<div style="background:#f0ece4; padding:0 0 80px; text-align:center;">', unsafe_allow_html=True)
    st.markdown('<div class="dark-btn">', unsafe_allow_html=True)
    if st.button("Start Questionnaire →", use_container_width=True):
        st.switch_page("pages/TravelPlannerQuestionnaire.py")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    SmartTravel &nbsp;·&nbsp; AI-Powered Destination Matching &nbsp;·&nbsp; 2025
</div>
""", unsafe_allow_html=True)
