from setuptools import setup

setup(
    name='llm-security',
    version='0.0.1',
    install_requires=[
        'langchain-community==0.3.19',
        'langchain-ollama==0.2.3',
        'langchain[groq]==0.3.20',
        'langchain-text-splitters==0.3.6',
        'langgraph==0.3.5',
        'beautifulsoup4==4.13.3',
        'faiss-cpu',
        'pypdf'
    ],
)