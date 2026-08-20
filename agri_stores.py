# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

# Dummy Store Data (Production me JSON/Database se load hoga)
STORES_DATA = [
    {
        "नाम": "किसान मित्र कृषि सेवा केंद्र",
        "लाइसेंस नंबर": "MP-461-FERT-2024",
        "पिनकोड": "461111",
        "शहर/तहसील": "इटारसी",
        "फोन": "+91 9826012345",
        "पता": "रेलवे ओवरब्रिज के पास, मेन रोड, इटारसी",
        "उपलब्ध ब्रांड्स": "IFFCO, KRIBHCO, Bayer, Mahyco",
        "वेरीफाइड": True
    },
    {
        "नाम": "कृषि धन खाद एवं बीज भंडार",
        "लाइसेंस नंबर": "MP-461-SEED-9081",
        "पिनकोड": "461111",
        "शहर/तहसील": "इटारसी",
        "फोन": "+91 9425098765",
        "पता": "बस स्टैंड के सामने, इटारसी",
        "उपलब्ध ब्रांड्स": "UPL, Syngenta, Tata Rallis",
        "वेरीफाइड": True
    },
    {
        "नाम": "सत्यम एग्रो एजेंसी",
        "लाइसेंस नंबर": "MP-462-CHEM-1102",
        "पिनकोड": "462001",
        "शहर/तहसील": "भोपाल",
        "फोन": "+91 9111054321",
        "पता": "करोंद मंडी रोड, भोपाल",
        "उपलब्ध ब्रांड्स": "Corteva, IFFCO, Godrej Agrovet",
        "वेरीफाइड": True
    }
]

def render_store_locator_module(is_hindi=True):
    title = "🏪 प्रमाणित खाद-बीज स्टोर (Verified Agri-Stores)" if is_hindi else "🏪 Verified Agri-Input Stores"
    st.subheader(title)
    
    st.info("🛡️ **AGRIQN सुरक्षा गारंटी:** केवल राज्य सरकार द्वारा जारी वैध लाइसेंस वाले प्रमाणित विक्रेताओं की सूची।" if is_hindi else "🛡️ Verified licensed dealers only.")

    # Search Bar
    search_pin = st.text_input(
        "🔍 अपने क्षेत्र का पिनकोड या शहर दर्ज करें (Enter Pincode or City):", 
        value="461111"
    ).strip()

    # Filter Logic
    filtered_stores = [
        store for store in STORES_DATA 
        if search_pin in store["पिनकोड"] or search_pin.lower() in store["शहर/तहसील"].lower()
    ]

    st.markdown("---")

    if filtered_stores:
        st.success(f"📍 {len(filtered_stores)} प्रमाणित स्टोर मिले (Stores Found)" if is_hindi else f"📍 Found {len(filtered_stores)} Verified Stores")
        
        for store in filtered_stores:
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"### {store['नाम']} ✅")
                    st.caption(f"📜 **लाइसेंस सं.:** {store['लाइसेंस नंबर']} | 📍 {store['शहर/तहसील']} ({store['पिनकोड']})")
                    st.write(f"🏢 **पता:** {store['पता']}")
                    st.write(f"🌱 **उपलब्ध ब्रांड्स:** `{store['उपलब्ध ब्रांड्स']}`")
                
                with col2:
                    st.markdown("#### संपर्क करें")
                    st.markdown(f"[📞 Call Store](tel:{store['फोन']})")
                    # Direct Google Maps Link
                    maps_url = f"https://www.google.com/maps/search/?api=1&query={store['नाम'].replace(' ', '+')}+{store['शहर/तहसील']}"
                    st.markdown(f"[🗺️ Map Location]({maps_url})")
                
                st.markdown("---")
    else:
        st.warning("⚠️ आपके दर्ज किए गए पिनकोड/शहर पर कोई सत्यापित स्टोर नहीं मिला।" if is_hindi else "⚠️ No verified store found in this area.")
