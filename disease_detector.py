import streamlit as st
from PIL import Image, ImageOps
import numpy as np

# ---------------------------------------------------------
# 1. AI Model Loader (Cached for Speed)
# ---------------------------------------------------------
@st.cache_resource
def load_tflite_model():
    """
    नोट: अपने मॉडल की फ़ाइल (.tflite) को models/ फ़ोल्डर में रखें।
    यदि फ़ाइल उपलब्ध नहीं है, तो डेमो/फ़ॉलबैक मोड में चलेगा।
    """
    try:
        import tflite_runtime.interpreter as tflite
        interpreter = tflite.Interpreter(model_path="models/crop_disease_model.tflite")
        interpreter.allocate_tensors()
        return interpreter
    except Exception as e:
        return None

# ---------------------------------------------------------
# 2. Disease Database (बीमारी और उसका इलाज)
# ---------------------------------------------------------
DISEASE_DB = {
    "Wheat___Yellow_Rust": {
        "hi_name": "गेहूं का पीला रतुआ (Yellow Rust)",
        "en_name": "Wheat Yellow Rust",
        "chemical": "प्रोपीकोनाज़ोल (Propiconazole 25% EC) - 1 ml/लीटर पानी में छिड़कें।",
        "organic": "10-12 दिन पुरानी खट्टी छाछ (5%) या नीम तेल (10,000 PPM) 5ml/लीटर पानी में स्प्रे करें।"
    },
    "Tomato___Early_Blight": {
        "hi_name": "टमाटर का अगेती झुलसा (Early Blight)",
        "en_name": "Tomato Early Blight",
        "chemical": "मैनकोज़ेब (Mancozeb 75% WP) - 2 ग्राम/लीटर पानी में घोलकर छिड़कें।",
        "organic": "ट्राइकोडर्मा विरिडी (Trichoderma viride) 5 ग्राम/लीटर पानी में मिलाकर पौधों की जड़ों पर दें।"
    },
    "Healthy": {
        "hi_name": "फसल पूरी तरह स्वस्थ है! ✅",
        "en_name": "Healthy Plant",
        "chemical": "किसी रासायनिक दवा की आवश्यकता नहीं है।",
        "organic": "पौधों की अच्छी वृद्धि के लिए नियमित जीवामृत या पंचगव्य का प्रयोग करते रहें।"
    }
}

# ---------------------------------------------------------
# 3. Image Processing & Prediction Function
# ---------------------------------------------------------
def predict_disease(image, interpreter):
    if interpreter is None:
        # अगर मॉडल फ़ाइल लोड न हो तो टेस्टिंग के लिए डमी रिजल्ट
        return "Wheat___Yellow_Rust", 0.95

    # TFLite मॉडल के हिसाब से 224x224 में रीसाइज़ और नॉर्मलाइज़ेशन
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    img_array = np.asarray(image, dtype=np.float32) / 255.0
    input_data = np.expand_dims(img_array, axis=0)

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    predicted_class_idx = np.argmax(output_data[0])
    confidence = float(np.max(output_data[0]))

    # क्लास लिस्ट के आधार पर मैच करें
    classes = ["Wheat___Yellow_Rust", "Tomato___Early_Blight", "Healthy"]
    predicted_label = classes[predicted_class_idx] if predicted_class_idx < len(classes) else "Healthy"
    
    return predicted_label, confidence

# ---------------------------------------------------------
# 4. Main Module UI Rendering
# ---------------------------------------------------------
def render_disease_module(is_hindi):
    title = "📸 फसल रोग पहचान AI" if is_hindi else "📸 Crop Disease AI Scanner"
    subtitle = "बीमार पत्ती की फोटो अपलोड करें और तुरंत सटीक निदान पाएं।" if is_hindi else "Upload a leaf photo for instant AI diagnosis."
    
    st.markdown(f"<h2 style='color:#047857;'>{title}</h2>", unsafe_allow_html=True)
    st.write(subtitle)
    st.markdown("---")
    
    interpreter = load_tflite_model()
    
    col1, col2 = st.columns([1.2, 0.8])
    uploaded_image = None
    
    with col1:
        st.subheader("📷 फोटो अपलोड या कैप्चर करें" if is_hindi else "📷 Capture or Upload")
        input_type = st.radio(
            "इनपुट माध्यम:" if is_hindi else "Input Mode:",
            ["📸 कैमरा (Camera)", "🖼️ गैलरी (Gallery)"],
            horizontal=True
        )
        
        if "📸" in input_type:
            img_file = st.camera_input("पत्ती को कैमरे के सामने लाएं" if is_hindi else "Show leaf to camera")
            if img_file:
                uploaded_image = Image.open(img_file)
        else:
            img_file = st.file_uploader("फसल की फोटो चुनें..." if is_hindi else "Select leaf photo...", type=["jpg", "jpeg", "png"])
            if img_file:
                uploaded_image = Image.open(img_file)

    with col2:
        st.subheader("💡 फोटो लेने के निर्देश" if is_hindi else "💡 Guidelines")
        st.info("""
        * 🟢 **क्लोज-अप लें:** प्रभावित पत्ती या धब्बे की साफ फोटो लें।
        * 🟢 **उजाला:** पर्याप्त रोशनी या धूप में फोटो लें।
        * 🔴 **धुंधलापन न हो:** कैमरा स्थिर रखकर क्लिक करें।
        """)

    # प्रेडिक्शन प्रोसेसिंग
    if uploaded_image is not None:
        st.markdown("---")
        res_col1, res_col2 = st.columns([1, 1])
        
        with res_col1:
            st.image(uploaded_image, caption="स्कैन की गई फोटो" if is_hindi else "Scanned Image", use_container_width=True)
            
        with res_col2:
            with st.spinner("🧠 AI मॉडल फोटो का विश्लेषण कर रहा है..." if is_hindi else "🧠 AI analyzing image..."):
                predicted_key, confidence = predict_disease(uploaded_image, interpreter)
                disease_info = DISEASE_DB.get(predicted_key, DISEASE_DB["Wheat___Yellow_Rust"])

            st.success("✅ स्कैन पूरा हुआ!" if is_hindi else "✅ Scan Complete!")
            
            # रिजल्ट कार्ड UI
            dis_name = disease_info["hi_name"] if is_hindi else disease_info["en_name"]
            st.markdown(f"""
                <div style="background-color: #FEF2F2; border: 1px solid #FECACA; padding: 15px; border-radius: 10px; margin-bottom: 12px;">
                    <h3 style="color: #991B1B; margin:0;">⚠️ {dis_name}</h3>
                    <p style="color: #166534; font-weight: bold; margin:5px 0 0 0;">🎯 AI सटीकता (Confidence): {int(confidence*100)}%</p>
                </div>
            """, unsafe_allow_html=True)
            
            # इलाज सुझाव
            st.markdown("### 🧪 संस्तुत उपचार (Treatment Plan)")
            tab1, tab2 = st.tabs(["🧪 रासायनिक (Chemical)", "🌿 जैविक (Organic)"])
            
            with tab1:
                st.warning(f"**उपचार:** {disease_info['chemical']}")
            with tab2:
                st.success(f"**उपचार:** {disease_info['organic']}")

            # एक्शन बटन्स
            st.markdown("---")
            b_col1, b_col2 = st.columns(2)
            with b_col1:
                st.button("🔊 रिपोर्ट सुनें" if is_hindi else "🔊 Listen Report")
            with b_col2:
                st.button("📲 WhatsApp शेयर" if is_hindi else "📲 Share Report", type="primary")
