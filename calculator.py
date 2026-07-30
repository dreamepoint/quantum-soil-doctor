import streamlit as st

def render_calculator(is_hindi):
    if is_hindi:
        st.markdown("## 💰 उर्वरक मात्रा एवं लागत कैलकुलेटर")
        st.markdown("यहाँ आप अपनी जमीन के क्षेत्रफल और सिफ़ारिश के अनुसार खाद की बोरी (Bags) और लागत का हिसाब लगा सकते हैं।")
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            land_area = st.number_input("🌾 खेत का क्षेत्रफल (एकड़ में):", min_value=0.5, value=1.0, step=0.5)
            urea_rate = st.number_input("💵 यूरिया की 1 बोरी (45 kg) की कीमत (₹):", min_value=200, value=266, step=5)
        with col2:
            dap_rate = st.number_input("💵 DAP की 1 बोरी (50 kg) की कीमत (₹):", min_value=1000, value=1350, step=10)
            mop_rate = st.number_input("💵 MOP की 1 बोरी (50 kg) की कीमत (₹):", min_value=1000, value=1700, step=10)

        # सिमुलेशन स्टेट से सिफ़ारिश निकालें (यदि उपलब्ध हो)
        if 'results' in st.session_state:
            res = st.session_state['results']
            n_val = res['n_val']
            p_val = res['p_val']
            k_val = res['k_val']

            # बोरी का हिसाब (यूरिया 45kg, DAP 50kg, MOP 50kg)
            # मानक औसतन खुराक के आधार पर अनुमानित गणना
            recommended_urea_kg = (100 if n_val >= 110 else 130) * land_area
            recommended_dap_kg = (0 if p_val > 10 else 50) * land_area
            recommended_mop_kg = (0 if k_val > 110 else 20) * land_area

            urea_bags = round(recommended_urea_kg / 45, 1)
            dap_bags = round(recommended_dap_kg / 50, 1)
            mop_bags = round(recommended_mop_kg / 50, 1)

            total_cost = (urea_bags * urea_rate) + (dap_bags * dap_rate) + (mop_bags * mop_rate)

            st.markdown("---")
            st.markdown("### 📊 आपकी सिफ़ारिश के अनुसार कुल आवश्यकता:")

            c1, c2, c3 = st.columns(3)
            c1.metric("🌱 यूरिया बोरी (45 kg)", f"{urea_bags} Bags", f"~{int(recommended_urea_kg)} kg")
            c2.metric("🌾 DAP बोरी (50 kg)", f"{dap_bags} Bags", f"~{int(recommended_dap_kg)} kg")
            c3.metric("🍂 MOP बोरी (50 kg)", f"{mop_bags} Bags", f"~{int(recommended_mop_kg)} kg")

            st.success(f"💰 **अनुमानित कुल खाद लागत ({land_area} एकड़):** ₹{int(total_cost)}")

            if n_val > 220:
                saved_bags = round((50 * land_area) / 45, 1)
                saved_money = saved_bags * urea_rate
                st.info(f"🎉 **क्वांटम एआई बचत एडवाइजरी:** आपकी मिट्टी में नाइट्रोजन पहले से अधिक है, यूरिया न डालने से आपके लगभग **₹{int(saved_money)}** बचेंगे!")

        else:
            st.info("💡 पहले 'सॉइल टेस्ट पोर्टल' टैब में जाकर अपनी मिट्टी की जांच रन करें, फिर यहाँ सटीक गणना देखें।")

    else:
        st.markdown("## 💰 Fertilizer Quantity & Cost Calculator")
        st.markdown("Calculate fertilizer bags required and estimated costs based on your land size.")
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            land_area = st.number_input("🌾 Land Area (in Acres):", min_value=0.5, value=1.0, step=0.5)
            urea_rate = st.number_input("💵 Urea Price per 45kg Bag (₹):", min_value=200, value=266, step=5)
        with col2:
            dap_rate = st.number_input("💵 DAP Price per 50kg Bag (₹):", min_value=1000, value=1350, step=10)
            mop_rate = st.number_input("💵 MOP Price per 50kg Bag (₹):", min_value=1000, value=1700, step=10)

        if 'results' in st.session_state:
            res = st.session_state['results']
            n_val = res['n_val']
            p_val = res['p_val']
            k_val = res['k_val']

            recommended_urea_kg = (100 if n_val >= 110 else 130) * land_area
            recommended_dap_kg = (0 if p_val > 10 else 50) * land_area
            recommended_mop_kg = (0 if k_val > 110 else 20) * land_area

            urea_bags = round(recommended_urea_kg / 45, 1)
            dap_bags = round(recommended_dap_kg / 50, 1)
            mop_bags = round(recommended_mop_kg / 50, 1)

            total_cost = (urea_bags * urea_rate) + (dap_bags * dap_rate) + (mop_bags * mop_rate)

            st.markdown("---")
            st.markdown("### 📊 Required Fertilizer Estimation:")

            c1, c2, c3 = st.columns(3)
            c1.metric("🌱 Urea Bags (45 kg)", f"{urea_bags} Bags", f"~{int(recommended_urea_kg)} kg")
            c2.metric("🌾 DAP Bags (50 kg)", f"{dap_bags} Bags", f"~{int(recommended_dap_kg)} kg")
            c3.metric("🍂 MOP Bags (50 kg)", f"{mop_bags} Bags", f"~{int(recommended_mop_kg)} kg")

            st.success(f"💰 **Estimated Total Fertilizer Cost ({land_area} Acre):** ₹{int(total_cost)}")

            if n_val > 220:
                saved_bags = round((50 * land_area) / 45, 1)
                saved_money = saved_bags * urea_rate
                st.info(f"🎉 **Quantum AI Savings Advisory:** Nitrogen is high in your soil. Skipping unnecessary Urea saves you approx **₹{int(saved_money)}**!")

        else:
            st.info("💡 Run the soil analysis in the 'Soil Test Portal' tab first to view customized calculations here.")
