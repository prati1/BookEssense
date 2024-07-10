from typing import List, Dict
from app.core.config import settings

class LLMClient:
    def __init__(self, llm_type: str, api_key: str):
        self.llm_type = llm_type
        self.api_key = api_key
        self.client = self._initialize_client()

    def _initialize_client(self):
        if self.llm_type == "openai":
            from langchain import OpenAI
            return OpenAI(api_key=self.api_key)
        elif self.llm_type == "claude":
            from anthropic import Anthropic
            return Anthropic(api_key=self.api_key)
        elif self.llm_type == "ollama":
            from langchain.llms import Ollama
            return Ollama(base_url=settings.ollama_base_url, model="qwen2:0.5b")
        else:
            raise ValueError("Unsupported LLM type")

    def analyze_characters(self, text: str) -> Dict[str, List[str]]:
        prompt = (
            "Analyze the following text and list out ALL characters and their relationships with each other.\n\n"
            f"{text}"
        )

        if self.llm_type == "openai":
            response = self.client(prompt)
        elif self.llm_type == "claude":
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
        elif self.llm_type == "ollama":
            response = self.client(prompt)
        return response
