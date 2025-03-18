```bash
llm-security/
├── main.py                   # 程式進入點，負責啟動系統
├── setup.py                  # 安裝與依賴管理腳本
├── README.md                 # 專案說明文件
├── config/                   # 設定檔目錄
│   ├── __init__.py
│   ├── config.yaml          # 系統參數（如模型路徑、log路徑等）
│   └── logging_config.py    # 日誌記錄設定
├── data_collection/          # 資料收集與處理模組
│   ├── __init__.py
│   ├── log_collector.py     # 從 /var/log/syslog 收集日誌
│   ├── data_processor.py    # 日誌資料預處理（過濾、格式化）
│   └── anomaly_detector.py  # 異常檢測邏輯（可結合 AI）
├── rag/                      # RAG（Retrieval-Augmented Generation）模組
│   ├── __init__.py
│   ├── generator.py         # 生成回應（使用 ChatOllama, model="llama3"）
│   ├── retriever.py         # 檢索相關資料
│   └── rag_pipeline.py      # RAG 完整流程整合
├── vector_database/          # 向量資料庫模組
│   ├── __init__.py
│   ├── index_builder.py     # 建立向量索引（使用 SentenceTransformer）
│   └── vector_store.py      # 向量儲存與查詢（使用 FAISS）
├── langchain_integration/    # LangChain 功能整合
│   ├── __init__.py
│   ├── chain_builder.py     # 定義 LangChain 的鏈（Chains）
│   └── memory_manager.py    # 管理對話記憶（Conversation Memory）
├── langgraph/                # LangGraph 工作流程模組
│   ├── __init__.py
│   ├── workflow.py          # 定義專家系統的工作流程圖
│   └── nodes/               # LangGraph 的節點定義
│       ├── __init__.py
│       ├── analysis_node.py # 分析日誌節點
│       └── alert_node.py    # 警報生成節點
├── langsmith/                # LangSmith 監控與調試模組
│   ├── __init__.py
│   └── tracing.py           # 追蹤與記錄模型行為
├── ai_agent/                 # AI-Agent 模組（專家系統核心）
│   ├── __init__.py
│   ├── agent_core.py        # AI 代理主邏輯
│   ├── tools/               # 代理可用的工具
│   │   ├── __init__.py
│   │   ├── log_analyzer.py  # 日誌分析工具
│   │   └── alert_generator.py # 警報生成工具
│   └── state_manager.py     # 代理狀態管理
├── utils/                    # 通用工具模組
│   ├── __init__.py
│   ├── file_utils.py        # 檔案處理工具
│   └── text_utils.py        # 文字處理工具
└── tests/                    # 測試模組
    ├── __init__.py
    ├── test_data_collection.py
    ├── test_rag.py
    └── test_agent.py
```