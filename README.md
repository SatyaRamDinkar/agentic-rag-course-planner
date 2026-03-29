# AI Course Planning Assistant

## Setup

pip install -r requirements.txt

## Run Steps

1. Add your OpenAI API key:
   export OPENAI_API_KEY=your_key

2. Create vector DB:
   python src/vector_store.py

3. Run system:
   python src/rag_pipeline.py

4. Run evaluation:
   python evaluation/run_eval.py

5. Run UI:
   streamlit run app/app.py

## Features

* RAG-based QA
* Citation-based answers
* Safe fallback ("I don't know")


## Advanced Features

* Multi-agent system using CrewAI
* Verifier agent to reduce hallucinations
* Structured output enforcement
* Evaluation metrics included
* Safe abstention mechanism

