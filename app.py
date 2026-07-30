import streamlit as st
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import time
import io
import urllib.request
import os

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------------------------------------------------------
# 1. Hindi Font Registration (for UTF-8 Support in PDF)
# ---------------------------------------------------------
FONT_PATH = "NotoSansDevanagari-Regular.ttf"

@st.cache_resource
def load_hindi_font():
    if not os.path.exists(FONT_PATH):
        url = "https://github.com/google/fonts/raw/main/ofl/notosansdevanagari/NotoSansDevanagari%5Bwdth%2Cwght%5D.ttf"
        urllib.request.urlretrieve(url, FONT_PATH)
    pdfmetrics.registerFont(TTFont('HindiFont', FONT_PATH))

try:
    load_hindi_font()
    HINDI_SUPPORT = True
except Exception as e:
    HINDI_SUPPORT = False

# ---------------------------------------------------------
# 2. Streamlit Mobile-First Config & Meta Tags
# ---------------------------------------------------------
st.set_page_config(
    page_title="Dream Merchant Quantum AI — Soil Doctor", 
    page_icon="🌾", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Social Media Sharing Meta Tags (Permanent Raw Image URL)
st.markdown("""
    <head>
        <meta property="og:type" content="website">
        <meta property="og:title" content="Dream Merchant Quantum AI — Soil Doctor">
        <meta property="og:description" content="भारतीय किसानों के लिए क्वांटम कंप्यूटर आधारित सॉइल एनालिसिस पोर्टल।">
        <meta property="og:image" content="https://raw.githubusercontent.com/dreamepoint/quantum-soil-doctor/main/ogimage.png">
        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:image" content="https://raw.githubusercontent.com/dreamepoint/quantum-soil-doctor/main/ogimage.png">
    </head>
""", unsafe_allow_html=True)

# UI Styling
st.markdown("""
    <style>
    .main { padding: 10px; }
    h1 { color: #1E3A8A !important; font-size: 28px !important; text-align: center; font-weight: bold; margin-bottom: 5px; }
    h3 { color: #10B981 !important; font-size: 18px !important; text-align: center; margin-top: 0px; margin-bottom: 25px; }
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

# Header Branding
st.markdown("<h1>DREAM MERCHANT</h1>", unsafe_allow_html=True)
st.markdown("<h3>🧬 Quantum AI Soil Doctor v2.5</h3>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. Input Controls (Language & Crop Selection)
# ---------------------------------------------------------
col_lang, col_crop = st.columns(2)
with col_lang:
    report_lang = st.selectbox("🌐 रिपोर्ट की भाषा (Language):", ["हिंदी (Hindi)", "English"])

is_hindi = "हिंदी" in report_lang

crops_dict = {
    "हिंदी (Hindi)": ["कपास (Cotton)", "धान (Rice)", "गेहूं (Wheat)"],
    "English": ["Cotton", "Rice", "Wheat"]
}

with col_crop:
    crop_choice = st.selectbox(
        "आप खेत में कौन सी फसल उगाना चाहते हैं?" if is_hindi else "Select Target Crop:", 
        crops_dict[report_lang]
    )

st.markdown("---")
st.markdown("### 📊 " + ("मिट्टी की जांच रिपोर्ट" if is_hindi else "Soil Test Inputs"))

col1, col2 = st.columns(2)
with col1:
    n_value = st.number_input("🌱 " + ("नाइट्रोजन (N) - kg/ha" if is_hindi else "Nitrogen (N) - kg/ha"), min_value=0, value=280, step=10)
    p_value = st.number_input("🌾 " + ("फॉस्फोरस (P) - kg/ha" if is_hindi else "Phosphorus (P) - kg/ha"), min_value=0, value=15, step=5)
with col2:
    k_value = st.number_input("🍂 " + ("पोटेशियम (K) - kg/ha" if is_hindi else "Potassium (K) - kg/ha"), min_value=0, value=150, step=10)
    ph_value = st.number_input("🧪 " + ("मिट्टी का pH मान" if is_hindi else "Soil pH Level"), min_value=0.0, max_value=14.0, value=7.0, step=0.1)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. Multi-Language PDF Generation Function
# ---------------------------------------------------------
def generate_pdf_report(crop, n, p, k, ph, n_msg, p_msg, k_msg, ph_msg, is_hi):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    
    font_name = 'HindiFont' if (is_hi and HINDI_SUPPORT) else 'Helvetica'
    font_bold = 'HindiFont' if (is_hi and HINDI_SUPPORT) else 'Helvetica-Bold'

    title_style = ParagraphStyle('Title', fontName=font_bold, fontSize=22, leading=26, textColor=colors.HexColor('#1E3A8A'), alignment=1)
    subtitle_style = ParagraphStyle('Sub', fontName=font_bold, fontSize=13, leading=17, textColor=colors.HexColor('#10B981'), alignment=1)
    normal_style = ParagraphStyle('Normal', fontName=font_name, fontSize=10, leading=14, textColor=colors.HexColor('#374151'))
    bold_style = ParagraphStyle('BoldStyle', fontName=font_bold, fontSize=11, leading=15, textColor=colors.HexColor('#111827'))

    story = []
    
    story.append(Paragraph("<b>DREAM MERCHANT BUSINESS SOLUTION</b>", title_style))
    sub_title = "क्वांटम एआई मृदा विश्लेषण एवं सिफारिश कार्ड" if is_hi else "Quantum AI Soil Analysis & Prescription Card"
    story.append(Paragraph(sub_title, subtitle_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph(f"<b>{'रिपोर्ट आईडी' if is_hi else 'Report ID'}:</b> DM-SOIL-{int(time.time())}", normal_style))
    story.append(Paragraph(f"<b>{'फसल' if is_hi else 'Target Crop'}:</b> {crop}", normal_style))
    story.append(Paragraph(f"<b>{'दिनांक' if is_hi else 'Date'}:</b> {time.strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    story.append(Spacer(1, 12))
    
    if is_hi:
        table_data = [
            ['मापदंड (Parameter)', 'आपका स्तर', 'स्थिति (Status)'],
            ['नाइट्रोजन (N)', f'{n} kg/ha', 'अत्यधिक' if n>560 else ('मध्यम' if n>=280 else 'कम')],
            ['फॉस्फोरस (P)', f'{p} kg/ha', 'पर्याप्त' if p>25 else 'कम'],
            ['पोटेशियम (K)', f'{k} kg/ha', 'पर्याप्त' if k>280 else 'कम'],
            ['मिट्टी का pH', f'{ph}', 'क्षारीय' if ph>7.5 else ('अम्लीय' if ph<6.5 else 'उत्तम')]
        ]
    else:
        table_data = [
            ['Parameter', 'Your Value', 'Status'],
            ['Nitrogen (N)', f'{n} kg/ha', 'High' if n>560 else ('Medium' if n>=280 else 'Low')],
            ['Phosphorus (P)', f'{p} kg/ha', 'High' if p>25 else 'Low/Medium'],
            ['Potassium (K)', f'{k} kg/ha', 'High' if k>280 else 'Low/Medium'],
            ['Soil pH', f'{ph}', 'Alkaline' if ph>7.5 else ('Acidic' if ph<6.5 else 'Optimal')]
        ]

    t = Table(table_data, colWidths=[150, 150, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F3F4F6')),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#E5E7EB')),
        ('FONTNAME', (0,0), (-1,-1), font_name),
        ('FONTSIZE', (0,0), (-1,-1), 10),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    
    rec_title = "🔬 क्वांटम कंप्यूटर एआई की सिफारिशें:" if is_hi else "🔬 QUANTUM COMPUTER AI RECOMMENDATIONS:"
    story.append(Paragraph(f"<b>{rec_title}</b>", bold_style))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph(f"• <b>{'नाइट्रोजन व यूरिया' if is_hi else 'Nitrogen & Urea'}:</b> {n_msg}", normal_style))
    story.append(Spacer(1, 5))
    story.append(Paragraph(f"• <b>{'फॉस्फोरस' if is_hi else 'Phosphorus (P)'}:</b> {p_msg}", normal_style))
    story.append(Spacer(1, 5))
    story.append(Paragraph(f"• <b>{'पोटेशियम' if is_hi else 'Potassium (K)'}:</b> {k_msg}", normal_style))
    story.append(Spacer(1, 5))
    story.append(Paragraph(f"• <b>{'मिट्टी pH स्तर' if is_hi else 'Soil pH Level'}:</b> {ph_msg}", normal_style))
    
    story.append(Spacer(1, 30))
    foot_text = "* यह एक स्वचालित रिपोर्ट है जो IBM क्वांटम सर्किट सिमुलेटर द्वारा तैयार की गई है।" if is_hi else "* Automated report generated via IBM Quantum Circuit Simulators."
    story.append(Paragraph(f"<font color='#6B7280'>{foot_text}</font>", ParagraphStyle('Foot', fontName=font_name, fontSize=8, alignment=1)))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# ---------------------------------------------------------
# 5. Quantum Circuit Execution & Output Logic
# ---------------------------------------------------------
btn_text = "📊 क्वांटम एआई जांच शुरू करें" if is_hindi else "📊 Start Quantum AI Analysis"
if st.button(btn_text):
    spin_text = "🧠 क्वांटम सर्किट और पीडीएफ रिपोर्ट तैयार की जा रही है..." if is_hindi else "🧠 Processing Quantum Circuit & Generating PDF Report..."
    with st.spinner(spin_text):
        time.sleep(1.5)
        
        # Qiskit Quantum Circuit Execution
        circuit = QuantumCircuit(4, 4)
        circuit.ry(np.pi if n_value > 560 else (np.pi/2 if n_value >= 280 else 0), 0)
        circuit.ry(np.pi if p_value > 25 else (np.pi/2 if p_value >= 10 else 0), 1)
        circuit.ry(np.pi if k_value > 280 else (np.pi/2 if k_value >= 108 else 0), 2)
        circuit.ry(np.pi if ph_value > 7.5 else (np.pi/2 if ph_value >= 6.5 else 0), 3)
        circuit.measure([0,1,2,3], [0,1,2,3])

        simulator = AerSimulator()
        counts = simulator.run(circuit, shots=100).result().get_counts()
        
        # Fertilizer Logic Calculation
        base_urea = 120 if "धान" in crop_choice or "Rice" in crop_choice else (100 if "गेहूं" in crop_choice or "Wheat" in crop_choice else 150)
        
        if is_hindi:
            if n_value > 560:
                n_msg = "नाइट्रोजन अत्यधिक है! यूरिया का उपयोग पूरी तरह रोकें।"
            elif n_value >= 280:
                u_dose = int(base_urea * 0.8)
                n_msg = f"नाइट्रोजन मध्यम है। 20% कम यूरिया का उपयोग करें। अनुशंसित: {u_dose} किग्रा/एकड़।"
            else:
                u_dose = int(base_urea * 1.2)
                n_msg = f"नाइट्रोजन की कमी है! प्रति एकड़ {u_dose} किग्रा यूरिया जैविक खाद के साथ दें।"

            p_msg = "फॉस्फोरस का स्तर पर्याप्त है। अतिरिक्त DAP/SSP की आवश्यकता नहीं है।" if p_value > 25 else "फॉस्फोरस कम है। बुवाई के समय SSP या DAP डालें।"
            k_msg = "पोटेशियम भरपूर है। फसल की रोग प्रतिरोधक क्षमता अच्छी रहेगी।" if k_value > 280 else "पोटेशियम की कमी है! प्रति एकड़ 20 किग्रा MOP का छिड़काव करें।"
            ph_msg = "मिट्टी क्षारीय (Alkaline) है। जिप्सम या हरी खाद का प्रयोग करें।" if ph_value > 7.5 else ("मिट्टी अम्लीय (Acidic) है। चूना (Lime) का प्रयोग करें।" if ph_value < 6.5 else "मिट्टी का pH मान बिल्कुल सही है।")
        else:
            if n_value > 560:
                n_msg = "Nitrogen is extremely high! Stop using Urea completely."
            elif n_value >= 280:
                u_dose = int(base_urea * 0.8)
                n_msg = f"Nitrogen is medium. Use 20% less urea. Recommended: {u_dose} kg/acre."
            else:
                u_dose = int(base_urea * 1.2)
                n_msg = f"Nitrogen deficiency detected! Recommended: {u_dose} kg urea per acre."

            p_msg = "Phosphorus level is optimal. No need for additional DAP/SSP." if p_value > 25 else "Phosphorus is low. Apply SSP or DAP during sowing."
            k_msg = "Potassium is rich. Plant immunity will be excellent." if k_value > 280 else "Potassium deficiency! Apply 20 kg MOP per acre."
            ph_msg = "Soil is Alkaline. Apply Gypsum to normalize pH." if ph_value > 7.5 else ("Soil is Acidic. Apply Lime during field prep." if ph_value < 6.5 else "Soil pH is perfect and neutral.")

        # Screen Display
        st.success("📊 " + ("क्वांटम सिमुलेशन सफलतापूर्वक पूरा हुआ!" if is_hindi else "Quantum simulation completed successfully!"))
        st.markdown(f"## 📋 {'मृदा स्वास्थ्य कार्ड' if is_hindi else 'SOIL HEALTH REPORT'} - {crop_choice}")
        
        st.markdown(f"<div class='custom-card card-warning'>🌱 <b>{'नाइट्रोजन' if is_hindi else 'Nitrogen'}:</b> {n_msg}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='custom-card card-success'>🌾 <b>{'फॉस्फोरस' if is_hindi else 'Phosphorus'}:</b> {p_msg}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='custom-card card-success'>🍂 <b>{'पोटेशियम' if is_hindi else 'Potassium'}:</b> {k_msg}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='custom-card card-info'>🧪 <b>{'pH स्तर' if is_hindi else 'pH Level'}:</b> {ph_msg}</div>", unsafe_allow_html=True)

        # PDF Download Button
        pdf_data = generate_pdf_report(crop_choice, n_value, p_value, k_value, ph_value, n_msg, p_msg, k_msg, ph_msg, is_hindi)
        
        st.download_button(
            label="📥 " + ("ऑफिशियल सॉइल हेल्थ कार्ड (PDF) डाउनलोड करें" if is_hindi else "Download Official Soil Health Card (PDF)"),
            data=pdf_data,
            file_name=f"Soil_Report_{'HI' if is_hindi else 'EN'}_{int(time.time())}.pdf",
            mime="application/pdf"
        )
        st.balloons()
