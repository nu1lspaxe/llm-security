```bash
llm-security/
├── main.py                   # 程式進入點，負責啟動系統
├── setup.py                  # 安裝與依賴管理腳本
├── README.md                 # 專案說明文件
├── config/                   # 設定檔目錄
│   ├── __init__.py
│   └── logging_config.py    # 日誌記錄設定
├── data_collection/          # 資料收集與處理模組
│   ├── __init__.py
│   ├── log_collector.py     # 從 /var/log/syslog 收集日誌
│   └── data_processor.py    # 日誌資料預處理（過濾、格式化）
├── rag/                      # RAG（Retrieval-Augmented Generation）模組
│   ├── __init__.py
│   ├── generator.py         # 生成回應（使用 ChatOllama, model="llama3"）
│   └── retriever.py         # 檢索相關資料
└── vector_database/          # 向量資料庫模組
    ├── __init__.py
    ├── index_builder.py     # 建立向量索引（使用 SentenceTransformer）
    └── vector_store.py      # 向量儲存與查詢（使用 FAISS）
```