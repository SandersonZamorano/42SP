import os
import chromadb
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
from chromadb.config import Settings

def process_pdf_directory(pdf_directory, collection):
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith(".pdfs")]
    print(f"Encontrados {len(pdf_files)} arquivos PDF no diretório.")
    
    for idx, pdf_file in enumerate(pdf_files):
        print(f"Processando PDF {idx + 1}/{len(pdf_files)}: {pdf_file}")
        file_path = os.path.join(pdf_directory, pdf_file)
        
        text = extract_text_from_pdf(file_path)
        
        collection.add(
            documents=[text], 
            metadatas=[{"source": pdf_file}], 
            ids=[f"doc_{idx}"]
        )
        print(f"- Documento {pdf_file} processado e armazenado.")
    
    print("Processamento de todos os PDFs concluído.")

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def interactive_query_loop(collection, embedding_function):
    while True:
        query = input("\nConsulta: ")
        if query.lower() == 'sair':
            break
        
        query_embedding = embedding_function.encode([query])
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=3
        )
        
        print("\nResultados:")
        for i in range(len(results['documents'])):
            documents = results['documents'][i]
            metadatas = results['metadatas'][i]
            
            for doc, meta in zip(documents, metadatas):
                print(f"Documento: {meta['source']}")
                print(f"Trecho: {doc[:200]}...\n")

def main():
    pdf_directory = "./pdfs"
    persist_directory = "./chroma_persist_data"
    
    chroma_client = chromadb.PersistentClient(path=persist_directory)

    embedding_function = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    collection = chroma_client.get_or_create_collection(name="curriculos")

    process_pdf_directory(pdf_directory, collection)
    
    print("Processamento concluído. Iniciando modo de consulta.")
    interactive_query_loop(collection, embedding_function)

if __name__ == "__main__":
    main()
