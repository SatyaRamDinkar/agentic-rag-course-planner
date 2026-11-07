import os
from langchain_core.documents import Document


def load_documents(data_path="data"):
    """Load all text catalog and policy documents with full file metadata.
    
    Args:
        data_path: Directory containing course catalog text files.
        
    Returns:
        List of LangChain Document objects with rich metadata.
    """
    documents = []
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data path '{data_path}' not found.")
        
    for filename in sorted(os.listdir(data_path)):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
                
            doc_type = "course_description"
            if "PROGRAM" in filename:
                doc_type = "program_requirements"
            elif "POLICY" in filename or "REGULATION" in filename:
                doc_type = "academic_policy"
                
            doc = Document(
                page_content=content,
                metadata={
                    "source": filename,
                    "filepath": filepath,
                    "doc_type": doc_type,
                    "doc_id": os.path.splitext(filename)[0]
                }
            )
            documents.append(doc)
            
    return documents


if __name__ == "__main__":
    docs = load_documents("data")
    print(f"Successfully loaded {len(docs)} catalog documents.")
    for d in docs[:3]:
        print(f" - {d.metadata['source']} ({d.metadata['doc_type']}, {len(d.page_content)} chars)")
