import streamlit as st
from PIL import Image
import io
import requests

# ---------------------------------------------------------
# 1. Hugging Face Inference API Configuration
# ---------------------------------------------------------
# PlantVillage dataset पर ट्रेन्ड MobileNet V2 AI मॉडल
HF_API_URL = "https://api-inference.huggingface.co/models/linkanjarad/mobilenet_v2_1.0_224-plant-disease"

# 🔑 अपना Hugging Face Token यहाँ 'Bearer ' के आगे रखें
# Streamlit Secrets से टोकन लोड करें (GitHub Security Warn नहीं करेगा)
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

def query_huggingface_api(image_bytes):
    """
    Hugging Face API को इमेज बाइट्स भेजकर रिजल्ट प्राप्त करता है।
    """
    try:
        headers = {
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/octet-stream"
        }
        response = requests.post(
            HF_API_URL, 
            headers=headers, 
            data=image_bytes,
            timeout=20  # 20 सेकंड टाइमआउट ताकि स्लो नेटवर्क पर भी रिस्पॉन्स आ जाए
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

# ---------------------------------------------------------
# 2. Disease Translations & Treatment Database
# ---------------------------------------------------------
DISEASE_TRANSLATIONS = {
    # Apple
    "Apple___Apple_scab": ("सेब का स्कैब (Apple Scab)", "कैप्टन (Captan 50% WP) 2 ग्राम/लीटर का छिड़काव करें।", "नीम तेल (10,000 PPM) 5ml/लीटर का स्प्रे करें।"),
    "Apple___Black_rot": ("सेब का काला सड़न (Black Rot)", "कॉपर ऑक्सीक्लोराइड 3 ग्राम/लीटर पानी में घोलें।", "संक्रमित टहनियों और फलों को हटाकर जला दें।"),
    "Apple___Cedar_apple_rust": ("सेब का सिडार रस्ट (Cedar Apple Rust)", "मायक्लोबुटानिल (Myclobutanil) 1 ग्राम/लीटर का स्प्रे करें।", "संक्रमित पत्तियों को एकत्र कर नष्ट करें।"),
    "Apple___healthy": ("सेब का पौधा पूरी तरह स्वस्थ है! ✅", "किसी रासायनिक दवा की आवश्यकता नहीं है।", "जैविक खाद व पंचगव्य का नियमित उपयोग करें।"),
    
    # Corn (Maize)
    "Corn_(maize)___Common_rust_": ("मक्का का सामान्य रतुआ (Common Rust)", "मैनकोज़ेब (Mancozeb) 2.5 ग्राम/लीटर का स्प्रे करें।", "ट्राइकोडर्मा विरिडी 5 ग्राम/लीटर का उपयोग करें।"),
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": ("मक्का का भूरा लीफ स्पॉट (Gray Leaf Spot)", "एज़ोक्सीस्ट्रोबिन (Azoxystrobin) 1 ml/लीटर का स्प्रे करें।", "नीम का अर्क या छाछ का स्प्रे करें।"),
    "Corn_(maize)___Northern_Leaf_Blight": ("मक्का का उत्तरी पत्ती झुलसा (Northern Leaf Blight)", "प्रोपीकोनाज़ोल (Propiconazole) 1 ml/लीटर का स्प्रे करें।", "दशपर्णी अर्क 5% का छिड़काव करें।"),
    "Corn_(maize)___healthy": ("मक्का का पौधा पूरी तरह स्वस्थ है! ✅", "किसी दवा की आवश्यकता नहीं है।", "जीवामृत का छिड़काव करते रहें।"),

    # Potato
    "Potato___Early_blight": ("आलू का अगेती झुलसा (Potato Early Blight)", "मैनकोज़ेब (Mancozeb 75% WP) 2.5 ग्राम/लीटर का स्प्रे करें।", "खट्टी छाछ (5%) या नीम तेल का छिड़काव करें।"),
    "Potato___Late_blight": ("आलू का पछेती झुलसा (Potato Late Blight)", "साइमोक्सानिल + मैनकोज़ेब 2 ग्राम/लीटर पानी में घोलें।", "तांबे युक्त जैविक कवकनाशी का प्रयोग करें।"),
    "Potato___healthy": ("आलू का पौधा पूरी तरह स्वस्थ है! ✅", "किसी दवा की आवश्यकता नहीं है।", "जैविक खाद व वर्मीकंपोस्ट का प्रयोग जारी रखें।"),

    # Tomato
    "Tomato___Early_blight": ("टमाटर का अगेती झुलसा (Tomato Early Blight)", "कॉपर ऑक्सीक्लोराइड 3 ग्राम/लीटर का स्प्रे करें।", "ट्राइकोडर्मा विरिडी 5 ग्राम/लीटर जड़ों के पास दें।"),
    "Tomato___Late_blight": ("टमाटर का पछेती झुलसा (Tomato Late Blight)", "मैनकोज़ेब 2.5 ग्राम/लीटर पानी में मिलाकर स्प्रे करें।", "10-12 दिन पुरानी खट्टी छाछ का छिड़काव करें।"),
    "Tomato___Bacterial_spot": ("टमाटर का जीवाणु धब्बा (Bacterial Spot)", "स्ट्रेप्टोसाइक्लिन 1 ग्राम + कॉपर 30 ग्राम प्रति 10 लीटर पानी।", "नीम की खली व छाछ का प्रयोग करें।"),
    "Tomato___Leaf_Mold": ("टमाटर का लीफ मोल्ड (Leaf Mold)", "क्लोरोथैलोनिल (Chlorothalonil) 2 ग्राम/लीटर का स्प्रे करें।", "हवा का संचार बढ़ाएं और पत्तियां छांटें।"),
    "Tomato___Septoria_leaf_spot": ("टमाटर का सेप्टोरिया लीफ स्पॉट (Septoria Leaf Spot)", "मैनकोज़ेब (Mancozeb) 2.5 ग्राम/लीटर का छिड़काव करें।", "जैविक तांबा (Copper Fungicide) छिड़कें।"),
    "Tomato___Spider_mites Two-spotted_spider_mite": ("टमाटर में मकड़ी कीट (Spider Mites)", "एबामेक्टिन (Abamectin) 0.5 ml/लीटर का स्प्रे करें।", "नीम तेल (10,000 PPM) 5ml/लीटर का स्प्रे करें।"),
    "Tomato___Target_Spot": ("टमाटर का टारगेट स्पॉट (Target Spot)", "अज़ोक्सीस्ट्रोबिन 1 ml/लीटर पानी में छिड़कें।", "छाछ और गोमूत्र का 5% घोल छिड़कें।"),
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": ("टमाटर का पीला पत्ती मरोड़ा वायरस (Leaf Curl Virus)", "सफेद मक्खी नियंत्रण हेतु इमिडाक्लोप्रिड 0.5 ml/लीटर छिड़कें।", "पीले चिपचिपे कार्ड (Yellow Sticky Traps) लगाएं।"),
    "Tomato___Tomato_mosaic_virus": ("टमाटर का मोज़ेक वायरस (Mosaic Virus)", "संक्रमित पौधों को उखाड़कर तुरंत नष्ट करें।", "नीम तेल और साबुन के घोल का स्प्रे करें।"),
    "Tomato___healthy": ("टमाटर का पौधा पूरी तरह स्वस्थ है! ✅", "किसी रासायनिक दवा की आवश्यकता नहीं है।", "पंचगव्य का प्रयोग नियमित रूप से करें।"),

    # Pepper Bell (मिर्च)
    "Pepper,_bell___Bacterial_spot": ("मिर्च का जीवाणु धब्बा रोग (Bacterial Spot)", "कॉपर ऑक्सीक्लोराइड 3 ग्राम/लीटर पानी में घोलकर छिड़कें।", "स्यूडोमोनास फ्लोरेसेंस 10 ग्राम/लीटर का प्रयोग करें।"),
    "Pepper,_bell___healthy": ("मिर्च का पौधा पूरी तरह स्वस्थ है! ✅", "दवा की आवश्यकता नहीं है।", "जीवामृत का प्रयोग जारी रखें।"),

    # Grape (अंगूर)
    "Grape___Black_rot": ("अंगूर का ब्लैक रॉट (Black Rot)", "मायक्लोबुटानिल 1 ग्राम/लीटर का स्प्रे करें।", "संक्रमित गुच्छों को नष्ट करें।"),
    "Grape___Esca_(Black_Measles)": ("अंगूर का एस्का रोग (Black Measles)", "टैबुकोनाज़ोल 1 ml/लीटर पानी में स्प्रे करें।", "पौधे के कटे हुए हिस्सों पर बोर्डो पेस्ट लगाएं।"),
    "Grape___healthy": ("अंगूर का पौधा पूरी तरह स्वस्थ है! ✅", "दवा की आवश्यकता नहीं है।", "पंचगव्य दें।")
}

def clean_label(label_str):
    """
    यदि कोई बीमारी डेटाबेस में सीधे न मिले, तो उसके टेक्निकल कोड को साफ़ नाम में बदलता है।
    """
    clean = label_str.replace("___", " - ").replace("_", " ").title()
    return clean

# ---------------------------------------------------------
# 3. Main UI Module Rendering
# ---------------------------------------------------------
def render_disease_module(is_hindi):
    title = "📸 फसल रोग पहचान AI (Cloud API)" if is_hindi else "📸 AI Crop Disease Scanner"
    subtitle = "केवल बीमार पत्ती की फोटो अपलोड करें और तुरंत सटीक निदान पाएं।" if is_hindi else "Upload a leaf photo for instant AI diagnosis."
    
    st.markdown(f"<h2 style='color:#047857;'>{title}</h2>", unsafe_allow_html=True)
    st.write(subtitle)
    st.markdown("---")
    
    col1, col2 = st.columns([1.2, 0.8])
    uploaded_image = None
    image_bytes = None
    
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
                image_bytes = img_file.getvalue()
        else:
            img_file = st.file_uploader("फसल की फोटो चुनें..." if is_hindi else "Select leaf photo...", type=["jpg", "jpeg", "png"])
            if img_file:
                uploaded_image = Image.open(img_file)
                image_bytes = img_file.getvalue()

    with col2:
        st.subheader("💡 आवश्यक निर्देश" if is_hindi else "💡 Instructions")
        st.info("""
        * 🍃 **केवल पौधे/पत्ती की फोटो डालें:** केवल प्रभावित पत्ती या धब्बे की साफ़ फोटो लें।
        * 🚫 **कंप्यूटर/स्क्रीनशॉट न डालें:** स्क्रीनशॉट, इंसानों या कागज़ की फोटो को AI रिजेक्ट कर देगा।
        * 🟢 **पर्याप्त रोशनी:** रोशनी अच्छी हो ताकि बीमारी के लक्षण साफ़ दिखें।
        """)

    # ---------------------------------------------------------
    # 4. Processing Image via Hugging Face Cloud
    # ---------------------------------------------------------
    if uploaded_image is not None and image_bytes is not None:
        st.markdown("---")
        res_col1, res_col2 = st.columns([1, 1])
        
        with res_col1:
            st.image(uploaded_image, caption="स्कैन की गई फोटो" if is_hindi else "Scanned Image", use_container_width=True)
            
        with res_col2:
            with st.spinner("🧠 AI क्लाउड मॉडल फोटो का विश्लेषण कर रहा है..." if is_hindi else "🧠 Analyzing image..."):
                api_results = query_huggingface_api(image_bytes)

            # यदि API से रिस्पॉन्स मिलता है
            if api_results and isinstance(api_results, list) and len(api_results) > 0:
                top_prediction = api_results[0]
                label = top_prediction.get("label", "")
                confidence = float(top_prediction.get("score", 0.0))

                # 🛑 Non-Leaf / Invalid Screenshot Filter:
                # यदि मॉडल का Confidence Threshold 35% (0.35) से कम है, तो फोटो अवैध है।
                if confidence < 0.35:
                    st.error("❌ **अवैध फोटो! (Invalid Image)**")
                    st.markdown("""
                        <div style="background-color: #FEF2F2; border: 1px solid #FECACA; padding: 15px; border-radius: 10px; color: #991B1B;">
                            <b>⚠️ AI चेतावनी:</b><br>
                            यह फोटो किसी पौधे या फसल की पत्ती की नहीं लग रही है। कृपया केवल खेत से ली गई <b>पौधे की पत्ती/रोगग्रस्त हिस्से की साफ़ फोटो</b> अपलोड करें।
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.success("✅ स्कैन पूरा हुआ!" if is_hindi else "✅ Scan Complete!")
                    
                    # ट्रांसलेशन या फ़ॉलबैक
                    if label in DISEASE_TRANSLATIONS:
                        hi_name, chemical_rx, organic_rx = DISEASE_TRANSLATIONS[label]
                    else:
                        hi_name = clean_label(label)
                        chemical_rx = "व्यापक स्पेक्ट्रम कवकनाशी (Mancozeb 75% WP) - 2.5 ग्राम/लीटर का छिड़काव करें।"
                        organic_rx = "नीम तेल (10,000 PPM) 5ml/लीटर और खट्टी छाछ का छिड़काव करें।"

                    st.markdown(f"""
                        <div style="background-color: #ECFDF5; border: 1px solid #A7F3D0; padding: 15px; border-radius: 10px; margin-bottom: 12px;">
                            <h3 style="color: #065F46; margin:0;">⚠️ {hi_name}</h3>
                            <p style="color: #047857; font-weight: bold; margin:5px 0 0 0;">🎯 AI विश्वास स्तर (Confidence): {int(confidence * 100)}%</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("### 🧪 संस्तुत उपचार (Treatment Plan)")
                    tab1, tab2 = st.tabs(["🧪 रासायनिक (Chemical)", "🌿 जैविक (Organic)"])
                    
                    with tab1:
                        st.warning(f"**उपचार:** {chemical_rx}")
                    with tab2:
                        st.success(f"**उपचार:** {organic_rx}")

                    st.markdown("---")
                    b_col1, b_col2 = st.columns(2)
                    with b_col1:
                        st.button("🔊 रिपोर्ट सुनें" if is_hindi else "🔊 Listen Report")
                    with b_col2:
                        st.button("📲 WhatsApp शेयर" if is_hindi else "📲 Share Report", type="primary")

            else:
                st.warning("⚠️ सर्वर से जुड़ने में समय लग रहा है। कृपया फोटो पुनः अपलोड करें या 5 सेकंड बाद प्रयास करें।")
