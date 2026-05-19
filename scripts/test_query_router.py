from services.query_router import query_router

def test_route():
    question = "Есть ли рейс в Париж и сколько багажа можно взять?"
    result = query_router.route(question)
    print("Выбранный маршрут:", result["route"])
    print("Оценки:")
    for route, score in result["scores"].items():
        print(f"{route}: {score:.4f}")

if __name__ == "__main__":
    test_route()