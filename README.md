## Text2Sql


## install reqs
```bash 
pip install -r requirements.txt
```

## activate the env
```bash
conda activate text2sql
```


## sys Architector 

```bash
text2sql/
│
├── app/
│   │
│   ├── core/
│   │   └── config.py          
│   │   └── database.py
│   │
│   ├── createdb/
│   │   └── categories.py       
│   │   └── customers.py
│   │   └── orderitems.py       
│   │   └── orders.py
│   │   └── products.py       
│   │   └── text2sql_base.py
│   │
│   ├── rag/
│   │   └── embedder.py    
│   │   └── retriver.py
│   │   └── schema_loader.py
│   │   └── test.py
│   │   └── vector_store.py
│   │
│   ├── llm/
│   │   └── generator.py       
│   │   └── prompt_builder.py  
│   │
│   ├── scripts/
│   │   └── test_service.py    
│   │   └── test_generator.py
│   │   └── test_db.py
│   │   └── seed_data.py
│   │   └── create_tables.py
│   │
│   ├── services/ 
│   │   └── text2sql_service.py
│   │
│   ├── training/ 
│   │   └── train_lora.py
│   │
│   └── api/ 
│       └── __init.py__
│       └── main.py
│       └── routes.py
│       └── schemas.py
│
├── data/
│   ├── merged-model/
│   │   └── faiss_index.bin 
│   │   └── texts.pkl        
│   └── processed/  
│       └── schema_texts.txt
│       └── schema.json       
│
├── Docker/
│   └── docker-compose.yml
│   
│
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── LICENCE
└── README.md
```