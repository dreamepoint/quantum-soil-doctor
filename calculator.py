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
            n_val = res.get('n_val', 0)
            p_val = res.get('p_val', 0)
            k_val = res.get('k_val', 0)

            # 1. DAP (Phosphorus Target)
            recommended_dap_kg = (0 if p_val > 50 else (50 if p_val > 25 else 75)) * land_area
            dap_bags = round(recommended_dap_kg / 50, 1)

            # 2. Urea Target (DAP से प्राप्त 18% Nitrogen को घटाकर)
            n_from_dap_kg = recommended_dap_kg * 0.18
            target_n_kg = (60 if n_val >= 200 else (90 if n_val >= 100 else 120)) * land_area
            remaining_n_kg = max(0, target_n_kg - n_from_dap_kg)
            
            recommended_urea_kg = remaining_n_kg / 0.46
            urea_bags = round(recommended_urea_kg / 45, 1)

            # 3. MOP (Potassium Target)
            recommended_mop_kg = (0 if k_val > 200 else (25 if k_val > 100 else 40)) * land_area
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
                st.info(f"🎉 **क्वांटम एआई बचत एडवाइजरी:** आपकी मिट्टी में नाइट्रोजन पर्याप्त है। DAP में मौजूद N को एडजस्ट करने से आपके लगभग **₹{int(saved_money)}** बच रहे हैं!")

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
            n_val = res.get('n_val', 0)
            p_val = res.get('p_val', 0)
            k_val = res.get('k_val', 0)

            recommended_dap_kg = (0 if p_val > 50 else (50 if p_val > 25 else 75)) * land_area
            dap_bags = round(recommended_dap_kg / 50, 1)

            n_from_dap_kg = recommended_dap_kg * 0.18
            target_n_kg = (60 if n_val >= 200 else (90 if n_val >= 100 else 120)) * land_area
            remaining_n_kg = max(0, target_n_kg - n_from_dap_kg)
            
            recommended_urea_kg = remaining_n_kg / 0.46
            urea_bags = round(recommended_urea_kg / 45, 1)

            recommended_mop_kg = (0 if k_val > 200 else (25 if k_val > 100 else 40)) * land_area
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
                st.info(f"🎉 **Quantum AI Savings Advisory:** Nitrogen is optimal. By adjusting N from DAP, you save approx **₹{int(saved_money)}** on Urea!")

        else:
            st.info("💡 Run the soil analysis in the 'Soil Test Portal' tab first to view customized calculations here.")

    # ---------------------------------------------------------
    # Expander Logic (Function ke andar sahi Indentation ke sath)
    # ---------------------------------------------------------
    st.markdown("---")
    with st.expander("📖 समझें: यह कैलकुलेटर खाद की बोरी की सही गणना कैसे करता है? (लॉजिक एवं उदाहरण)"):
        if is_hindi:
            st.markdown("""
            ### 🧪 वैज्ञानिक उर्वरक संतुलन लॉजिक (Agronomic Logic)
            
            प्रायः किसान यूरिया और DAP की गणना अलग-अलग करते हैं, जिससे मिट्टी में **नाइट्रोजन की ओवरडोज़ (ओवरडोज)** हो जाती है। 
            हमारा एआई मॉडल **DAP से मिलने वाले नाइट्रोजन को यूरिया में से घटाकर (Adjust)** सटीक बोरी निकालता है।

            #### 📊 मानक खाद अनुपात (Nutrient Values):
            * **DAP (50 kg बोरी):** इसमें **46% फास्फोरस** और **18% नाइट्रोजन** होता है (अर्थात् 1 बोरी DAP = 9 kg N + 23 kg P)।
            * **यूरिया (45 kg बोरी):** इसमें **46% नाइट्रोजन** होता है (अर्थात् 1 बोरी यूरिया = ~20.7 kg N)।
            * **MOP (50 kg बोरी):** इसमें **60% पोटाश** होता है।

            ---

            ### 🧮 उदाहरण (Example Scenario):
            मान लीजिए आपके **1 एकड़** खेत की मिट्टी जाँच रिपोर्ट (Soil Test) के अनुसार आपके खेत को **90 kg नाइट्रोजन** और **50 kg फास्फोरस** की आवश्यकता है:

            1. **चरण 1: DAP की गणना (Phosphorus first)**
               * 50 kg फास्फोरस की पूर्ति के लिए लगभग **1 बोरी (50 kg) DAP** की आवश्यकता होगी।
               
            2. **चरण 2: DAP से मिले नाइट्रोजन का हिसाब**
               * 1 बोरी (50 kg) DAP से मिट्टी को **9 kg नाइट्रोजन मुफ़्त में मिल गया**।
               * अब बची हुई आवश्यक नाइट्रोजन = $90 \\text{ kg} - 9 \\text{ kg} = \\mathbf{81 \\text{ kg Nitrogen}}$

            3. **चरण 3: यूरिया की बोरी की सही गणना**
               * 81 kg शुद्ध नाइट्रोजन के लिए यूरिया = $81 \\div 0.46 = \\mathbf{176 \\text{ kg यूरिया}}$
               * यूरिया की बोरी (45 kg) = $176 \\div 45 = \\mathbf{3.9 \\text{ बोरी यूरिया}}$

            > 💡 **निष्कर्ष:** यदि हम DAP के 9 kg N को न घटाते, तो आपको 4.3 बोरी यूरिया डालनी पड़ती। **DAP एडजस्टमेंट से आपके पैसे बचे और फसल यूरिया की ओवरडोज़ से बच गई!**
            """)
        else:
            st.markdown("""
            ### 🧪 Scientific Fertilizer Balancing Logic
            
            Farmers often calculate Urea and DAP separately, leading to **Nitrogen Overdosing**. 
            Our AI Engine credits the Nitrogen contained in DAP before calculating the required Urea bags.

            #### 📊 Standard Nutrient Percentages:
            * **DAP (50 kg bag):** Contains **46% Phosphorus** and **18% Nitrogen** (1 bag DAP = 9 kg N + 23 kg P).
            * **Urea (45 kg bag):** Contains **46% Nitrogen** (1 bag Urea = ~20.7 kg N).
            * **MOP (50 kg bag):** Contains **60% Potash**.

            ---

            ### 🧮 Calculation Example:
            Assume for a **1-Acre** field, the soil test target is **90 kg Nitrogen** and **50 kg Phosphorus**:

            1. **Step 1: DAP Calculation (Phosphorus target first)**
               * To supply ~50 kg Phosphorus, you need **1 Bag (50 kg) DAP**.
               
            2. **Step 2: Accounting Nitrogen from DAP**
               * 1 bag DAP automatically adds **9 kg Nitrogen** to the soil.
               * Remaining required Nitrogen = $90 \\text{ kg} - 9 \\text{ kg} = \\mathbf{81 \\text{ kg Nitrogen}}$

            3. **Step 3: Adjusted Urea Bags Calculation**
               * Urea required for 81 kg N = $81 \\div 0.46 = \\mathbf{176 \\text{ kg Urea}}$
               * Urea Bags (45 kg) = $176 \\div 45 = \\mathbf{3.9 \\text{ Bags of Urea}}$

            > 💡 **Takeaway:** Without adjusting DAP's Nitrogen, you would have bought 4.3 bags of Urea. **This logic saves money and prevents soil toxicity!**
            """)
