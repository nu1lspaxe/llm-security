from vector_database.index_builder import IndexBuilder
from rag.retriever import Retriever
from rag.generator import Generator
import json

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
        return None

    def add_to_vector_db(self, log_dict):
        """Add processed log to the FAISS vector database."""
        if log_dict:
            self.index_builder.build_index([log_dict["message"]])
            self.logs.append(log_dict)
            print(f"Added log to FAISS DB: {log_dict['message'][:50]}...")

    def query(self, question):
        """Query the system with a question."""
        context = self.retriever.retrieve(question)
        return self.generator.generate(context, question)
