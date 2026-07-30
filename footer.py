import streamlit as st

def render_footer():
    st.markdown("---")
    st.markdown("""
        <style>
        .footer {
            text-align: center;
            color: #6B7280;
            font-size: 14px;
            padding: 15px 0px 5px 0px;
        }
        .footer a {
            color: #10B981;
            text-decoration: none;
            font-weight: bold;
        }
        </style>
        <div class="footer">
            <p>🧬 <b>Dream Merchant Quantum AI — Soil Doctor v2.5</b></p>
            <p>भारतीय किसानों के लिए क्वांटम कंप्यूटर आधारित डिजिटल सॉइल हेल्थ प्लेटफॉर्म।</p>
            <p>Powered by Qiskit & Streamlit | Developed with ❤️ for Farmers</p>
        </div>
    """, unsafe_allow_html=True)
