from sklearn.metrics.pairwise import cosine_similarity

class QueryRouter:
    def __init__(self, embedding_function):
        self.embedding_function = embedding_function
        self.examples = {
            "faq": [
                "Сколько багажа можно провозить?",
                "Как вернуть билет?",
                "Как пройти онлайн-регистрацию?",
                "Можно ли взять ручную кладь?"
            ],

            "flights": [
                "Когда вылетает рейс SU123?",
                "Есть ли рейс из Франкфурта в Париж?",
                "Хочу лететь из Санкт-Петербурга в Дубай",
                "Нужен рейс из Москвы в Якутск",
                "Подберите перелет в Токио",
                "Расписание рейсов Москва Якутск"
            ],

            "combined": [
                "Есть ли рейс в Париж и сколько багажа можно взять?",
                "Когда вылетает рейс и какие правила провоза багажа?",
                "Можно ли вернуть билет и узнать расписание рейсов?"
            ]
        }
        self.example_embeddings = {}
        for route, questions in self.examples.items():
            self.example_embeddings[route] = []
            for question in questions:
                embedding = self.embedding_function(question)
                self.example_embeddings[route].append(embedding)

    def average_similarity(self, query_embedding, embeddings):
        similarities = []
        for embedding in embeddings:
            similarity = cosine_similarity([query_embedding],[embedding])[0][0]
            similarities.append(similarity)
        return sum(similarities) / len(similarities)

    def route(self, query_embedding: list) -> dict:
        scores = {}
        for route, embeddings in self.example_embeddings.items():
            avg_similarity = self.average_similarity(query_embedding, embeddings)
            scores[route] = avg_similarity
        best_route = max(scores, key=scores.get)
        return {
            "route": best_route,
            "scores": scores
        }