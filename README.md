# 🎓 Agentic RAG Course Planning Assistant

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system for academic course planning using LangChain and CrewAI.

## Data Sources

This project uses a custom-built dataset consisting of computer science courses and their prerequisite relationships.

The dataset is inspired by real-world academic catalogs, including:

* MIT Course Catalog – https://catalog.mit.edu/ (Accessed: March 2026)
* Stanford Bulletin – https://bulletin.stanford.edu/ (Accessed: March 2026)
* Carnegie Mellon University Course Catalog – https://coursecatalog.web.cmu.edu/ (Accessed: March 2026)

These sources provide realistic course structures and prerequisite relationships, which were adapted to design the dataset used in this project.


## Features

* Prerequisite reasoning with eligibility decisions
* Course plan generation
* Strict citation enforcement (chunk-level)
* Safe abstention ("I don't know")
* Multi-agent architecture
* Evaluation metrics

## Tech Stack

* Python
* LangChain
* FAISS
* CrewAI

## Pipeline

1. Document ingestion
2. Chunking (500 size, 100 overlap)
3. Embeddings (OpenAI)
4. FAISS vector store
5. Retrieval (Top-k = 3)
6. LLM generation with strict prompts

## Run Instructions

### Step 1

pip install -r requirements.txt

### Step 2

export OPENAI_API_KEY=your_key

### Step 3

python src/vector_store.py

### Step 4

python src/rag_pipeline.py

### Step 5 (Evaluation)

python evaluation/run_eval.py

## Evaluation Metrics

* Citation Coverage
* Abstention Accuracy
* Structure Compliance

## Future Improvements

* Better agent coordination
* UI improvements
* Structured parsing of catalogs
