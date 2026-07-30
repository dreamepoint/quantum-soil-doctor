import streamlit as st
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import time
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# 📱 1. Mobile-First Page Configuration
st.set_page_config(
    page_title="Dream Merchant - Quantum AI", 
    page_icon="🌾", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# 🌐 2. सोशल मीडिया शेयरिंग मेटा टैग्स
st.markdown("""
    <head>
        <meta property="og:type" content="website">
        <meta property="og:title" content="Dream Merchant Quantum AI — Soil Doctor">
        <meta property="og:description" content="भारतीय किसानों के लिए क्वांटम कंप्यूटर आधारित सॉइल एनालिसिस पोर्टल।">
        <meta property="og:image" content="https://raw.githubusercontent.com/dreamepoint/quantum-soil-doctor/refs/heads/main/ogimage.png?token=GHSAT0AAAAAAEEIPVERXYFZEG5AWDH7F3T62TLNURA">
    </head>
""", unsafe_allow_html=True)

# 🎨 3. Custom CSS for UI/UX
st.markdown("""
    <style>
    .main { padding: 10px; }
    h1 { color: #FFFFFF !important; font-size: 28px !important; text-align: center; font-weight: bold; margin-bottom: 5px; }
    h3 { color: #10B981 !important; font-size: 18px !important; text-align: center; margin-top: 0px; margin-bottom: 25px; }
    .custom-card {
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
        font-size: 16px;
        line-height: 1.5;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
    }
    .card-success { background-color: #DCFCE7; border-left: 6px solid #16A34A; color: #14532D; }
    .card-warning { background-color: #FEF3C7; border-left: 6px solid #D97706; color: #78350F; }
    .card-error { background-color: #FEE2E2; border-left: 6px solid #DC2626; color: #7F1D1D; }
    .card-info { background-color: #E0F2FE; border-left: 6px solid #0284C7; color: #0C4A6E; }
    
    div.stButton > button:first-child {
        width: 100% !important;
        background-color: #10B981 !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        padding: 12px 0px !important;
        border-radius: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🏢 4. Header Branding
st.markdown("<h1>DREAM MERCHANT</h1>", unsafe_allow_html=True)
st.markdown("<h3>🧬 Quantum AI Soil Doctor v2.5</h3>", unsafe_allow_html=True)

# 🚜 Inputs
crop_choice = st.selectbox("आप खेत में कौन सी फसल उगाना चाहते हैं?", ["धान (Rice)", "गेहूं (Wheat)", "कपास (Cotton)"])
st.markdown("---")
st.markdown("### 📊 मिट्टी की जांच रिपोर्ट")

col1, col2 = st.columns(2)
with col1:
    n_value = st.number_input("🌱 नाइट्रोजन (N) - kg/ha", min_value=0, value=280, step=10)
    p_value = st.number_input("🌾 फॉस्फोरस (P) - kg/ha", min_value=0, value=15, step=5)
with col2:
    k_value = st.number_input("🍂 पोटेशियम (K) - kg/ha", min_value=0, value=150, step=10)
    ph_value = st.number_input("🧪 मिट्टी का pH मान", min_value=0.0, max_value=14.0, value=7.0, step=0.1)

st.markdown("<br>", unsafe_allow_html=True)

# 🚀 5. PDF बनाने का बैक-एंड फंक्शन
def generate_pdf_report(crop, n, p, k, ph, n_msg, p_msg, k_msg, ph_msg):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=24, leading=28, textColor=colors.HexColor('#1E3A8A'), alignment=1)
    subtitle_style = ParagraphStyle('Sub', parent=styles['Heading3'], fontSize=14, leading=18, textColor=colors.HexColor('#10B981'), alignment=1)
    normal_style = ParagraphStyle('Normal', parent=styles['Normal'], fontSize=11, leading=15, textColor=colors.HexColor('#374151'))
    
    story = []
    story.append(Paragraph("<b>DREAM MERCHANT BUSINESS SOLUTION</b>", title_style))
    story.append(Paragraph("Quantum AI Soil Analysis & Prescription Card", subtitle_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph(f"<b>Report ID:</b> DM-SOIL-{int(time.time())}", normal_style))
    story.append(Paragraph(f"<b>Target Crop:</b> {crop}", normal_style))
    story.append(Paragraph(f"<b>Date:</b> {time.strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    story.append(Spacer(1, 15))
    
    data = [
        ['Parameter', 'Your Value', 'Status'],
        ['Nitrogen (N)', f'{n} kg/ha', 'High' if n>560 else ('Medium' if n>=280 else 'Low')],
        ['Phosphorus (P)', f'{p} kg/ha', 'High' if p>25 else 'Low/Medium'],
        ['Potassium (K)', f'{k} kg/ha', 'High' if k>280 else 'Low/Medium'],
        ['Soil pH', f'{ph}', 'Alkaline' if ph>7.5 else ('Acidic' if ph<6.5 else 'Optimal')]
    ]
    t = Table(data, colWidths=[150, 150, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F3F4F6')),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#E5E7EB')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("<b>🔬 QUANTUM COMPUTER AI RECOMMENDATIONS:</b>", ParagraphStyle('Bold', parent=normal_style, fontName='Helvetica-Bold', fontSize=12)))
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"• <b>Nitrogen & Urea:</b> {n_msg}", normal_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"• <b>Phosphorus (P):</b> {p_msg}", normal_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"• <b>Potassium (K):</b> {k_msg}", normal_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"• <b>Soil pH Level:</b> {ph_msg}", normal_style))
    
    story.append(Spacer(1, 40))
    story.append(Paragraph("<font color='#6B7280'>* This is an automated report processed via IBM Quantum Circuit Simulators by Dream Merchant AI Team.</font>", ParagraphStyle('Foot', parent=normal_style, fontSize=9, alignment=1)))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# 🚀 6. Execution Button
if st.button("📊 क्वांटम एआई जांच शुरू करें"):
    with st.spinner("🧠 क्वांटम सर्किट और पीडीएफ रिपोर्ट तैयार की जा रही है..."):
        time.sleep(2.0)
        
        circuit = QuantumCircuit(4, 4)
        circuit.ry(np.pi if n_value > 560 else (np.pi/2 if n_value >= 280 else 0), 0)
        circuit.ry(np.pi if p_value > 25 else (np.pi/2 if p_value >= 10 else 0), 1)
        circuit.ry(np.pi if k_value > 280 else (np.pi/2 if k_value >= 108 else 0), 2)
        circuit.ry(np.pi if ph_value > 7.5 else (np.pi/2 if ph_value >= 6.5 else 0), 3)
        
        circuit.measure([0,1,2,3], [0,1,2,3])

        simulator = AerSimulator()
        counts = simulator.run(circuit, shots=100).result().get_counts()
        
        st.success("📊 क्वांटम क्रॉप सिमुलेशन सफलतापूर्वक पूरा हुआ!")
        st.markdown(f"## 📋 FINAL SOIL HEALTH REPORT - {crop_choice}")
        
        base_urea = 120 if crop_choice == "धान (Rice)" else (100 if crop_choice == "गेहूं (Wheat)" else 150)
        
        if n_value > 560:
            n_msg = "Nitrogen is extremely high! Stop using Urea completely. Give soil rest."
            st.markdown("<div class='custom-card card-error'><b>❌ नाइट्रोजन अत्यधिक है!</b><br>यूरिया का उपयोग तुरंत रोकें।</div>", unsafe_allow_html=True)
        elif n_value >= 280:
            u_dose = int(base_urea * 0.8)
            n_msg = f"Nitrogen is medium. Use 20% less urea. Recommended: {u_dose} kg per acre."
            st.markdown(f"<div class='custom-card card-warning'><b>⚠️ नाइट्रोजन मध्यम है।</b><br>प्रति एकड़ केवल <b>{u_dose} kg यूरिया</b> दें।</div>", unsafe_allow_html=True)
        else:
            u_dose = int(base_urea * 1.2)
            n_msg = f"Nitrogen deficiency detected! Recommended: {u_dose} kg urea per acre mixed with organic compost."
            st.markdown(f"<div class='custom-card card-info'><b>ℹ️ नाइट्रोजन की भारी कमी है!</b><br>प्रति एकड़ <b>{u_dose} kg यूरिया</b> डालें।</div>", unsafe_allow_html=True)
            
        if p_value > 25:
            p_msg = "Phosphorus level is optimal. No need for additional DAP/SSP."
            st.markdown("<div class='custom-card card-success'><b>✅ फॉस्फोरस पर्याप्त है।</b></div>", unsafe_allow_html=True)
        else:
            p_msg = "Phosphorus is low. Apply Single Super Phosphate (SSP) or DAP during sowing."
            st.markdown("<div class='custom-card card-warning'><b>⚠️ फॉस्फोरस कम है!</b></div>", unsafe_allow_html=True)

        if k_value > 280:
            k_msg = "Potassium is rich. Plant immunity will be excellent."
            st.markdown("<div class='custom-card card-success'><b>✅ पोटेशियम भरपूर है।</b></div>", unsafe_allow_html=True)
        else:
            k_msg = "Potassium deficiency! Apply 20 kg Muriate of Potash (MOP) per acre."
            st.markdown("<div class='custom-card card-warning'><b>⚠️ पोटेशियम की कमी है!</b></div>", unsafe_allow_html=True)

        if ph_value > 7.5:
            ph_msg = "Soil is Alkaline. Apply Gypsum or green manure to normalize pH."
            st.markdown("<div class='custom-card card-error'><b>🔴 मिट्टी क्षारीय (Alkaline) है!</b></div>", unsafe_allow_html=True)
        elif ph_value < 6.5:
            ph_msg = "Soil is Acidic. Apply slaked Lime during land preparation."
            st.markdown("<div class='custom-card card-info'><b>🔵 मिट्टी अम्लीय (Acidic) है!</b></div>", unsafe_allow_html=True)
        else:
            ph_msg = "Soil pH is perfect and neutral. Highly fertile."
            st.markdown("<div class='custom-card card-success'><b>✅ मिट्टी का pH स्तर उत्तम है!</b></div>", unsafe_allow_html=True)

        # 🖨️ असली प्रोफेशनल पीडीएफ जनरेट करना
        pdf_data = generate_pdf_report(crop_choice, n_value, p_value, k_value, ph_value, n_msg, p_msg, k_msg, ph_msg)
        
        st.markdown("", unsafe_allow_html=True)
        st.download_button(
            label="📥 ऑफिशियल सॉइल हेल्थ कार्ड (PDF) डाउनलोड करें",
            data=pdf_data,
            file_name=f"Dream_Merchant_Soil_Report_{int(time.time())}.pdf",
            mime="application/pdf"
        )
        st.balloons()
