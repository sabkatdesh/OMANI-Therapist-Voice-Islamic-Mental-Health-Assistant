import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values
from typing import Callable, Optional

# Load environment variables
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("ASSISTANT_VOICE", "bn-BD-NabanitaNeural")  # Default to Bangla voice

# Bangla responses for long messages
BANGLA_RESPONSES = [
    "বাকি উত্তরটি চ্যাট স্ক্রিনে দেখানো হয়েছে, দয়া করে দেখুন।",
    "আপনি চ্যাট স্ক্রিনে বাকি অংশ দেখতে পাবেন।",
    "সম্পূর্ণ উত্তরটি চ্যাট স্ক্রিনে পাওয়া যাবে।",
    "অতিরিক্ত তথ্য চ্যাট স্ক্রিনে রয়েছে।",
    "আপনি চ্যাট স্ক্রিনে বাকি অংশ পড়তে পারবেন।"
]


async def TextToAudioFile(text: str) -> None:
    """Convert text to speech audio file"""
    file_path = r"Data\speech.mp3"

    if os.path.exists(file_path):
        os.remove(file_path)

    # Adjust voice parameters for Bangla
    communicate = edge_tts.Communicate(
        text,
        voice=AssistantVoice,
        pitch="+5Hz",
        rate="+10%",  # Slightly slower for Bangla
        volume="+0%"
    )
    await communicate.save(file_path)


def TTS(text: str, callback: Optional[Callable] = lambda r=None: True) -> bool:
    """Play text as speech with error handling"""
    while True:
        try:
            asyncio.run(TextToAudioFile(text))
            pygame.mixer.init()
            pygame.mixer.music.load(r"Data\speech.mp3")
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                if callback() is False:
                    break
                pygame.time.Clock().tick(10)
            return True

        except Exception as e:
            print(f"TTS Error: {e}")
            return False
        finally:
            try:
                callback(False)
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            except Exception as e:
                print(f"Cleanup Error: {e}")


def TextToSpeech(text: str, callback: Optional[Callable] = lambda r=None: True) -> None:
    """Smart speech output with length handling"""
    if not text:
        return

    # Split text into sentences
    sentences = [s.strip() for s in str(text).split(".") if s.strip()]

    # For long responses, speak first part and notify about the rest
    if len(sentences) > 50 and len(text) >= 10000:
        brief_response = ". ".join(sentences[:2]) + "."
        notification = random.choice(BANGLA_RESPONSES)
        full_response = f"{brief_response} {notification}"
        TTS(full_response, callback)
    else:
        TTS(text, callback)


def speak(text: str) -> None:
    """Simplified interface for external use"""
    TextToSpeech(text)