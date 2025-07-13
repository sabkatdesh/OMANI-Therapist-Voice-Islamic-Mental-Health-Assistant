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
  GROQ_API_KEY="your_key"
  GOOGLE_API_KEY="your_key"
  ALERT_RECIPIENT="caregiver@example.com"

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




  
