from setuptools import setup, find_packages

setup(
    name='llm-security',
    version='0.0.1',
    packages=find_packages(include=['rag', 'data_collection', 'vector_database']),
    install_requires=[
        'langchain',
        'langchain[groq]',
        'langchain-core',
        'langchain-ollama',
        'langchain-huggingface',
        'langchain-text-splitters',
        'langgraph',
        'sentence-transformers',
        'faiss-cpu',
    ],
)