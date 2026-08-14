import streamlit as st
from footer import render_footer
from insights import render_insights_page
import soil_health
import disease_detector

# 1. Page Config
st.set_page_config(
    page_title="AGRIQN - Quantum & Crop AI Doctor",
    page_icon="logo.PNG",  # 👈 यहाँ '🌾' की जगह 'logo.png' लिख दें
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

# Styling
st.markdown("""
    <style>
    .main { padding: 10px; }
    h1 { color: #1E3A8A !important; font-size: 28px !important; text-align: center; font-weight: bold; margin-bottom: 5px; }
    h3 { color: #10B981 !important; font-size: 18px !important; text-align: center; margin-top: 0px; margin-bottom: 20px; }
    .custom-card { padding: 15px; border-radius: 12px; margin-bottom: 15px; font-size: 16px; box-shadow: 0px 2px 5px rgba(0,0,0,0.05); }
    .card-success { background-color: #DCFCE7; border-left: 6px solid #16A34A; color: #14532D; }
    .card-warning { background-color: #FEF3C7; border-left: 6px solid #D97706; color: #78350F; }
    .card-error { background-color: #FEE2E2; border-left: 6px solid #DC2626; color: #7F1D1D; }
    .card-info { background-color: #E0F2FE; border-left: 6px solid #0284C7; color: #0C4A6E; }
    div.stButton > button:first-child {
        width: 100% !important; background-color: #10B981 !important; color: white !important;
        font-size: 18px !important; font-weight: bold !important; padding: 12px 0px !important; border-radius: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Sidebar Setup
st.sidebar.image("logo.PNG", use_container_width=True)
st.sidebar.markdown("# 🌾 AGRIQN AI")
st.sidebar.markdown("---")

report_lang = st.sidebar.selectbox("🌐 भाषा (Language):", ["हिंदी (Hindi)", "English"])
is_hindi = "हिंदी" in report_lang

st.sidebar.markdown("### 🔍 सेवा चुनें (Select Feature)")

# 🌟 3rd विकल्प (System Insights)
menu_choice = st.sidebar.radio(
    "",
    [
        "🪴 मिट्टी पोषण जांच (Soil Health)", 
        "📸 फसल रोग पहचान (Crop Disease Scanner)",
        "📊 सर्वर स्थिति (System Insights)"
    ],
    index=0
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
