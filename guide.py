import streamlit as st

def render_guide(is_hindi):
    """
    किसान भाइयों के लिए ऐप का उपयोग करने और मिट्टी का डेटा प्राप्त करने की पूरी गाइड।
    """
    if is_hindi:
        st.markdown("## 👨‍🌾 ऐप का उपयोग कैसे करें और मिट्टी का डेटा कहाँ से लाएं?")
        st.markdown("---")

        # Step 1: Data Sources
        st.markdown("### 1️⃣ मिट्टी की जाँच का डेटा (N, P, K, pH) कहाँ से मिलेगा?")
        st.markdown("""
        अपनी मिट्टी का सही डेटा (नाइट्रोजन, फॉस्फोरस, पोटेशियम और pH मान) प्राप्त करने के 3 आसान तरीके हैं:
        
        * **सरकारी मृदा परीक्षण प्रयोगशाला (Soil Testing Lab):** अपने नजदीकी कृषि विज्ञान केंद्र (KVK) या जिला कृषि कार्यालय में जाकर 50-100 रुपये में मिट्टी की जाँच करवाएं।
        * **सॉइल हेल्थ कार्ड (Soil Health Card):** यदि आपके पास सरकार द्वारा जारी 'मृदा स्वास्थ्य कार्ड' है, तो उसमें लिखे N, P, K और pH के मान यहाँ दर्ज करें।
        * **डिजिटल/डिजिटल सॉइल टेस्टिंग किट:** बाजार में मिलने वाले पोर्टेबल सॉइल सेंसर या डिजिटल किट से तुरंत अपनी मिट्टी का मान मापें।
        """)

        st.markdown("---")

        # Step 2: How to Use App
        st.markdown("### 2️⃣ 'क्वांटम एआई सॉइल डॉक्टर' ऐप का उपयोग कैसे करें?")
        st.markdown("""
        * **स्टेप 1 (भाषा चुनें):** सबसे ऊपर अपनी सुविधा अनुसार **हिंदी** या **English** चुनें।
        * **स्टेप 2 (फसल चुनें):** आप अपने खेत में जो फसल (जैसे: कपास, धान, गेहूं) उगाना चाहते हैं, उसे चुनें।
        * **स्टेप 3 (डेटा भरें):** अपनी मिट्टी की जाँच रिपोर्ट से नाइट्रोजन (N), फॉस्फोरस (P), पोटेशियम (K) और pH का मान दर्ज करें।
        * **स्टेप 4 (जाँच शुरू करें):** **"📊 क्वांटम एआई जांच शुरू करें"** वाले हरे बटन पर क्लिक करें।
        * **स्टेप 5 (परिणाम और शेयरिंग):**
            * 👁️ **रिपोर्ट देखें:** स्क्रीन पर ही तुरंत सलाह देखें।
            * 📥 **डाउनलोड PDF:** ऑफिशियल PDF रिपोर्ट अपने फोन में सेव करें।
            * 📲 **व्हाट्सएप:** सलाह को सीधे अपने किसान दोस्तों या व्हाट्सएप पर शेयर करें।
        """)

        st.info("💡 **सुझाव:** यदि आपके पास सटीक लैब रिपोर्ट नहीं है, तो आप अपने अनुमानित मान डालकर भी एआई की सिफारिशों को समझ सकते हैं।")

    else:
        st.markdown("## 👨‍🌾 How to Use this App & Get Soil Data?")
        st.markdown("---")

        st.markdown("### 1️⃣ How to get Soil Data (N, P, K, pH)?")
        st.markdown("""
        You can get your soil parameter values through any of these 3 easy ways:
        
        * **Government Soil Testing Labs:** Visit your nearest Krishi Vigyan Kendra (KVK) or Agriculture Office for an official soil test.
        * **Soil Health Card:** Enter the N, P, K, and pH values listed on your government-issued Soil Health Card.
        * **Digital Soil Testing Kits:** Use portable digital soil testing meters/sensors available in the market for instant readings.
        """)

        st.markdown("---")

        st.markdown("### 2️⃣ How to use 'Quantum AI Soil Doctor'?")
        st.markdown("""
        * **Step 1 (Language):** Choose **Hindi** or **English** from the dropdown at the top.
        * **Step 2 (Crop):** Select the target crop (e.g., Cotton, Rice, Wheat) you plan to sow.
        * **Step 3 (Inputs):** Enter your soil test values for Nitrogen (N), Phosphorus (P), Potassium (K), and pH.
        * **Step 4 (Analyze):** Click on the green **"📊 Start Quantum AI Analysis"** button.
        * **Step 5 (Actions):**
            * 👁️ **View:** Read recommendations directly on screen.
            * 📥 **Download PDF:** Save the official PDF report to your mobile/computer.
            * 📲 **WhatsApp:** Share the report instantly via WhatsApp.
        """)

        st.info("💡 **Tip:** If you don't have exact lab results right now, you can input approximate values to test the AI recommendations.")
