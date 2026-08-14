import streamlit as st

# 1. Page Config
st.set_page_config(
    page_title="AGRIQN AI - Quantum & Crop AI Doctor",
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
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1100px;
    }
    h1 { color: #6EE7B7 !important; font-size: 36px !important; }
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
    
    # B. Language Selector
    report_lang = st.selectbox("🌐 भाषा (Language):", ["हिंदी (Hindi)", "English"])
    is_hindi = "हिंदी" in report_lang

    st.markdown("### 🔍 सेवा चुनें (Select Feature)")

    # C. Other Features List (Radio Button Navigation)
    menu_choice = st.radio(
        label="Navigation Menu",
        options=[
            "🪴 मिट्टी पोषण जांच (Soil Health)", 
            "📸 फसल रोग पहचान (Crop Disease Scanner)",
            "📊 सर्वर स्थिति (System Insights)"
        ],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.info("💡 **AGRIQN Helpline:**\n\n+91 8269967777\n\nकिसान का अपना डिजिटल डॉक्टर।")

# ---------------------------------------------------------
# 3. MAIN PAGE TOP HEADER (Logo Box & Branding on Top Right)
# ---------------------------------------------------------
head_col1, head_col2 = st.columns([3, 1])

with head_col1:
    # मुख्य पेज का शीर्षक/स्वागत संदेश (अपेक्षा अनुसार छोड़ सकते हैं या रख सकते हैं)
    pass

with head_col2:
    # Top Right Box for Logo and AGRIQN AI Brand Title
    try:
        st.image("logo_temp1.PNG", use_container_width=True)
    except Exception:
        pass
    st.markdown(
        "<h2 style='text-align: center; color: #047857; margin-top: -10px; font-weight: bold;'>AGRIQN AI</h2>", 
        unsafe_allow_html=True
    )

st.markdown("---")

# ---------------------------------------------------------
# 4. DYNAMIC MODULE RENDERING
# ---------------------------------------------------------
if menu_choice == "🪴 मिट्टी पोषण जांच (Soil Health)":
    if 'soil_health' in globals():
        soil_health.render_soil_module(is_hindi)

elif menu_choice == "📸 फसल रोग पहचान (Crop Disease Scanner)":
    if 'disease_detector' in globals():
        disease_detector.render_disease_module(is_hindi)

else:
    if 'render_insights_page' in globals():
        render_insights_page(is_hindi)

# ---------------------------------------------------------
# 5. GLOBAL FOOTER
# ---------------------------------------------------------
if 'render_footer' in globals():
    render_footer()
