from services.rag_service import rag_service

def test_search():
    question = "Какое количество багажа можно провозить?"
    results = rag_service.search_similar(question, top_k=2)
    for r in results:
        print(f"{r}\n")

if(__name__ == "__main__"):
    test_search()