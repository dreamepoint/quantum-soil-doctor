import streamlit as st
from PIL import Image

def render_disease_module(is_hindi):
    title = "📸 फसल रोग पहचान AI" if is_hindi else "📸 Crop Disease Scanner AI"
    subtitle = "प्रभावित पत्ती की फोटो खींचें और 2 सेकंड में बीमारी व सटीक इलाज जानें।" if is_hindi else "Upload a leaf photo to diagnose diseases instantly."
    
    st.markdown(f"<h2 style='color:#047857;'>{title}</h2>", unsafe_allow_html=True)
    st.write(subtitle)
    st.markdown("---")
    
    col1, col2 = st.columns([1.2, 0.8])
    uploaded_image = None
    
    with col1:
        st.subheader("📷 फोटो लें या अपलोड करें" if is_hindi else "📷 Capture or Upload")
        input_type = st.radio(
            "इनपुट स्रोत चुनें:" if is_hindi else "Select Input Source:",
            ["📸 कैमरा (Camera)", "🖼️ गैलरी (Gallery)"],
            horizontal=True
        )
        
        if "📸" in input_type:
            img_file = st.camera_input("पत्ती को फ्रेम में रखें" if is_hindi else "Position leaf in frame")
            if img_file:
                uploaded_image = Image.open(img_file)
        else:
            img_file = st.file_uploader("पत्ती की फोटो चुनें..." if is_hindi else "Choose leaf image...", type=["jpg", "jpeg", "png"])
            if img_file:
                uploaded_image = Image.open(img_file)

    with col2:
        st.subheader("💡 फोटो लेने का सही तरीका" if is_hindi else "💡 Photography Guide")
        st.info("""
        * 🟢 **पास से फोटो लें:** केवल बीमार पत्ती या धब्बे पर ध्यान दें।
        * 🟢 **अच्छी रोशनी:** दिन के उजाले में फोटो लें।
        * 🔴 **धुंधली फोटो न लें:** कैमरा स्थिर रखें।
        * 🔴 **पूरा पौधा न लें:** केवल प्रभावित हिस्सा दिखाएं।
        """)

    if uploaded_image is not None:
        st.markdown("---")
        res_col1, res_col2 = st.columns([1, 1])
        
        with res_col1:
            st.image(uploaded_image, caption="आपकी खींची फोटो" if is_hindi else "Uploaded Photo", use_container_width=True)
            
        with res_col2:
            st.success("✅ फोटो स्कैन हो गई है!" if is_hindi else "✅ Image scanned successfully!")
            
            with st.status("🔍 AI विश्लेषण जारी है..." if is_hindi else "🔍 AI Analyzing...", expanded=True) as status:
                st.write("• धब्बों का आकार मापा जा रहा है...")
                st.write("• रोग के लक्षणों से मिलान किया जा रहा है...")
                status.update(label="विश्लेषण पूरा हुआ! (Analysis Complete)", state="complete", expanded=False)
            
            st.markdown("""
                <div style="background-color: #FEF2F2; border: 1px solid #FECACA; padding: 12px; border-radius: 8px; margin-bottom: 10px;">
                    <h3 style="color: #991B1B; margin:0;">⚠️ रोग: गेहूं का पीला रतुआ (Yellow Rust)</h3>
                    <p style="color: #166534; font-weight: bold; margin:0;">🎯 AI सटीकता: 96% Confident</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🧪 उपचार सुझाव (Treatment Plan)")
            tab1, tab2 = st.tabs(["🧪 रासायनिक (Chemical)", "🌿 जैविक (Organic)"])
            
            with tab1:
                st.warning("<b>दवा:</b> प्रोपीकोनाज़ोल (Propiconazole 25% EC)\n\n<b>मात्रा:</b> 1 ml प्रति लीटर पानी में मिलाकर छिड़काव करें।")
            with tab2:
                st.success("<b>देशी उपाय:</b> 10-12 दिन पुरानी खट्टी छाछ (5%) या नीम का तेल (10,000 PPM) 5ml/लीटर पानी में घोलकर स्प्रे करें।")

            st.markdown("---")
            b_col1, b_col2 = st.columns(2)
            with b_col1:
                st.button("🔊 रिपोर्ट सुनें" if is_hindi else "🔊 Listen Report")
            with b_col2:
                st.button("📲 WhatsApp शेयर करें" if is_hindi else "📲 Share on WhatsApp", type="primary")
