import logging, requests
from dotenv import load_dotenv
from Globals.Constants import Gemini_Api_Url, Gemini_Key

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class GeminiClient:
    def __init__(self):
        self.api_key = Gemini_Key
        self.api_url = Gemini_Api_Url

    async def chat(self, prompt: str) -> str:
        """Chat with Gemini AI"""
        headers = {"Content-Type": "application/json"}
        params = {"key": self.api_key}
        body = {"contents": [{"parts": [{"text": prompt}]}]}

        try:
            response = requests.post(self.api_url, headers=headers, params=params, json=body)
            response.raise_for_status()
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except requests.exceptions.RequestException as e:
            logger.error(f"Error communicating with Gemini API: {e}")
            return "I'm sorry, I couldn't connect to the AI service at the moment."
        except (KeyError, IndexError):
            logger.error("Unexpected response format from Gemini API.")
            return "I'm sorry, I received an unexpected response from the AI service."
