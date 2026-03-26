from sklearn.metrics.pairwise import cosine_similarity
import requests
import json
import config
from services.db_service import db_service

class RAGService:
    def get_embedding(self, text: str) -> list:
        url = f'{config.OLLAMA_BASE_URL}/api/embeddings'
        response = requests.post(url, json={'model':config.EMBEDDING_MODEL, 'prompt': text})
        response.raise_for_status()
        return response.json()["embedding"]
    def search_similar(self, question: str, top_k: int = 2) -> list:
        question_embedding = self.get_embedding(question)
        rows = db_service.get_all_faqs()
        similarities = []
        for row in rows:
            faq_id, category, faq_question, faq_answer, faq_embedding, dt = row
            faq_embedding = self.get_embedding(faq_question)
            # if isinstance(faq_embedding, str):
            #     faq_embedding = json.loads(faq_embedding)
            similarity = cosine_similarity([question_embedding],[faq_embedding])[0][0]

            similarities.append({
                    'id': faq_id,
                    'category': category,
                    'question': faq_question,
                    'answer': faq_answer,
                    'similarity': similarity
                })
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[:top_k]

    def build_context(self, results: list) -> str:
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(
                f'''
                    [Источник {i}]
                    Категория: {result['category']}
                    Вопрос: {result['question']}
                    Ответ: {result['answer']}
                '''
            )
        return '\n'.join(context_parts)

rag_service = RAGService()