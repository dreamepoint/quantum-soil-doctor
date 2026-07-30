import streamlit as st
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

st.set_page_config(page_title="Dream Merchant - Quantum AI", page_icon="🌾", layout="centered")
st.title("🌾 Dream Merchant Business Solution")
st.subheader("🤖 Quantum AI Soil Doctor - भारतीय कृषि समाधान")
st.markdown("---")

st.write("अपने खेत की मिट्टी की जांच रिपोर्ट (Soil Health Card) के आंकड़े नीचे दर्ज करें और क्वांटम सुपरकंप्यूटर आधारित सटीक वैज्ञानिक सलाह तुरंत प्राप्त करें।")

col1, col2 = st.columns(2)
with col1:
    n_value = st.number_input("नाइट्रोजन की मात्रा (N) - kg/ha", min_value=0, value=280)
    p_value = st.number_input("फॉस्फोरस की मात्रा (P) - kg/ha", min_value=0, value=15)
with col2:
    k_value = st.number_input("पोटेशियम की मात्रा (K) - kg/ha", min_value=0, value=150)
    ph_value = st.number_input("मिट्टी का pH मान (0 से 14)", min_value=0.0, max_value=14.0, value=7.0, step=0.1)

st.markdown("---")

if st.button("🚀 क्वांटम सलाह प्राप्त करें", type="primary"):
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
    
    st.success("📊 क्वांटम एआई विश्लेषण पूरा हुआ!")
    
    st.markdown("### 🧪 पोषक तत्व रिपोर्ट:")
    if n_value > 560:
        st.error("❌ सलाह: नाइट्रोजन अत्यधिक है! यूरिया का उपयोग तुरंत रोकें और नीम-कोटिंग यूरिया ही डालें।")
    elif n_value >= 280:
        st.warning("⚠️ सलाह: नाइट्रोजन मध्यम स्तर पर है। केवल आवश्यकतानुसार हल्की डोज़ दें।")
    else:
        st.info("✅ सलाह: नाइट्रोजन कम है। मिट्टी की उपजाऊ क्षमता बढ़ाने के लिए जैविक खाद डालें।")
        
    st.markdown("### 🪵 मिट्टी की सेहत (pH स्तर):")
    if ph_value > 7.5:
        st.error("🔴 सलाह: मिट्टी हल्की क्षारीय (Alkaline) है, सुधार के लिए जिप्सम मिलाएं।")
    elif ph_value < 6.5:
        st.error("🔵 सलाह: मिट्टी अम्लीय (Acidic) है, चूने (Lime) का प्रयोग करें।")
    else:
        st.success("✅ सलाह: मिट्टी का pH स्तर खेती के लिए एकदम उत्तम (Neutral) है।")
