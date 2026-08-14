import streamlit as st
import requests
from PIL import Image
import io

# ------------------------------------------------------------------
# 1. Hugging Face API Call (Raw Bytes Method - Fixes Error 400)
# ------------------------------------------------------------------
# ध्यान दें: यहाँ अपने Hugging Face मॉडल का सही URL रखें
HF_API_URL = "https://api-inference.huggingface.co/models/linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"

def query_huggingface_api(image_bytes):
    """
    Hugging Face Inference API को इमेज की बाइट्स भेजता है।
    """
    hf_token = st.secrets.get("HF_TOKEN")
    
    if not hf_token:
        st.error("⚠️ Secrets में HF_TOKEN नहीं मिला! कृपया Streamlit Secrets जांचें।")
        return None

    headers = {
        "Authorization": f"Bearer {hf_token}"
    }

    try:
        # सीधे इमेज बाइट्स पोस्ट कर रहे हैं (No JSON Wrapping, No Base64 Bug)
        response = requests.post(HF_API_URL, headers=headers, data=image_bytes, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 503:
            st.warning("⏳ मॉडल सर्वर पर लोड हो रहा है, कृपया 10-15 सेकंड बाद पुनः प्रयास करें...")
            return None
        else:
            st.error(f"🚨 Server Error Code: {response.status_code}")
            st.caption(f"Details: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        st.error("⏱️ API रिक्वेस्ट टाइम-आउट हो गई। कृपया दोबारा प्रयास करें।")
        return None
    except Exception as e:
        st.error(f"❌ कनेक्शन त्रुटि: {e}")
        return None

# ------------------------------------------------------------------
# 2. Main Render Function for Streamlit Page
# ------------------------------------------------------------------
def render_disease_module(is_hindi=True):
    # हेडिंग्स (भाषा अनुसार)
    title = "📸 फसल रोग पहचान AI (Cloud API)" if is_hindi else "📸 Crop Disease Scanner AI (Cloud API)"
    sub_title = "केवल बीमार पत्ती की फोटो अपलोड करें और तुरंत सटीक निदान पाएं।" if is_hindi else "Upload an image of an infected plant leaf for instant diagnosis."
    
    st.markdown(f"## {title}")
    st.caption(sub_title)
    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📷 फोटो अपलोड या कैप्चर करें" if is_hindi else "📷 Upload or Capture Photo")
        
        # इनपुट सोर्स (कैमरा या गैलरी)
        input_source = st.radio(
            "इनपुट माध्यम:" if is_hindi else "Input Source:",
            ["कैमरा (Camera)", "गैलरी (Gallery)"],
            horizontal=True
        )

        uploaded_file = None
        if "कैमरा" in input_source or "Camera" in input_source:
            uploaded_file = st.camera_input("पत्ती की फोटो खींचें" if is_hindi else "Take leaf photo")
        else:
            uploaded_file = st.file_uploader(
                "कपास या फसल की फोटो चुनें..." if is_hindi else "Choose leaf photo...", 
                type=["jpg", "jpeg", "png"]
            )

    with col2:
        st.markdown("### 💡 आवश्यक निर्देश" if is_hindi else "💡 Important Guidelines")
        info_text = """
        * 🌿 **केवल पौधे/पत्ती की फोटो डालें:** केवल प्रभावित पत्ती या धब्बे की साफ फोटो लें।
        * 🚫 **कंप्यूटर/स्क्रीनशॉट न डालें:** स्क्रीनशॉट, इंसानों या कागज की फोटो को AI रिजेक्ट कर देगा।
        * 🟢 **पर्याप्त रोशनी:** रोशनी अच्छी हो ताकि बीमारी के लक्षण साफ दिखें।
        """ if is_hindi else """
        * 🌿 **Crop Leaves Only:** Take a clear close-up photo of the infected leaf/spot.
        * 🚫 **No Screenshots:** Do not upload images of paper, people, or digital screens.
        * 🟢 **Good Lighting:** Ensure proper lighting for accurate detection.
        """
        st.info(info_text)

    # ------------------------------------------------------------------
    # 3. Image Processing & AI Detection
    # ------------------------------------------------------------------
    if uploaded_file is not None:
        st.markdown("---")
        res_col1, res_col2 = st.columns([1, 1])

        # इमेज प्रिव्यू
        with res_col1:
            st.image(uploaded_file, caption="आपकी अपलोड की गई फोटो" if is_hindi else "Uploaded Photo", width='stretch')

        # AI स्कैनिंग
        with res_col2:
            st.markdown("### 🔍 AI निदान परिणाम" if is_hindi else "🔍 AI Diagnosis Result")
            
            with st.spinner("AI फसल की जांच कर रहा है..." if is_hindi else "AI is analyzing the leaf..."):
                # 1. फोटो की Raw Bytes निकालें
                image_bytes = uploaded_file.getvalue()
                
                # 2. API कॉल करें
                predictions = query_huggingface_api(image_bytes)

            # 3. परिणाम दिखाएं
            if predictions and isinstance(predictions, list) and len(predictions) > 0:
                top_pred = predictions[0]
                label = top_pred.get("label", "Unknown Disease")
                score = top_pred.get("score", 0.0) * 100

                st.success("✅ विश्लेषण सफलतापूर्वक पूरा हुआ!" if is_hindi else "✅ Analysis Completed Successfully!")
                
                st.metric(
                    label="संभावित बीमारी / स्थिति" if is_hindi else "Detected Condition", 
                    value=label
                )
                st.metric(
                    label="AI विश्वसनीयता (Confidence)" if is_hindi else "AI Confidence Score", 
                    value=f"{score:.2f}%"
                )

                st.progress(min(int(score), 100))
