import os
import google.generativeai as genai
import re
from pprint import pprint

# Configure IA Models
genai.configure(api_key=os.environ.get("GEMINI_IA_API_KEY"))

def run_prompt_chain():
    results = []

    step_1 = """
        Forneça uma visão geral da vida e carreira de Claude Shannon.
        <OVERVIEW>
        [sua resposta aqui]
        </OVERVIEW>
    """
    overview_response = call_llm(step_1)
    overview_content = extract_content(overview_response, "OVERVIEW")

    step_2 = f"""
        Com base na visão geral da vida de Claude Shannon: "{overview_content}", 
        analise suas principais contribuições para a teoria da informação dentro das tags:
        <CONTRIBUTIONS>
        [sua resposta aqui]
        </CONTRIBUTIONS>
    """
    contributions_response = call_llm(step_2)
    contributions_content = extract_content(contributions_response, "CONTRIBUTIONS")

    step_3 = f"""
        Considerando a visão geral da vida de Claude Shannon: "{overview_content}" e suas contribuições para a teoria da informação: 
        "{contributions_content}", explore o impacto de seu trabalho na computação moderna e nas tecnologias de comunicação dentro das tags:
        <IMPACTS>
        [sua resposta aqui]
        </IMPACTS>
    """
    impacts_response = call_llm(step_2)
    impacts_content = extract_content(impacts_response, "IMPACTS")

    step_4 = f"""
        Com base nas informações anteriores:
        Visão geral: "{overview_content}", 
        Contribuições: "{contributions_content}", 
        Impacto: "{impacts_content}", faça uma análise abrangente sobre Claude Shannon dentro das tags:
        <SYNTHESIS>
        [análise completa aqui]
        </SYNTHESIS>
    """
    synthesis_response = call_llm(step_4)
    synthesis_content = extract_content(synthesis_response, "SYNTHESIS")
    
    # Resultado final
    print("[resultado final do encadeamento, apresentando uma análise abrangente sobre Claude Shannon]")
    print(synthesis_content)

    # Processar e exibir resultados


def call_llm(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    text_content = response.candidates[0].content.parts[0].text
    return text_content.strip()

def extract_content(text, tag):
    pattern = f"<{tag}>(.*?)</{tag}>"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else "Conteúdo não encontrado."

if __name__ == "__main__":
    run_prompt_chain()
