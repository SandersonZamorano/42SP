## Análise de currículos com RAG

Este código implementa um sistema que utiliza **Recuperação de Informação Baseada em Representação (RAG)** para analisar currículos e responder perguntas sobre os candidatos. O sistema combina a busca semântica com um modelo de linguagem de grande porte (Gemini) para fornecer respostas completas e personalizadas.

## Componentes principais

1. **Interface Streamlit:**
    - A interface do usuário é construída com a biblioteca Streamlit, permitindo que os usuários interajam com o sistema de forma simples e intuitiva.
    - As funcionalidades da interface incluem:
        - Upload de arquivos PDF (currículos)
        - Campo de entrada de texto para perguntas sobre os candidatos
        - Exibição de resultados e respostas geradas pelo sistema
2. **ChromaDB:**
    - Um banco de dados vetorial utilizado para armazenar e realizar buscas em dados textuais.
    - O ChromaDB facilita a organização e o acesso aos dados dos currículos, permitindo a busca semântica eficiente.
3. **Sentence Transformers:**
    - Uma biblioteca que gera embeddings de frases, permitindo que textos sejam representados como vetores numéricos.
    - A função de embedding é usada para comparar a similaridade semântica entre as perguntas do usuário e o conteúdo dos currículos.
4. **PyPDF2:**
    - Uma biblioteca que permite a leitura e extração de texto de arquivos PDF.
    - A biblioteca é utilizada para extrair o conteúdo dos currículos, que serão processados pelo sistema.
5. **Google Gemini:**
    - Um modelo de linguagem de grande porte que gera respostas completas e personalizadas com base em um contexto fornecido.
    - O Gemini é utilizado para gerar respostas personalizadas às perguntas dos usuários sobre os candidatos, utilizando o contexto extraído dos currículos relevantes.

## Conceitos principais

- **RAG (Recuperação de Informação Baseada em Representação):** Uma técnica que combina a busca semântica com modelos de linguagem de grande porte para fornecer respostas mais precisas e contextualmente relevantes.
- **Embeddings:** Representações vetoriais de textos que capturam a similaridade semântica entre diferentes frases.
- **Busca Semântica:** Um tipo de busca que considera o significado do conteúdo, em vez de apenas correspondências exatas de palavras-chave.
- **Modelo de Linguagem de Grande Porte (LLM):** Um modelo de inteligência artificial que pode gerar texto, traduzir idiomas, escrever diferentes tipos de conteúdo criativo e responder a suas perguntas de forma informativa.

## Fluxo de funcionamento

1. **Upload de currículos:** O usuário carrega os currículos em formato PDF para o sistema.
2. **Processamento de currículos:**
    - Os arquivos PDF são processados usando a biblioteca PyPDF2 para extrair o texto de cada página.
    - O texto é dividido em pedaços (chunks) de tamanho pré-definido para facilitar o processamento.
    - Os chunks de texto são armazenados no ChromaDB com seus respectivos metadados (nome do arquivo, número da página, etc.).
3. **Busca semântica:**
    - O usuário insere uma pergunta sobre os candidatos.
    - A pergunta é convertida em um embedding usando a biblioteca Sentence Transformers.
    - O ChromaDB é usado para buscar os chunks de texto mais relevantes à pergunta, com base na similaridade semântica entre os embeddings.
4. **Geração de respostas:**
    - Os chunks de texto relevantes são fornecidos como contexto para o modelo de linguagem Gemini.
    - O Gemini gera uma resposta completa e personalizada à pergunta do usuário, utilizando o contexto dos currículos relevantes.
5. **Exibição de resultados:** A resposta gerada pelo Gemini é apresentada ao usuário na interface Streamlit.

## Benefícios do sistema

- **Análise eficiente de currículos:** O sistema automatiza a análise de currículos, permitindo que os usuários busquem informações relevantes de forma rápida e eficiente.
- **Respostas personalizadas:** O Gemini gera respostas completas e personalizadas, considerando o contexto dos currículos relevantes.
- **Busca semântica:** A busca semântica permite que o sistema encontre informações relevantes mesmo que as perguntas do usuário não contenham palavras-chave exatas.
- **Interface amigável:** A interface do usuário é simples e intuitiva, facilitando a interação com o sistema.
