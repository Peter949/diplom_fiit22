from sklearn.metrics.pairwise import cosine_similarity
from services.query_router import QueryRouter
import requests
import config
from services.db_service import db_service

class RAGService:

    def get_embedding(self, text: str) -> list:
        url = f'{config.OLLAMA_BASE_URL}/api/embeddings'
        response = requests.post(url, json={'model':config.EMBEDDING_MODEL, 'prompt': text})
        response.raise_for_status()
        return response.json()["embedding"]
    def __init__(self):
        self.query_router = QueryRouter(self.get_embedding)
    def search_faq(self, question_embedding, top_k: int = 2) -> list:
        rows = db_service.get_all_faqs()
        similarities = []
        for row in rows:
            faq_id, category, faq_question, faq_answer, faq_embedding, dt = row
            faq_embedding = self.get_embedding(faq_question)
            similarity = cosine_similarity([question_embedding], [faq_embedding])[0][0]
            similarities.append({
                'type': 'faq',
                'id': faq_id,
                'category': category,
                'question': faq_question,
                'answer': faq_answer,
                'similarity': similarity
            })
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[:top_k]
    def search_flights(self, question_embedding, top_k: int = 2) -> list:
        rows = db_service.get_all_flights()
        similarities = []
        for row in rows:
            flight_id, flight_number, departure_airport, arrival_airport, intermediate_point, departure_days, departure_time, arrival_time, is_return, active, created_at = row
            flight_text = f"""
                                Рейс {flight_number}
                                из {departure_airport}
                                в {arrival_airport}
                                вылетает в {departure_time}
                                прилетает в {arrival_time}
                                выполняется {departure_days}
                                """
            flight_embedding = self.get_embedding(flight_text)
            similarity = cosine_similarity([question_embedding], [flight_embedding])[0][0]
            similarities.append({
                'type': 'flights',
                "id": flight_id,
                "flight_number": flight_number,
                "departure_airport": departure_airport,
                "arrival_airport": arrival_airport,
                "departure_days": departure_days,
                "departure_time": departure_time,
                "arrival_time": arrival_time,
                "similarity": similarity
            })
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        return similarities[:top_k]
    def search_similar(self, question: str):
        question_embedding = self.get_embedding(question)
        route = self.query_router.route(question_embedding)
        route = route["route"]
        if(route == "faq"):
            return self.search_faq(question_embedding)
        elif(route == "flights"):
            return self.search_flights(question_embedding)
        elif(route == "combined"):
            faq_results = self.search_faq(question_embedding)
            flight_results = self.search_flights(question_embedding)
            combined_results = faq_results + flight_results
            combined_results.sort(key=lambda x: x["similarity"], reverse=True)
            return combined_results[:2]

    def build_context(self, results: list) -> str:
        context_parts = []
        for i, result in enumerate(results, 1):
            if (result['type'] == 'faq'):
                context_parts.append(
                    f'''
                        [Источник {i}]
                        Категория: {result['category']}
                        Вопрос: {result['question']}
                        Ответ: {result['answer']}
                    '''
                )
            elif (result['type'] == 'flights'):
                context_parts.append(
                    f'''
                        [Источник {i}]
                        Рейс: {result['flight_number']}
                        Маршрут: {result['departure_airport']} -> {result['arrival_airport']}
                        Дни выполнения: {result['departure_days']}
                        Вылет: {result['departure_time']}
                        Прилет: {result['arrival_time']}
                    '''
                )
        return '\n'.join(context_parts)

rag_service = RAGService()