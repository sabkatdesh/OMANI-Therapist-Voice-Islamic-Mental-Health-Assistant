# main.py
from enegine_2_arabic import respond  # Your chatbot logic
from stt import get_recognized_text  # Speech-to-text
from tts import speak  # Text-to-speech
import gradio as gr
from crisis_detection import CrisisDetectorWithEmail


def process_voice():
    """Mimics terminal behavior but in Gradio"""
    try:
        # 1. Listen for voice input (auto-triggered)
        user_text = get_recognized_text()
        if not user_text:
            return "Could not detect speech. Try again."

        detector = CrisisDetectorWithEmail()
        is_crisis, details = detector.detect_crisis(user_text)

        # 2. Generate response
        bot_response = respond(user_text, history=None)



        # 3. Speak the response
        speak(bot_response)

        return f"👤 You: {user_text}\n\n🤖 Bot: {bot_response}"

    except Exception as e:
        return f"Error: {str(e)}"


# Simple Gradio UI
with gr.Blocks(title="Voice Counselor", theme=gr.themes.Soft()) as app:
    gr.Markdown("## 🎤 Islamic Voice Counselor")
    gr.Markdown("*Speak now - it's listening automatically*")

    # Auto-triggered voice input
    output = gr.Textbox(label="Conversation", interactive=False)
    record_btn = gr.Button("Start Listening", variant="primary")

    record_btn.click(
        fn=process_voice,
        outputs=output
    )

app.launch()

