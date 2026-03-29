import os

def load_documents(data_path):
documents = []


for file in os.listdir(data_path):
    if file.endswith(".txt"):
        with open(os.path.join(data_path, file), 'r', encoding='utf-8') as f:
            documents.append(f.read())

return documents


if **name** == "**main**":
docs = load_documents("data")
print(f"Loaded {len(docs)} documents")


