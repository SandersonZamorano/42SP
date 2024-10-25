import streamlit as st
import os
import chromadb
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
import google.generativeai as genai  # Para a chamada ao Gemini

# Configurar a API do Gemini
genai.configure(api_key=os.getenv("GEMINI_IA_API_KEY"))

# Configurar o ChromaDB com persistência local
persist_directory = "./chroma_persist_data"
chroma_client = chromadb.PersistentClient(path=persist_directory)
embedding_function = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Função para chunking e processamento de PDFs
def process_pdf(pdf_file, collection):
    pdf_reader = PdfReader(pdf_file)
    text_chunks = []
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            chunks = [text[i:i+500] for i in range(0, len(text), 500)]
            text_chunks.extend(chunks)

    for idx, chunk in enumerate(text_chunks):
        collection.add(
            documents=[chunk], 
            metadatas=[{"source": pdf_file.name}], 
            ids=[f"doc_{pdf_file.name}_{idx}"]
        )

# Função para realizar a busca semântica
def semantic_search(query, collection):
    query_embedding = embedding_function.encode([query])
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=5
    )
    return results

# Função para gerar a resposta com o Gemini
def generate_response_with_gemini(results, user_query):
    # Preparar contexto recuperado para o Gemini
    context = ""
    for i in range(len(results['documents'])):
        for doc in results['documents'][i]:
            context += doc + "\n\n"
    
    # Adiciona a pergunta do usuário ao contexto
    full_prompt = (
        "Com base nos currículos apresentados, responda em português e forneça informações detalhadas conforme solicitado. "
        "Ao final das informações de cada candidato inclua o nome do arquivo do candidato:\n"
        f"{user_query}\n\n" + context
    )

    # Consultar Gemini
    print("Consultando Gemini...")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(full_prompt)
    text_content = response.candidates[0].content.parts[0].text
    
    return text_content.strip()

# Interface Streamlit
st.title("Análise de Currículos com RAG")

# Upload de arquivos PDF (currículos)
uploaded_files = st.file_uploader("1º Envie os currículos (PDF) e depois poderá fazer uma pergunta referente aos candidatos:", 
                                  accept_multiple_files=True, type=["pdf"])

# Processar currículos enviados
if uploaded_files:
    collection = chroma_client.get_or_create_collection(name="curriculos")
    
    with st.spinner('Processando currículos...'):
        for pdf_file in uploaded_files:
            process_pdf(pdf_file, collection)
        st.success("Currículos processados com sucesso!")

    # Campo de pergunta após o processamento
    query = st.text_input("2º Faça uma pergunta sobre os candidatos:")

    # Realizar busca e exibir resultados
    if query:
        with st.spinner('Realizando busca semântica...'):
            results = semantic_search(query, collection)
        
        with st.spinner('Gerando resposta com Gemini...'):
            formatted_response = generate_response_with_gemini(results, query)
            st.write(formatted_response)
