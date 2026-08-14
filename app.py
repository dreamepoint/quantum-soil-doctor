import streamlit as st
from footer import render_footer
from insights import render_insights_page
import soil_health
import disease_detector

# 1. Page Config
st.set_page_config(
    page_title="AGRIQN - Quantum & Crop AI Doctor",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Social Media Meta Tags
st.markdown("""
    <head>
        <meta property="og:type" content="website">
        <meta property="og:title" content="AGRIQN — Quantum AI Soil & Crop Doctor">
        <meta property="og:description" content="भारतीय किसानों के लिए ऑल-इन-वन एग्री AI प्लेटफ़ॉर्म।">
    </head>
""", unsafe_allow_html=True)

# Upgraded Premium Modern Styling
st.markdown("""
    <style>
    /* 1. Main Background & Spacing Fix */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1100px;
    }
    
    /* 2. Header Title Styling */
    h1 {
        color: #6EE7B7 !important; /* Bright Emerald for Dark Theme */
        font-size: 36px !important;
        font-weight: 800 !important;
        text-align: center;
        letter-spacing: 1px;
        margin-bottom: 2px !important;
    }
    h3 {
        color: #3B82F6 !important;
        font-size: 20px !important;
        text-align: center;
        margin-top: 0px !important;
        margin-bottom: 25px !important;
    }

    /* 3. Streamlit Native Input Labels Fix */
    div[data-widget="stNumberInput"] label, div[data-widget="stSelectbox"] label {
        color: #F3F4F6 !important;
        font-weight: 600 !important;
        font-size: 15px !important;
    }

    /* 4. Glassmorphism Card Effect for Form Container */
    div[data-testid="stForm"] {
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background: rgba(30, 41, 59, 0.7) !important;
        border-radius: 16px !important;
        padding: 25px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
    }

    /* 5. Full-Width Glowing Primary Button Fix */
    div.stButton > button:first-child, div[data-testid="stFormSubmitButton"] > button {
        width: 100% !important;
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        color: #FFFFFF !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        padding: 14px 20px !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 14px 0 rgba(16, 185, 129, 0.39) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:first-child:hover, div[data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(16, 185, 129, 0.55) !important;
    }

    /* 6. Sidebar Improvements */
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# 2. Sidebar Setup
st.sidebar.image("logo_temp1.PNG", width=180)
st.sidebar.markdown("---")

report_lang = st.sidebar.selectbox("🌐 भाषा (Language):", ["हिंदी (Hindi)", "English"])
is_hindi = "हिंदी" in report_lang

st.sidebar.markdown("### 🔍 सेवा चुनें (Select Feature)")

# 🌟 Menu Option Fix: label_visibility="collapsed" जोड़ा गया है ताकि warning न आये
menu_choice = st.sidebar.radio(
    label="Navigation Menu",
    options=[
        "🪴 मिट्टी पोषण जांच (Soil Health)", 
        "📸 फसल रोग पहचान (Crop Disease Scanner)",
        "📊 सर्वर स्थिति (System Insights)"
    ],
    index=0,
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **AGRIQN Helpline:**\n\n+91 8269967777\n\nकिसान का अपना डिजिटल डॉक्टर।")

# 3. Dynamic Rendering
if menu_choice == "🪴 मिट्टी पोषण जांच (Soil Health)":
    soil_health.render_soil_module(is_hindi)
elif menu_choice == "📸 फसल रोग पहचान (Crop Disease Scanner)":
    disease_detector.render_disease_module(is_hindi)
else:
    # 🌟 सिस्टम स्थिति वाला पेज रेंडर होगा
    render_insights_page(is_hindi)

# 4. Global Footer
render_footer()
