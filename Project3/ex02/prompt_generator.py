import os
import google.generativeai as genai
from pprint import pprint

## Configure IA Models
genai.configure(api_key=os.environ.get("GEMINI_IA_API_KEY"))

def create_prompt(role, task, topic, specific_question):
    
    return f"""
    Antes de prosseguir, examine cuidadosamente o conteúdo entre as tags <ROLE></ROLE>. Compreenda bem a proposta apresentada.
    Após entender o papel, analise profundamente as instruções entre as tags <TASK></TASK>.
    Em seguida, revise o conteúdo dentro das tags <TOPIC></TOPIC>, assegurando que tudo esteja claro.
    Depois, estude com atenção o material nas tags <QUESTION></QUESTION>. Certifique-se de entender firmemente o que foi proposto.

    Uma vez que todos os pontos tenham sido compreendidos, siga em frente com o processamento.

    Você adotará uma persona, nela, adotará a seguinte vocação:
    <ROLE>{role}</ROLE>
    Descreva detalhadamente o que você faz no seu dia a dia e o seu conhecimento.

    Após isso, você explicará cuidadosamente a seguinte atividade:
    <TASK>{task}</TASK>

    Em seguida, você dará uma análise sobre o seguinte ponto:
    <TOPIC>{topic}</TOPIC>

    E, só depois de ter detalhado todas essas informações, você dará um conceito geral sobre a questão:
    <QUESTION>{specific_question}</QUESTION>

    Você não deve adicionar informações que não estejam presentes nos requisitos enviados. Apresente a estrutura da seguinte maneira:

    ### 1. Explicação básica do conceito
    ### 2. Analogia do cotidiano
    ### 3. Solução passo a passo da pergunta:
    ### 4. Exemplo detalhado
        **Exemplo:**
            1. **Dúvida:** Posso duvidar da existência do mundo exterior.
            2. **Dúvida ainda maior:** Posso duvidar da existência do meu próprio corpo.
            3. **Certeza:** Não posso duvidar que estou duvidando, pois duvidar é uma forma de pensar.
            4. **Conclusão:** Se penso, logo existo ("Cogito, ergo sum").
    ### 5. Dica prática para iniciantes
    """

def send_to_gemini(promp):
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"{prompt}")
    text_content = response.candidates[0].content.parts[0].text
    return text_content.strip().replace('\n', '\n')


role = "especialista em conhecimento do esporte hipismo"
task = "explicar as regras do hipismo e seus métodos de avaliação"
topic = "Hipismo Brasileiro"
specific_question = "Qual a melhor raça de cavalo para iniciar no hipismo"
prompt = create_prompt(role, task, topic, specific_question)

response = send_to_gemini(prompt)
print("\nResposta do Gemini 1.5 Flash:")
print(response)