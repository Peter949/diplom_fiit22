import requests
import config


class LLMService:
    def generate_answer(self, context: str, query: str) -> str:
        full_prompt = f"Используй данные: {context}\nВопрос: {query}"

        response = requests.post(
            f"{config.OLLAMA_BASE_URL}/api/generate",
            json={
                "model": config.CHAT_MODEL,
                "prompt": full_prompt,
                "stream": False
            }
        )
        return response.json()['response']


llm_service = LLMService()
