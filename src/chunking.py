from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_docs(documents):
splitter = RecursiveCharacterTextSplitter(
chunk_size=500,
chunk_overlap=100
)

return splitter.create_documents(documents)



