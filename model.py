import os
import openai
from openai import OpenAI
from typing import List, Union, Dict

os.environ["http_proxy"] = "http://127.0.0.1:10809"
os.environ["https_proxy"] = "http://127.0.0.1:10809"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ChatModel():
    def __init__(self, 
                 model_name: str = "gpt-4-turbo",
                 max_tokens: int = 1024,
                 temperature: float = 0.0, 
                 n: int = 1
                 ):
        self.client = OpenAI(api_key = OPENAI_API_KEY)
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.n = n
    
    def generate(self, messages: List[Dict]) -> Union[List[str], str]:
        response = self.client.chat.completions.create(
            model = self.model_name,
            messages = messages,
            max_tokens = self.max_tokens,
            temperature = self.temperature,
            n = self.n
        )
        if self.n == 1:
            return response.choices[0].message.content  # type: ignore
        return [choice.message.content for choice in response.choices]  # type: ignore
