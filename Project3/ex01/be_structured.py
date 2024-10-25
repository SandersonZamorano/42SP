import os
import requests
import json
import google.generativeai as genai
from groq import Groq
from pprint import pprint

## Configure IA Models
genai.configure(api_key=os.environ["GEMINI_IA_API_KEY"])
client = Groq(api_key=os.environ.get("GROQ_API_KEY"),)

def gemini(prompt):

    print("Consultando Gemini...")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"{prompt}")
    text_content = response.candidates[0].content.parts[0].text
    return text_content.strip().replace('\n', '\n')

def groq(prompt):
    
    print("Consultando Groq...")

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{prompt}",
            }
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content

def ollama(prompt):
    print("Consultando o Ollama...")
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3.2:1b",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        response = response.text

        response_json = json.loads(response)
        
        formatted_response = response_json["response"].replace("\\n", "\n").replace("\\\"", "\"")
        
        return formatted_response.strip()

def formatPrompt(job_description):
    
    return f"""
    Você é um agente especializado em divulgar vagas de trabalho. Seu objetivo é estruturar as informações das vagas para que sejam legíveis e bem formatadas, aumentando a quantidade de candidaturas.

    Sua tarefa é a seguinte:

    Analisar cuidadosamente os requisitos da vaga fornecidos.
    Estruturar a vaga apenas com os seguintes pontos:
    Name of role
    Working hours
    Country
    Tech skills (entendidos como habilidades técnicas específicas, incluindo educação formal, faculdades, cursos e certificações)
    Você não deve adicionar informações que não estejam presentes nos requisitos enviados. Apresente a estrutura da seguinte maneira:

    * Name of role: [Nome da vaga]
    * Working hours: [Horário de trabalho]
    * Country: [País] 
    * Tech skills: [Habilidades técnicas]

    Exemplo:
    * Name of role: Pleno Software Engineer (BackEnd)
    * Working hours: 8-5 (Monday to Friday) - Remote or In Person
    * Country: United States
    * Tech skills: Python, Java, C#, programming methodologies and frameworks

    {job_description}
    """

def query_all_models(formatted_prompt):

    results = {}

    results["Groq"] = groq(formatted_prompt)
    results["Gemini"] = gemini(formatted_prompt)
    results["Ollama"] = ollama(formatted_prompt)
    
    return results

def main():
    with open("job_description.txt", "r") as file:
        job_description = file.read()
        formatted_prompt = formatPrompt(job_description)
        results = query_all_models(formatted_prompt)

        for model, response in results.items():
            print(f"\nAnálise do {model}:")
            print(response)
            print("-" * 50)

if __name__ == "__main__":
    main()