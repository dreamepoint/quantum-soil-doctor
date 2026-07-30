import streamlit as st
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import time

# 📱 1. Mobile-First Page Configuration
st.set_page_config(
    page_title="Dream Merchant - Quantum AI", 
    page_icon="🌾", 
    layout="centered", # मोबाइल स्क्रीन के लिए सबसे बेस्ट
    initial_sidebar_state="collapsed"
)

# 🎨 2. Custom CSS for Premium Mobile UI/UX
st.markdown("""
    <style>
    /* पूरे बैकग्राउंड और टेक्स्ट को सुव्यवस्थित करना */
    .main { padding: 10px; }
    h1 { color: #1E3A8A; font-size: 28px !important; text-align: center; font-weight: bold; margin-bottom: 5px; }
    h3 { color: #10B981; font-size: 18px !important; text-align: center; margin-top: 0px; margin-bottom: 25px; }
    
    /* इनपुट कंटेनर्स को सुंदर बनाना */
    .stNumberInput aria-label { font-weight: 600 !important; color: #374151; }
    
    /* बड़े मोबाइल रिस्पॉन्सिव बटन्स */
    div.stButton > button:first-child {
        width: 100% !important;
        background-color: #10B981 !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        padding: 12px 0px !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0px 4px 10px rgba(16, 185, 129, 0.3) !important;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #059669 !important;
        transform: translateY(-2px);
    }
    
    /* कस्टम रिपोर्ट कार्ड्स डिज़ाइन */
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
    </style>
""", unsafe_style_with_html=True)

# 🏢 3. Header Branding
st.markdown("<h1>DREAM MERCHANT</h1>", unsafe_style_with_html=True)
st.markdown("<h3>🧬 Quantum AI Soil Doctor</h3>", unsafe_style_with_html=True)

st.markdown("<p style='text-align: center; color: #6B7280; font-size: 15px;'>भारतीय कृषि को आधुनिक बनाने के लिए क्वांटम कंप्यूटर आधारित सॉइल एनालिसिस पोर्टल।</p>", unsafe_style_with_html=True)
st.markdown("<br>", unsafe_style_with_html=True)

# 📥 4. Clean Input Form (सिंगल कॉलम में जो मोबाइल पर ऊपर से नीचे बिल्कुल परफेक्ट दिखेगा)
n_value = st.number_input("🌱 नाइट्रोजन की मात्रा (N) - kg/ha", min_value=0, value=280, step=10)
p_value = st.number_input("🌾 फॉस्फोरस की मात्रा (P) - kg/ha", min_value=0, value=15, step=5)
k_value = st.number_input("🍂 पोटेशियम की मात्रा (K) - kg/ha", min_value=0, value=150, step=10)
ph_value = st.number_input("🧪 मिट्टी का pH मान (0.0 से 14.0)", min_value=0.0, max_value=14.0, value=7.0, step=0.1)

st.markdown("<br>", unsafe_style_with_html=True)

# 🚀 5. Action Button & Execution UX
if st.button("📊 क्वांटम एआई जांच शुरू करें"):
    
    # यूजर एक्सपीरियंस (UX) के लिए एक सस्पेंस और एनिमेटेड लोडिंग बार
    with st.spinner("🧠 क्वांटम कंप्यूटर सर्किट तैयार कर रहा है..."):
        time.sleep(1.5) # 1.5 सेकंड का रियल-टाइम फील देने के लिए डिले
        
    # बैक-एंड क्वांटम कोर लॉजिक
    angle_N = np.pi if n_value > 560 else (np.pi/2 if n_value >= 280 else 0)
    angle_pH = np.pi if ph_value > 7.5 else (np.pi/2 if ph_value >= 6.5 else 0)

    circuit = QuantumCircuit(2, 2)
    circuit.ry(angle_N, 0)
    circuit.ry(angle_pH, 1)
    circuit.measure([0, 1], [0, 1])

    simulator = AerSimulator()
    job = simulator.run(circuit, shots=100)
    counts = job.result().get_counts()
    best_pattern = max(counts, key=counts.get)
    
    # 📈 6. Beautiful Customized Output Cards Display
    st.markdown("### 📋 फाइनल सॉइल हेल्थ रिपोर्ट")
    
    # नाइट्रोजन का निर्णय और सुंदर कार्ड्स
    if n_value > 560:
        st.markdown("<div class='custom-card card-error'><b>❌ नाइट्रोजन अत्यधिक है!</b><br>यूरिया का उपयोग तुरंत रोकें और केवल नीम-कोटिंग यूरिया ही सीमित मात्रा में डालें। मिट्टी को विश्राम की आवश्यकता है।</div>", unsafe_style_with_html=True)
    elif n_value >= 280:
        st.markdown("<div class='custom-card card-warning'><b>⚠️ नाइट्रोजन मध्यम है।</b><br>नाइट्रोजन का स्तर सामान्य श्रेणी में है। फसल की स्थिति देखकर केवल आवश्यकतानुसार ही हल्की डोज़ दें।</div>", unsafe_style_with_html=True)
    else:
        st.markdown("<div class='custom-card card-info'><b>ℹ️ नाइट्रोजन की कमी है!</b><br>मिट्टी की उपजाऊ क्षमता बढ़ाने के लिए रासायनिक खाद के बजाय गोबर की जैविक खाद या केंचुए की खाद (Vermicompost) का प्रयोग करें।</div>", unsafe_style_with_html=True)
        
    # pH का निर्णय और सुंदर कार्ड्स
    if ph_value > 7.5:
        st.markdown("<div class='custom-card card-error'><b>🔴 मिट्टी क्षारीय (Alkaline) है!</b><br>pH स्तर सामान्य से अधिक है। मिट्टी के सुधार के लिए प्रति एकड़ खेत में थोड़ा जिप्सम या हरी खाद का प्रयोग अनिवार्य रूप से करें।</div>", unsafe_style_with_html=True)
    elif ph_value < 6.5:
        st.markdown("<div class='custom-card card-info'><b>🔵 मिट्टी अम्लीय (Acidic) है!</b><br>pH स्तर कम है। अम्लता को नियंत्रित करने के लिए खेत की जुताई के समय उचित मात्रा में बुझे हुए चूने (Lime) का छिड़काव करें।</div>", unsafe_style_with_html=True)
    else:
        st.markdown("<div class='custom-card card-success'><b>✅ मिट्टी का pH स्तर उत्तम है!</b><br>आपकी मिट्टी का स्वास्थ्य एकदम न्यूट्रल और फसलों के लिए सर्वोत्तम है। किसी विशेष रासायनिक सुधारक की आवश्यकता नहीं है।</div>", unsafe_style_with_html=True)
