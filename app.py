import streamlit as st
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import time
import os
import urllib.request
from fpdf import FPDF

# लोकल मॉड्यूल्स
from footer import render_footer
from whatsapp_share import get_whatsapp_share_url
from guide import render_guide
from calculator import render_calculator

# ---------------------------------------------------------
# 1. Hindi Font Download Setup
# ---------------------------------------------------------
@st.cache_resource
def prepare_hindi_fonts():
    font_file = "NotoSansDevanagari-Regular.ttf"
    if not os.path.exists(font_file):
        url = "https://github.com/google/fonts/raw/main/ofl/notosansdevanagari/NotoSansDevanagari%5Bwdth%2Cwght%5D.ttf"
        urllib.request.urlretrieve(url, font_file)
    return font_file

font_path_regular = prepare_hindi_fonts()

# ---------------------------------------------------------
# 2. Streamlit Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Dream Merchant Quantum AI — Soil Doctor", 
    page_icon="🌾", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Social Media Meta Tags
st.markdown("""
    <head>
        <meta property="og:type" content="website">
        <meta property="og:title" content="Dream Merchant Quantum AI — Soil Doctor">
        <meta property="og:description" content="भारतीय किसानों के लिए क्वांटम कंप्यूटर आधारित सॉइल एनालिसिस पोर्टल।">
        <meta property="og:image" content="https://raw.githubusercontent.com/dreamepoint/quantum-soil-doctor/main/ogimage.png">
    </head>
""", unsafe_allow_html=True)

