import streamlit as st

# 1. Page Config
st.set_page_config(
    page_title="AGRIQN - Quantum & Crop AI Doctor",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Safe Module Imports
try:
    from footer import render_footer
    from insights import render_insights_page
    import soil_health
    import disease_detector
except Exception as e:
    st.error(f"⚠️ Import Error: {e}")

# Styling
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1100px;
    }
    h1 { color: #6EE7B7 !important; font-size: 36px !important; text-align: center; }
    section[data-testid="stSidebar"] { background-color: #0F172A !important; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. SIDEBAR SETUP (Logo Top + Navigation List)
# ---------------------------------------------------------
with st.sidebar:
    # A. Sidebar Top Logo
    try:
        st.image("logo_temp1.PNG", use_container_width=True)
    except Exception:
        st.title("🌾 AGRIQN AI")

    st.markdown("---")

report_lang = st.sidebar.selectbox("🌐 भाषा (Language):", ["हिंदी (Hindi)", "English"])
is_hindi = "हिंदी" in report_lang

st.sidebar.markdown("### 🔍 सेवा चुनें (Select Feature)")

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
    if 'soil_health' in globals():
        soil_health.render_soil_module(is_hindi)
elif menu_choice == "📸 फसल रोग पहचान (Crop Disease Scanner)":
    if 'disease_detector' in globals():
        disease_detector.render_disease_module(is_hindi)
else:
    if 'render_insights_page' in globals():
        render_insights_page(is_hindi)

# 4. Global Footer
if 'render_footer' in globals():
    render_footer()
