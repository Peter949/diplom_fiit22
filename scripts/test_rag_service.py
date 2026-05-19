from services.rag_service import rag_service

def test_search():
    question = "Расписание рейсов Москва?"
    results = rag_service.search_similar(question)
    for r in results:
        print(f"{r}\n")

if(__name__ == "__main__"):
    test_search()