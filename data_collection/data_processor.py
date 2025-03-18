from vector_database.index_builder import IndexBuilder
from rag.retriever import Retriever
from rag.generator import Generator

from config.logging import logger

class DataProcessor:
    def __init__(self):
        self.logs = []
        self.index_builder = IndexBuilder()
        self.retriever = Retriever(self.index_builder)
        self.generator = Generator()

    def process_log(self, log_line):
        """Process a single log line into a structured format."""
        parts = log_line.split(" ", 5)
        if len(parts) >= 6:
            timestamp = " ".join(parts[0:3])
            host = parts[3]
            source = parts[4]
            message = parts[5]
            return {"timestamp": timestamp, "host": host, "source": source, "message": message}
        logger.warning(f"Invalid log line format: {log_line}")
        return None

    def add_to_vector_db(self, log_dict):
        """Add processed log to the FAISS vector database."""
        if log_dict:
            self.index_builder.build_index([log_dict["message"]])
            self.logs.append(log_dict)
            logger.info(f"Added log to FAISS DB: {log_dict['message'][:50]}...")
        else:
            logger.error("Attempted to add null log to vector DB")

    def query(self, question):
        """Query the system with a question."""
        context = self.retriever.retrieve(question)
        logger.debug(f"Retrieved context for query: {question}")
        return self.generator.generate(context, question)