from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

class Generator:
    def __init__(self):
        self.llm = ChatOllama(
            model="llama3",
            base_url="http://localhost:11434", 
            temperature=0.7,
            max_tokens=512
        )

        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="Given these security events: {context}, answer the question: {question}"
        )
        self.document_chain = create_stuff_documents_chain(self.llm, self.prompt)

    def generate(self, context, question):
        """Generate a response based on retrieved context and question."""
        return self.document_chain.invoke({"context": context, "question": question})