from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from config.logging import logger

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
        logger.info("Initialized Generator with Llama3 model")

    def generate(self, context, question):
        """Generate a response based on retrieved context and question."""
        try:
            response = self.document_chain.invoke({"context": context, "question": question})
            logger.debug(f"Generated response for question: {question}")
            return response
        except Exception as e:
            logger.error(f"Generation failed for question '{question}': {str(e)}")
            raise