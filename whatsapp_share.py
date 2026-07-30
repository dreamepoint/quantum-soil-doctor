import urllib.parse

def get_whatsapp_share_url(crop_choice, n_value, p_value, k_value, ph_value, n_msg, p_msg, k_msg, ph_msg, is_hindi):
    """
    सॉइल हेल्थ रिपोर्ट के आधार पर WhatsApp URL तैयार करता है।
    """
    if is_hindi:
        message = f"""🌾 *मृदा स्वास्थ्य रिपोर्ट - ड्रीम मर्चेंट क्वांटम एआई* 🌾

*फसल:* {crop_choice}
----------------------------------
📊 *मिट्टी की स्थिति:*
• नाइट्रोजन (N): {n_value} kg/acre
• फॉस्फोरस (P): {p_value} kg/acre
• पोटेशियम (K): {k_value} kg/acre
• pH स्तर: {ph_value}

🔬 *क्वांटम एआई सिफारिशें:*
🌱 *नाइट्रोजन:* {n_msg}
🌾 *फॉस्फोरस:* {p_msg}
🍂 *पोटेशियम:* {k_msg}
🧪 *pH सुझाव:* {ph_msg}

----------------------------------
💡 *ड्रीम मर्चेंट सॉइल डॉक्टर द्वारा जनरेटेड*"""
    else:
        message = f"""🌾 *Soil Health Report - Dream Merchant Quantum AI* 🌾

*Crop:* {crop_choice}
----------------------------------
📊 *Soil Parameters:*
• Nitrogen (N): {n_value} kg/acre
• Phosphorus (P): {p_value} kg/acre
• Potassium (K): {k_value} kg/acre
• pH Level: {ph_value}

🔬 *Quantum AI Recommendations:*
🌱 *Nitrogen:* {n_msg}
🌾 *Phosphorus:* {p_msg}
🍂 *Potassium:* {k_msg}
🧪 *pH Advice:* {ph_msg}

----------------------------------
💡 *Generated via Dream Merchant Soil Doctor*"""

    encoded_message = urllib.parse.quote(message)
    return f"https://api.whatsapp.com/send?text={encoded_message}"
