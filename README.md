# OMANI-Therapist-Voice-Islamic-Mental-Health-Assistant

# 🎤 OMANI-Therapist-Voice  
**Voice-Based Islamic Mental Health Assistant in Omani Arabic**  

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)  

<div align="center">
  <img src="assets/demo.gif" width="70%" alt="Demo Conversation">
</div>

## 🌟 Features  
- **Omani Arabic Dialect Support**  
  - Culturally adapted responses (e.g., "وايد" instead of "الكثير")  
  - Islamic counseling framework with Quran/Hadith integration  

- **Real-Time Voice Pipeline**  
  - Speech-to-Text (Selenium Web Speech API)  
  - Text-to-Speech (Edge TTS with Omani prosody)  

- **Crisis Intervention**  
  - 15+ trigger phrase detection (Arabic/English)  
  - Email alerts + hotline referral (1111)  

- **Dual-LLM Architecture**  
  - Primary: Llama-4 (Groq)  
  - Validation: Gemini Flash  

## 🚀 Quick Start  

### Prerequisites  
- Python 3.10+  
- Chrome browser (for STT)  
- `.env` file with:  
  ```ini
  InputLanguage = ar-OM# 
  ASSISTANT_VOICE= ar-OM-AyshaNeural
  ALERT_RECIPIENT=*************@email.com
  SMTP_SENDER= !!!!!!!!!!!@email.com
  SMTP_PASSWORD=device_password
  SMTP_SERVER=smtp.gmail.com
  SMTP_PORT=587

Installation
git clone https://github.com/sabkatdesh/OMANI-Therapist-Voice-Islamic-Mental-Health-Assistant
.git
cd omani-therapist-voice
pip install -r requirements.txt

Usage:
python main.py  # Launches Gradio UI at http://localhost:7860

🛠️ Customization
Change Voice (TTS)
Modify .env:
ASSISTANT_VOICE="ar-OM-AyshaNeural"  # Female voice

- .env
- crisis_detection.py
- eenigne_2_arabic.py
- main.py
- requirements.txt.txt
- stt.py
- tts.py
- data/
    - arabic-coping-with-mental-health-crises-and-emergencies.pdf
    - CwC-2-2008-Arabic.pdf
    - Islamic-Spirituality-and-Mental-Well-Being-revised.pdf
    - ISLAMICALLY_INTEGRATED_Psychotherapy (1).pdf








  
