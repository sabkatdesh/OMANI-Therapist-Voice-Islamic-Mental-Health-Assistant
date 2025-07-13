from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import time
import mtranslate as mt

# Load environment variables
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en-US")  # Default to English

# HTML Template for Speech Recognition
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;
        let isRecognizing = false;

        function startRecognition() {
            if (isRecognizing) return;

            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = '{LANGUAGE}';
            recognition.continuous = true;
            recognition.interimResults = false;
            isRecognizing = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript + ' ';
            };

            recognition.onerror = function(event) {
                console.error('Recognition error:', event.error);
                isRecognizing = false;
            };

            recognition.onend = function() {
                if (isRecognizing) recognition.start();
            };

            recognition.start();
        }

        function stopRecognition() {
            if (!isRecognizing) return;
            isRecognizing = false;
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# Initialize HTML file for recognition
def _setup_html():
    html_content = HTML_TEMPLATE.replace('{LANGUAGE}', InputLanguage)
    os.makedirs(os.path.join('Data'), exist_ok=True)
    with open(os.path.join('Data', 'Voice.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

_setup_html()  # Ensure HTML file is ready

# Initialize WebDriver
def _initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    chrome_options.add_argument("--use-fake-device-for-media-stream")
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

# Text processing utilities
def _query_modifier(query):
    if not query:
        return ""
    query = query.lower().strip().rstrip('.?!')
    is_question = any(query.startswith(word) for word in
                     ["how", "what", "where", "who", "whom", "whose", "can you", "what is", "where is"])
    return f"{query}{'?' if is_question else '.'}".capitalize()

def _universal_translator(text):
    if not text or InputLanguage.lower().startswith('en'):
        return text.capitalize() if text else ""
    try:
        return mt.translate(text, "en", "auto").capitalize()
    except Exception as e:
        print(f"Translation error: {e}")
        return text.capitalize()

# Core recognition function
def get_recognized_text(timeout=20):
    driver = _initialize_driver()
    try:
        driver.get(f"file:///{os.path.abspath('Data/Voice.html')}")
        driver.find_element(By.ID, "start").click()

        last_text = ""
        start_time = time.time()

        while time.time() - start_time < timeout:
            current_text = driver.find_element(By.ID, "output").text.strip()

            if current_text and len(current_text.split()) >= 2:
                driver.find_element(By.ID, "end").click()
                return _query_modifier(_universal_translator(current_text))

            time.sleep(0.5)

        return ""
    finally:
        driver.quit()

# Continuous listening (optional)
def listen(callback, timeout=60):
    """
    Continuously listens for speech and calls `callback(text)` when detected.
    Args:
        callback (function): Function to call with recognized text.
        timeout (int): Timeout per listening session. Default: 60.
    """
    while True:
        text = get_recognized_text(timeout)
        if text:
            callback(text)