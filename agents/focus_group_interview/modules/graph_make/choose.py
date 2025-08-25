import os
from dotenv import load_dotenv

from google import genai
import enum

load_dotenv()

class TalkType(enum.Enum):
    NORMAL = "normal"
    FREETALK = "freetalk"
    SEQUENCE = "sequence"

class StartGraph():
    def __init__(self):

        self.client = genai.Client(api_key = os.getenv("GOOGLE_API_KEY"))

    def get_type(self, theme):

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{theme}를 보고 해결 하기에 적합한 talk type을 정해주세요",
            config={
                "response_mime_type": "application/json",
                "response_schema": TalkType,
                "temperature": 0.0,
                "seed": 42,
            }
        )

        return response


