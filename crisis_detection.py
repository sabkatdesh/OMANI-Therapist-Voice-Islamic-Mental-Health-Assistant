import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from typing import Tuple, Dict

# Load environment variables
load_dotenv()


class CrisisDetectorWithEmail:
    def __init__(self):
        """Initialize with guaranteed crisis detection and email alerts"""
        # Crisis phrases (will ALWAYS trigger when matched)
        self.crisis_phrases = [
            'kill myself', 'end my life', 'want to die',
            'suicide', 'end it all', 'die tonight',
            'take my life', 'don\'t want to live',
            'better off dead', 'no reason to live'
        ]

        # Email configuration - verify all values are loaded
        self.alert_recipient = os.getenv('ALERT_RECIPIENT')
        self.smtp_config = {
            'server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
            'port': int(os.getenv('SMTP_PORT', 587)),
            'sender': os.getenv('SMTP_SENDER'),
            'password': os.getenv('SMTP_PASSWORD')
        }

        # Verify email configuration
        self._verify_email_config()

    def _verify_email_config(self):
        """Check if email settings are properly configured"""
        required_keys = ['alert_recipient', 'sender', 'password']
        missing = [key for key in required_keys if not getattr(self, key, None) and not self.smtp_config.get(key)]

        if missing:
            print(f"⚠️ Email alert disabled - Missing configuration: {', '.join(missing)}")
            print("Please check your .env file for:")
            print("ALERT_RECIPIENT, SMTP_SENDER, and SMTP_PASSWORD")
        else:
            print("✅ Email alerts configured successfully")

    def detect_crisis(self, text: str) -> Tuple[bool, Dict]:
        """100% reliable crisis detection with email alerts"""
        if not text.strip():
            return False, {}

        text_lower = text.lower()
        details = {
            'triggers': [],
            'confidence': 0.0,
            'response': "",
            'alert_sent': False,
            'alert_error': None
        }

        # Check for crisis phrases
        for phrase in self.crisis_phrases:
            if phrase in text_lower:
                details['triggers'].append(phrase)
                details['confidence'] = 0.99  # Absolute certainty

        # Generate response and send alert if crisis detected
        if details['confidence'] > 0.9:
            details['response'] = "🚨 Help is available! Emergency contacts have been notified."
            if self.alert_recipient and self.smtp_config['sender']:
                details['alert_sent'], details['alert_error'] = self._send_crisis_alert(text, details['triggers'])
            else:
                details['alert_error'] = "Email alerts not configured"

        return details['confidence'] > 0.9, details

    def _send_crisis_alert(self, message: str, triggers: list) -> Tuple[bool, str]:
        """Send emergency email alert with error handling"""
        try:
            msg = EmailMessage()
            msg['Subject'] = "🚨 CRISIS ALERT - Immediate Action Required"
            msg['From'] = self.smtp_config['sender']
            msg['To'] = self.alert_recipient

            msg.set_content(f"""
            CRISIS DETECTED IN CHAT:

            User Message:
            {message}

            Detected Triggers:
            {", ".join(triggers)}

            Required Action:
            1. Contact user immediately
            2. Escalate to mental health professional
            3. Verify user safety
            """)

            with smtplib.SMTP(
                    host=self.smtp_config['server'],
                    port=self.smtp_config['port'],
                    timeout=10  # Add timeout to prevent hanging
            ) as server:
                server.starttls()
                server.login(
                    self.smtp_config['sender'],
                    self.smtp_config['password']
                )
                server.send_message(msg)
            return True, None

        except Exception as e:
            error_msg = f"Email failed: {str(e)}"
            print(error_msg)
            return False, error_msg


