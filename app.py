import streamlit as st
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import time

# 📱 1. Mobile-First Page Configuration
st.set_page_config(
    page_title="Dream Merchant - Quantum AI", 
    page_icon="🌾", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# 🌐 2. व्हाट्सएप और सोशल मीडिया शेयरिंग मेटा टैग्स
st.markdown("""
    <head>
        <meta property="og:type" content="website">
        <meta property="og:title" content="Dream Merchant Quantum AI — Soil Doctor">
        <meta property="og:description" content="भारतीय किसानों के लिए क्वांटम कंप्यूटर आधारित सॉइल एनालिसिस और सटीक खाद सिमुलेशन पोर्टल।">
        <meta property="og:image" content="https://raw.githubusercontent.com/dreamepoint/quantum-soil-doctor/refs/heads/main/ogimage.png?token=GHSAT0AAAAAAEEIPVERXYFZEG5AWDH7F3T62TLNURA">
    </head>
""", unsafe_allow_html=True)

# 🎨 3. Premium CSS for UI/UX
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
        box-shadow: 0px 4px 10px rgba(16, 185, 129, 0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🏢 4. Header Branding
st.markdown("<h1>DREAM MERCHANT</h1>", unsafe_allow_html=True)
st.markdown("<h3>🧬 Quantum AI Soil Doctor v2.0</h3>", unsafe_allow_html=True)

# 🌾 Feature 1: Crop Selection Dropdown
st.markdown("### 🚜 फसल की जानकारी चुनें")
crop_choice = st.selectbox("आप खेत में कौन सी फसल उगाना चाहते हैं?", ["धान (Rice)", "गेहूं (Wheat)", "कपास (Cotton)"])

st.markdown("---")
st.markdown("### 📊 मिट्टी की जांच रिपोर्ट (NPK & pH)")

# इनपुट बॉक्स्स
col1, col2 = st.columns(2)
with col1:
    n_value = st.number_input("🌱 नाइट्रोजन (N) - kg/ha", min_value=0, value=280, step=10)
    p_value = st.number_input("🌾 फॉस्फोरस (P) - kg/ha", min_value=0, value=15, step=5)
with col2:
    k_value = st.number_input("🍂 पोटेशियम (K) - kg/ha", min_value=0, value=150, step=10)
    ph_value = st.number_input("🧪 मिट्टी का pH मान", min_value=0.0, max_value=14.0, value=7.0, step=0.1)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 क्वांटम एआई जांच शुरू करें"):
    
    with st.spinner("🧠 क्वांटम कंप्यूटर एआई सर्किट और क्रॉप सिमुलेशन तैयार कर रहा है..."):
        time.sleep(2.0)
        
    # बैक-एंड क्वांटम सिमुलेशन
    circuit = QuantumCircuit(4, 4)
    # एनकोडिंग डेटा
    circuit.ry(np.pi if n_value > 560 else (np.pi/2 if n_value >= 280 else 0), 0)
    circuit.ry(np.pi if p_value > 25 else (np.pi/2 if p_value >= 10 else 0), 1)
    circuit.ry(np.pi if k_value > 280 else (np.pi/2 if k_value >= 108 else 0), 2)
    circuit.ry(np.pi if ph_value > 7.5 else (np.pi/2 if ph_value >= 6.5 else 0), 3)
    circuit.measure(,[0,1,2,3])

    simulator = AerSimulator()
    counts = simulator.run(circuit, shots=100).result().get_counts()
    
    st.success("📊 क्वांटम क्रॉप सिमुलेशन सफलतापूर्वक पूरा हुआ!")
    st.markdown(f"## 📋 फाइनल सॉइल हेल्थ रिपोर्ट - {crop_choice}")
    
    # फसल के अनुसार खाद की डोज़ की गणना (लॉजिक लेयर)
    base_urea = 120 if crop_choice == "धान (Rice)" else (100 if crop_choice == "गेहूं (Wheat)" else 150)
    
    # 1. नाइट्रोजन रिपोर्ट
    if n_value > 560:
        st.markdown(f"<div class='custom-card card-error'><b>❌ नाइट्रोजन अत्यधिक है!</b><br>आपकी चुनी हुई फसल <b>{crop_choice}</b> के लिए इस खेत में यूरिया की कोई आवश्यकता नहीं है। मिट्टी को विश्राम दें।</div>", unsafe_allow_html=True)
    elif n_value >= 280:
        recommended_urea = int(base_urea * 0.8)
        st.markdown(f"<div class='custom-card card-warning'><b>⚠️ नाइट्रोजन मध्यम है।</b><br><b>{crop_choice}</b> के लिए आपको सामान्य से 20% कम यूरिया डालना है। प्रति एकड़ केवल <b>{recommended_urea} kg यूरिया</b> की डोज़ दें।</div>", unsafe_allow_html=True)
    else:
        recommended_urea = int(base_urea * 1.2)
        st.markdown(f"<div class='custom-card card-info'><b>ℹ️ नाइट्रोजन की भारी कमी है!</b><br><b>{crop_choice}</b> के अच्छे विकास के लिए प्रति एकड़ <b>{recommended_urea} kg यूरिया</b> डालें और साथ में गोबर की जैविक खाद अवश्य मिलाएं।</div>", unsafe_allow_html=True)
        
    # 2. Feature 2: फॉस्फोरस (P) रिपोर्ट
    if p_value > 25:
        st.markdown("<div class='custom-card card-success'><b>✅ फॉस्फोरस पर्याप्त है।</b><br>जड़ों के विकास के लिए फॉस्फोरस का स्तर उत्तम है, अलग से DAP डालने की आवश्यकता नहीं है।</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='custom-card card-warning'><b>⚠️ फॉस्फोरस कम है!</b><br>फसल की जड़ों को मजबूती देने के लिए सिंगल सुपर फॉस्फेट (SSP) या DAP खाद का उचित मात्रा में उपयोग करें।</div>", unsafe_allow_html=True)

    # 3. Feature 2: पोटेशियम (K) रिपोर्ट
    if k_value > 280:
        st.markdown("<div class='custom-card card-success'><b>✅ पोटेशियम भरपूर है।</b><br>पौधों की रोग प्रतिरोधक क्षमता अच्छी रहेगी। अतिरिक्त पोटाश की जरूरत नहीं है।</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='custom-card card-warning'><b>⚠️ पोटेशियम की कमी है!</b><br>दानों की चमक और वजन बढ़ाने के लिए बुआई के समय प्रति एकड़ 20 kg म्‍यूरिएट ऑफ पोटाश (MOP) का प्रयोग करें।</div>", unsafe_allow_html=True)

    # 4. pH रिपोर्ट
    if ph_value > 7.5:
        st.markdown("<div class='custom-card card-error'><b>🔴 मिट्टी क्षारीय (Alkaline) है!</b><br>सुधार के लिए प्रति एकड़ खेत में 2 टन जिप्सम या हरी खाद (ढैंचा) का प्रयोग अनिवार्य रूप से करें।</div>", unsafe_allow_html=True)
    elif ph_value < 6.5:
        st.markdown("<div class='custom-card card-info'><b>🔵 मिट्टी अम्लीय (Acidic) है!</b><br>अम्लता को नियंत्रित करने के लिए खेत की आखिरी जुताई के समय बुझे हुए चूने (Lime) का छिड़काव करें।</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='custom-card card-success'><b>✅ मिट्टी का pH स्तर उत्तम है!</b><br>आपकी मिट्टी का स्वास्थ्य एकदम न्यूट्रल और फसलों के लिए सर्वोत्तम है।</div>", unsafe_allow_html=True)

    # 🖨️ Feature 3: डिजिटल रसीद डाउनलोड (सिम्युलेटेड प्रिंट बटन जो मोबाइल पर बहुत काम आता है)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.download_button(
        label="📥 डिजिटल सॉइल कार्ड (PDF) डाउनलोड करें",
        data=f"DREAM MERCHANT QUANTUM AI REPORT\nCrop: {crop_choice}\nInputs - N:{n_value}, P:{p_value}, K:{k_value}, pH:{ph_value}\nStatus: Processed by Quantum Simulator successfully.",
        file_name=f"Soil_Report_DM_{int(time.time())}.txt",
        mime="text/plain"
    ):
        st.balloons()
