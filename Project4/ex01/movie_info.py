import os
import json
import google.generativeai as genai
from pprint import pprint

# Configure IA Models
genai.configure(api_key=os.environ.get("GEMINI_IA_API_KEY"))

movie_titles = [
    "The Matrix",
    "Inception",
    "Pulp Fiction",
    "The Shawshank Redemption",
    "The Godfather"
]

def create_prompt(movie_title):
    return f"""
    Você adotará uma persona especialista em buscar informações sobre filmes. Sua tarefa é
    analisar e coletar informações de filmes com base em seu título. Você fornecerá informações como nome, ano de lançamento do filme, nome do diretor, gêneros do filme e
    sinopse do filme.

    <EXEMPLO>
    {{
        "name": "Inception",
        "year": 2010,
        "director": "Christopher Nolan",
        "genre": ["Science Fiction", "Action"],
        "plot_summary": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO."
    }}
    </EXEMPLO>

    <REGRAS>
    Você retornará a resposta como um JSON válido, sem marcações de bloco de código.
    </REGRAS>

    Título do filme: {movie_title}
    """

def get_movie_info(movie_title):
    prompt = create_prompt(movie_title)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    raw_response = response.candidates[0].content.parts[0].text.strip()
    json_response = json.loads(raw_response)
    return json_response

for title in movie_titles:
    print(f"\nAnalyzing: {title} \n")
    result = get_movie_info(title)
    if result:
        print(f"title: {result['name']}")
        print(f"year: {result['year']}")
        print(f"director: {result['director']}")
        print(f"genre: {result['genre']}")
        print(f"plot_summary: {result['plot_summary']}")
    else:
        print("Error: Failed to generate valid JSON.")
    print("-" * 50)