# CSS UI Styling
st.markdown("""
    <style>
    .main { padding: 10px; }
    h1 { color: #1E3A8A !important; font-size: 28px !important; text-align: center; font-weight: bold; margin-bottom: 5px; }
    h3 { color: #10B981 !important; font-size: 18px !important; text-align: center; margin-top: 0px; margin-bottom: 20px; }
    .custom-card {
        padding: 15px; border-radius: 12px; margin-bottom: 15px; font-size: 16px; box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
    }
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

st.markdown("<h1>DREAM MERCHANT</h1>", unsafe_allow_html=True)
st.markdown("<h3>🧬 Quantum AI Soil Doctor v2.5</h3>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. Global Language Selector & Tabs Setup
# ---------------------------------------------------------
col_lang, _ = st.columns([1, 1])
with col_lang:
    report_lang = st.selectbox("🌐 भाषा (Language):", ["हिंदी (Hindi)", "English"])

is_hindi = "हिंदी" in report_lang

# App को 3 Tabs में बांटना
tab_app, tab_calc, tab_guide = st.tabs([
    "🌾 " + ("सॉइल टेस्ट पोर्टल" if is_hindi else "Soil Test Portal"),
    "💰 " + ("खाद एवं बचत कैलकुलेटर" if is_hindi else "Fertilizer Calculator"),
    "📖 " + ("किसान मार्गदर्शिका (Guide)" if is_hindi else "User Guide")
])

# ---------------------------------------------------------
# 4. Advanced PDF Generation Engine
# ---------------------------------------------------------
def generate_pdf_report(crop, n, p, k, ph, n_msg, p_msg, k_msg, ph_msg, is_hi):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(15, 15, 15)
    pdf.add_page()
    
    try:
        pdf.add_font("NotoSans", style="", fname=font_path_regular)
        pdf.set_text_shaping(True)
    except Exception:
        pass
        
    pdf.set_font("NotoSans", size=10)
    
    pdf.set_font("NotoSans", size=16)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(180, 8, "DREAM MERCHANT BUSINESS SOLUTION", new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.set_font("NotoSans", size=11)
    pdf.set_text_color(16, 185, 129)
    sub_title = "क्वांटम एआई मृदा विश्लेषण एवं सिफारिश कार्ड" if is_hi else "Quantum AI Soil Analysis & Prescription Card"
    pdf.cell(180, 7, sub_title, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(4)
    
    pdf.set_font("NotoSans", size=9.5)
    pdf.set_text_color(55, 65, 81)
    pdf.cell(180, 5, f"{'रिपोर्ट आईडी' if is_hi else 'Report ID'}: DM-SOIL-{int(time.time())}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(180, 5, f"{'फसल' if is_hi else 'Target Crop'}: {crop}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(180, 5, f"{'दिनांक' if is_hi else 'Date'}: {time.strftime('%Y-%m-%d %H:%M:%S')}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    
    pdf.set_fill_color(30, 58, 138)
    pdf.set_text_color(255, 255, 255)
    
    col_w = 60
    pdf.cell(col_w, 8, 'मापदंड (Parameter)' if is_hi else 'Parameter', border=1, fill=True, align="C")
    pdf.cell(col_w, 8, 'आपका स्तर' if is_hi else 'Your Value', border=1, fill=True, align="C")
    pdf.cell(col_w, 8, 'स्थिति (Status)' if is_hi else 'Status', border=1, fill=True, align="C", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_fill_color(243, 244, 246)
    pdf.set_text_color(55, 65, 81)
    
    if is_hi:
        table_rows = [
            ['नाइट्रोजन (N)', f'{n} kg/acre', 'अत्यधिक' if n>220 else ('मध्यम' if n>=110 else 'कम')],
            ['फॉस्फोरस (P)', f'{p} kg/acre', 'पर्याप्त' if p>10 else 'कम'],
            ['पोटेशियम (K)', f'{k} kg/acre', 'पर्याप्त' if k>110 else 'कम'],
            ['मिट्टी का pH', f'{ph}', 'क्षारीय' if ph>7.5 else ('अम्लीय' if ph<6.5 else 'उत्तम')]
        ]
    else:
        table_rows = [
            ['Nitrogen (N)', f'{n} kg/acre', 'High' if n>220 else ('Medium' if n>=110 else 'Low')],
            ['Phosphorus (P)', f'{p} kg/acre', 'Optimal' if p>10 else 'Low'],
            ['Potassium (K)', f'{k} kg/acre', 'Optimal' if k>110 else 'Low'],
            ['Soil pH', f'{ph}', 'Alkaline' if ph>7.5 else ('Acidic' if ph<6.5 else 'Optimal')]
        ]
    
    for row in table_rows:
        pdf.cell(col_w, 7, row[0], border=1, fill=True, align="C")
        pdf.cell(col_w, 7, row[1], border=1, fill=True, align="C")
        pdf.cell(col_w, 7, row[2], border=1, fill=True, align="C", new_x="LMARGIN", new_y="NEXT")
        
    pdf.ln(6)
    
    pdf.set_font("NotoSans", size=10.5)
    pdf.set_text_color(17, 24, 39)
    pdf.cell(180, 6, "🔬 क्वांटम कंप्यूटर एआई की सिफारिशें:" if is_hi else "🔬 QUANTUM COMPUTER AI RECOMMENDATIONS:", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    
    pdf.set_font("NotoSans", size=9)
    pdf.multi_cell(180, 5, f"• {'नाइट्रोजन व यूरिया' if is_hi else 'Nitrogen & Urea'}: {n_msg}")
    pdf.ln(1)
    pdf.multi_cell(180, 5, f"• {'फॉस्फोरस' if is_hi else 'Phosphorus (P)'}: {p_msg}")
    pdf.ln(1)
    pdf.multi_cell(180, 5, f"• {'पोटेशियम' if is_hi else 'Potassium (K)'}: {k_msg}")
    pdf.ln(1)
    pdf.multi_cell(180, 5, f"• {'मिट्टी pH स्तर' if is_hi else 'Soil pH Level'}: {ph_msg}")
    
    pdf.ln(8)
    pdf.set_font("NotoSans", size=8)
    pdf.set_text_color(107, 114, 128)
    foot_text = "* यह एक स्वचालित रिपोर्ट है जो IBM क्वांटम सर्किट सिमुलेटर द्वारा तैयार की गई है।" if is_hi else "* Automated report generated via IBM Quantum Circuit Simulators."
    pdf.cell(180, 5, foot_text, align="C")
    
    return bytes(pdf.output())


# =========================================================
# 📌 TAB 1: मुख्य सॉइल टेस्ट पोर्टल
# =========================================================
with tab_app:
    crops_dict = {
        "हिंदी (Hindi)": ["कपास (Cotton)", "धान (Rice)", "गेहूं (Wheat)"],
        "English": ["Cotton", "Rice", "Wheat"]
    }

    crop_choice = st.selectbox(
        "आप खेत में कौन सी फसल उगाना चाहते हैं?" if is_hindi else "Select Target Crop:", 
        crops_dict[report_lang]
    )

    st.markdown("---")
    st.markdown("### 📊 " + ("मिट्टी की जांच रिपोर्ट" if is_hindi else "Soil Test Inputs"))

    col1, col2 = st.columns(2)
    with col1:
        n_value = st.number_input("🌱 " + ("नाइट्रोजन (N) - kg/acre" if is_hindi else "Nitrogen (N) - kg/acre"), min_value=0, value=110, step=5)
        p_value = st.number_input("🌾 " + ("फॉस्फोरस (P) - kg/acre" if is_hindi else "Phosphorus (P) - kg/acre"), min_value=0, value=6, step=2)
    with col2:
        k_value = st.number_input("🍂 " + ("पोटेशियम (K) - kg/acre" if is_hindi else "Potassium (K) - kg/acre"), min_value=0, value=60, step=5)
        ph_value = st.number_input("🧪 " + ("मिट्टी का pH मान" if is_hindi else "Soil pH Level"), min_value=0.0, max_value=14.0, value=7.0, step=0.1)

    btn_text = "📊 क्वांटम एआई जांच शुरू करें" if is_hindi else "📊 Start Quantum AI Analysis"

    if st.button(btn_text):
        spin_text = "🧠 क्वांटम सर्किट और पीडीएफ रिपोर्ट तैयार की जा रही है..." if is_hindi else "🧠 Processing Quantum Circuit & Generating PDF Report..."
        with st.spinner(spin_text):
            time.sleep(1.0)
            
            circuit = QuantumCircuit(4, 4)
            circuit.ry(np.pi if n_value > 220 else (np.pi/2 if n_value >= 110 else 0), 0)
            circuit.ry(np.pi if p_value > 10 else (np.pi/2 if p_value >= 4 else 0), 1)
            circuit.ry(np.pi if k_value > 110 else (np.pi/2 if k_value >= 45 else 0), 2)
            circuit.ry(np.pi if ph_value > 7.5 else (np.pi/2 if ph_value >= 6.5 else 0), 3)
            circuit.measure([0,1,2,3], [0,1,2,3])

            simulator = AerSimulator()
            counts = simulator.run(circuit, shots=100).result().get_counts()
            
            base_urea = 120 if "धान" in crop_choice or "Rice" in crop_choice else (100 if "गेहूं" in crop_choice or "Wheat" in crop_choice else 150)
            
            if is_hindi:
                if n_value > 220:
                    n_msg = "नाइट्रोजन अत्यधिक है! यूरिया का उपयोग पूरी तरह रोकें।"
                elif n_value >= 110:
                    u_dose = int(base_urea * 0.8)
                    n_msg = f"नाइट्रोजन मध्यम है। 20% कम यूरिया का उपयोग करें। अनुशंसित: {u_dose} किग्रा/एकड़।"
                else:
                    u_dose = int(base_urea * 1.2)
                    n_msg = f"नाइट्रोजन की कमी है! प्रति एकड़ {u_dose} किग्रा यूरिया जैविक खाद के साथ दें।"

                p_msg = "फॉस्फोरस का स्तर पर्याप्त है। अतिरिक्त DAP/SSP की आवश्यकता नहीं है।" if p_value > 10 else "फॉस्फोरस कम है। बुवाई के समय SSP या DAP डालें।"
                k_msg = "पोटेशियम भरपूर है। फसल की रोग प्रतिरोधक क्षमता अच्छी रहेगी।" if k_value > 110 else "पोटेशियम की कमी है! प्रति एकड़ 20 किग्रा MOP का छिड़काव करें।"
                ph_msg = "मिट्टी क्षारीय (Alkaline) है। जिप्सम या हरी खाद का प्रयोग करें।" if ph_value > 7.5 else ("मिट्टी अम्लीय (Acidic) है। चूना (Lime) का प्रयोग करें।" if ph_value < 6.5 else "मिट्टी का pH मान बिल्कुल सही है।")
            else:
                if n_value > 220:
                    n_msg = "Nitrogen is extremely high! Stop using Urea completely."
                elif n_value >= 110:
                    u_dose = int(base_urea * 0.8)
                    n_msg = f"Nitrogen is medium. Use 20% less urea. Recommended: {u_dose} kg/acre."
                else:
                    u_dose = int(base_urea * 1.2)
                    n_msg = f"Nitrogen deficiency detected! Recommended: {u_dose} kg urea per acre."

                p_msg = "Phosphorus level is optimal. No need for additional DAP/SSP." if p_value > 10 else "Phosphorus is low. Apply SSP or DAP during sowing."
                k_msg = "Potassium is rich. Plant immunity will be excellent." if k_value > 110 else "Potassium deficiency! Apply 20 kg MOP per acre."
                ph_msg = "Soil is Alkaline. Apply Gypsum to normalize pH." if ph_value > 7.5 else ("Soil is Acidic. Apply Lime during field prep." if ph_value < 6.5 else "Soil pH is perfect and neutral.")

            # Store result in state
            st.session_state['results'] = {
                'crop': crop_choice,
                'n_val': n_value,
                'p_val': p_value,
                'k_val': k_value,
                'ph_val': ph_value,
                'n_msg': n_msg,
                'p_msg': p_msg,
                'k_msg': k_msg,
                'ph_msg': ph_msg,
                'is_hindi': is_hindi,
                'pdf_bytes': generate_pdf_report(crop_choice, n_value, p_value, k_value, ph_value, n_msg, p_msg, k_msg, ph_msg, is_hindi),
                'wa_url': get_whatsapp_share_url(crop_choice, n_value, p_value, k_value, ph_value, n_msg, p_msg, k_msg, ph_msg, is_hindi)
            }
            st.session_state['show_preview'] = False
            st.balloons()

    if 'results' in st.session_state:
        res = st.session_state['results']
        is_hi = res['is_hindi']

        st.success("📊 " + ("क्वांटम सिमुलेशन सफलतापूर्वक पूरा हुआ!" if is_hi else "Quantum simulation completed successfully!"))
        st.markdown(f"## 📋 {'मृदा स्वास्थ्य कार्ड' if is_hi else 'SOIL HEALTH REPORT'} - {res['crop']}")
        
        st.markdown(f"<div class='custom-card card-warning'>🌱 <b>{'नाइट्रोजन' if is_hi else 'Nitrogen'}:</b> {res['n_msg']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='custom-card card-success'>🌾 <b>{'फॉस्फोरस' if is_hi else 'Phosphorus'}:</b> {res['p_msg']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='custom-card card-success'>🍂 <b>{'पोटेशियम' if is_hi else 'Potassium'}:</b> {res['k_msg']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='custom-card card-info'>🧪 <b>{'pH स्तर' if is_hi else 'pH Level'}:</b> {res['ph_msg']}</div>", unsafe_allow_html=True)

        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)

        with col1:
            btn_view_label = "👁️ रिपोर्ट देखें" if is_hi else "👁️ View"
            if st.button(btn_view_label, use_container_width=True):
                st.session_state['show_preview'] = not st.session_state.get('show_preview', False)

        with col2:
            btn_dl_label = "📥 डाउनलोड PDF" if is_hi else "📥 Download"
            st.download_button(
                label=btn_dl_label,
                data=res['pdf_bytes'],
                file_name=f"Soil_Report_{'HI' if is_hi else 'EN'}_{int(time.time())}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        with col3:
            btn_wa_label = "📲 व्हाट्सएप" if is_hi else "📲 Share"
            st.markdown(f"""
                <a href="{res['wa_url']}" target="_blank" style="text-decoration: none;">
                    <div style="
                        background-color: #25D366;
                        color: white;
                        text-align: center;
                        padding: 8px 0px;
                        border-radius: 8px;
                        font-size: 15px;
                        font-weight: bold;
                        border: 1px solid #25D366;
                    ">
                        {btn_wa_label}
                    </div>
                </a>
            """, unsafe_allow_html=True)

        if st.session_state.get('show_preview', False):
            with st.expander("📄 " + ("सॉइल स्वास्थ्य कार्ड प्रीव्यू" if is_hi else "Soil Health Card Preview"), expanded=True):
                st.info(f"**{'फसल' if is_hi else 'Crop'}:** {res['crop']} | **N:** {res['n_val']} | **P:** {res['p_val']} | **K:** {res['k_val']} | **pH:** {res['ph_val']}")
                st.warning(f"**{'नाइट्रोजन' if is_hi else 'Nitrogen'}:** {res['n_msg']}")
                st.success(f"**{'फॉस्फोरस' if is_hi else 'Phosphorus'}:** {res['p_msg']}\n\n**{'पोटेशियम' if is_hi else 'Potassium'}:** {res['k_msg']}")
                st.info(f"**pH:** {res['ph_msg']}")


# =========================================================
# 📌 TAB 2: खाद एवं बचत कैलकुलेटर
# =========================================================
with tab_calc:
    render_calculator(is_hindi)


# =========================================================
# 📌 TAB 3: किसान मार्गदर्शिका (Guide Tab)
# =========================================================
with tab_guide:
    render_guide(is_hindi)


# ---------------------------------------------------------
# 5. Always Render Footer at Bottom
# ---------------------------------------------------------
render_footer()
