import os
from langchain_core.documents import Document


def split_docs(documents, chunk_size=600, chunk_overlap=120):
    """Clean, high-performance chunker tailored for catalog documents without regex overhead."""
    chunks = []
    chunk_counter = 0

    for doc in documents:
        text = doc.page_content.strip()
        source = doc.metadata.get("source", "catalog_doc")
        doc_type = doc.metadata.get("doc_type", "course_description")

        # For standard short course descriptions (< 800 chars), keep each as an atomic chunk
        if len(text) <= chunk_size + 100:
            c = Document(
                page_content=text,
                metadata={
                    **doc.metadata,
                    "chunk_id": f"{source}#chunk_{chunk_counter}",
                    "chunk_index": chunk_counter
                }
            )
            chunks.append(c)
            chunk_counter += 1
        else:
            # Paragraph / section based splitting for longer policies and programs
            paragraphs = text.split("\n\n")
            current_text = ""
            for p in paragraphs:
                p = p.strip()
                if not p:
                    continue
                if len(current_text) + len(p) + 2 <= chunk_size:
                    current_text = f"{current_text}\n\n{p}".strip()
                else:
                    if current_text:
                        chunks.append(Document(
                            page_content=current_text,
                            metadata={
                                **doc.metadata,
                                "chunk_id": f"{source}#chunk_{chunk_counter}",
                                "chunk_index": chunk_counter
                            }
                        ))
                        chunk_counter += 1
                    current_text = p

            if current_text:
                chunks.append(Document(
                    page_content=current_text,
                    metadata={
                        **doc.metadata,
                        "chunk_id": f"{source}#chunk_{chunk_counter}",
                        "chunk_index": chunk_counter
                    }
                ))
                chunk_counter += 1

    return chunks
