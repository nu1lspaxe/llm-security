from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chat_models import init_chat_model
from langchain_community.vectorstores import FAISS
from langchain.schema import HumanMessage, AIMessage
from dotenv import load_dotenv, find_dotenv
import os
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Annotated



load_dotenv(find_dotenv())
os.environ["LANGSMITH_TRACING"] = "true"

# 定義狀態結構
class GraphState(TypedDict):
    question: str
    context: str
    answer: str
    documents: List
    section: str

def read_pdf_file(file_path):
    """
    讀取本地 PDF 檔案並返回其內容
    
    Args:
        file_path (str): PDF 檔案的本地路徑
    Returns:
        list: 包含每頁內容的 document 物件列表
    Raises:
        Exception: 如果發生錯誤
    """
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return documents
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
    
def create_vector_db_and_chatbot(file_path):
    """
    從 PDF 文件創建向量資料庫並初始化 Grok chatbot
    
    Args:
        file_path (str): PDF 文件的本地路徑
    Returns:
        tuple: (vector_store, chatbot, split_texts) 或 (None, None, None) 如果失敗
    """
    try:
        # 1. 讀取 PDF 文件
        docs = read_pdf_file(file_path)
        if not docs:
            raise Exception("Failed to load PDF documents")

        # 2. 分割文本
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        split_texts = text_splitter.split_documents(docs)
        print(f"Total split texts: {len(split_texts)}")

        # 3. 使用 Ollama (LLaMA3) 創建 embeddings
        embeddings = OllamaEmbeddings(
            model="llama3",
            base_url="http://localhost:11434"  # 假設 Ollama 運行在本地的預設端口
        )
        vector_store = FAISS.from_documents(split_texts, embeddings)
        print("Vector store initialized.")

        # 4. 初始化 Grok 作為 chatbot
        chatbot = init_chat_model(
            "llama3-8b-8192",  # 使用 Grok 的模型名稱，這裡假設為 llama3-8b-8192
            model_provider="groq",
        )
        print("Grok chatbot initialized.")

        return vector_store, chatbot, split_texts

    except Exception as e:
        print(f"Error in create_vector_db_and_chatbot: {str(e)}")
        return None, None, None
    
def query_chatbot(vector_store, chatbot, question, top_k=3):
    """
    使用向量資料庫和 chatbot 回答問題
    
    Args:
        vector_store: FAISS 向量資料庫
        chatbot: Grok chatbot 實例
        question (str): 用戶的問題
        top_k (int): 從向量資料庫中檢索的前 k 個相關文檔
    Returns:
        str: chatbot 的回答
    """
    try:
        # 從向量資料庫中檢索相關文檔
        retriever = vector_store.as_retriever(search_kwargs={"k": top_k})
        relevant_docs = retriever.get_relevant_documents(question)
        
        # 將相關文檔內容組合成上下文
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # 構建對話提示
        messages = [
            HumanMessage(content=f"Based on the following context:\n\n{context}\n\nAnswer the question: {question}")
        ]
        
        # 使用 Grok chatbot 生成回答
        response = chatbot.invoke(messages)
        return response.content if isinstance(response, AIMessage) else str(response)

    except Exception as e:
        print(f"Error in query_chatbot: {str(e)}")
        return "Sorry, I couldn't process your question."
    
def retrieve_documents(state: GraphState, vector_store, split_texts):
    """從向量資料庫或特定區段檢索相關文件"""
    question = state["question"]
    section = state["section"]

    if section == "full":
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        relevant_docs = retriever.invoke(question)
    else:
        embeddings = OllamaEmbeddings(model="llama3", base_url="http://localhost:11434")
        top_k = 3
        start_idx = {"beginning": 0, "middle": len(split_texts)//2, "end": len(split_texts)-top_k}[section]
        custom_docs = split_texts[start_idx:start_idx + top_k]
        custom_vector_store = FAISS.from_documents(custom_docs, embeddings)
        retriever = custom_vector_store.as_retriever(search_kwargs={"k": 3})
        relevant_docs = retriever.invoke(question)
        print(f"Section: {section}, Start index: {start_idx}, Docs length: {len(custom_docs)}")

    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    return {"documents": relevant_docs, "context": context}

def generate_answer(state: GraphState, chatbot):
    """使用 chatbot 生成回答"""
    question = state["question"]
    context = state["context"]
    messages = [
        HumanMessage(content=f"Based on the following context:\n\n{context}\n\nAnswer the question: {question}")
    ]
    response = chatbot.invoke(messages)
    return {"answer": response.content if isinstance(response, AIMessage) else str(response)}
    
def build_graph(vector_store, split_texts, chatbot):
    workflow = StateGraph(GraphState)

    # 添加節點
    workflow.add_node("retrieve", lambda state: retrieve_documents(state, vector_store, split_texts))
    workflow.add_node("generate", lambda state: generate_answer(state, chatbot))

    # 定義邊
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)

    # 設置入口點
    workflow.set_entry_point("retrieve")

    return workflow.compile()

if __name__ == "__main__":
    vector_store, chatbot, split_texts = create_vector_db_and_chatbot("logsign_siem.pdf")
    
    if vector_store and chatbot and split_texts:
        app = build_graph(vector_store, split_texts, chatbot)
        
        question = "What are the benefits of SIEM?"
        
        inputs = {"question": question, "section": "full"}
        result = app.invoke(inputs)
        print(f"\nQuestion: {question}")
        print(f"Answer (Full Document): {result['answer']}")
        
        embeddings = OllamaEmbeddings(model="llama3", base_url="http://localhost:11434")
        for section in ["beginning", "middle", "end"]:
            inputs = {"question": question, "section": section}
            result = app.invoke(inputs)
            print(f"Question: {question}")
            print(f"Answer: {result['answer']}")
        