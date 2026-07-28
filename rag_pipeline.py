from rag.retriever import retrieve
from rag.llm import ask_llm


def ask_document(question):
    # Retrieve relevant chunks
    results = retrieve(question)

    # If nothing is found
    if not results:
        return "No relevant information found in the document."

    # Build context
    context = "\n\n".join(
        result["text"] for result in results
    )

    # Ask the LLM
    answer = ask_llm(context, question)

    return answer