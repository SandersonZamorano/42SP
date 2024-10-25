import os
import google.generativeai as genai

# Configure IA Models
genai.configure(api_key=os.environ.get("GEMINI_IA_API_KEY"))

github_comments = [
	{
    	"text": "Ótimo trabalho na implementação desta feature! O código está limpo e bem documentado. Isso vai ajudar muito nossa produtividade.",
    	"sentiment": ""
	},
	{
    	"text": "Esta mudança quebrou a funcionalidade X. Por favor, reverta o commit imediatamente.",
    	"sentiment": ""
	},
	{
    	"text": "Podemos discutir uma abordagem alternativa para este problema? Acho que a solução atual pode causar problemas de desempenho no futuro.",
    	"sentiment": ""
	},
	{
    	"text": "Obrigado por relatar este bug. Vou investigar e atualizar a issue assim que tiver mais informações.",
    	"sentiment": ""
	},
	{
    	"text": "Este pull request não segue nossas diretrizes de estilo de código. Por favor, revise e faça as correções necessárias.",
    	"sentiment": ""
	},
	{
    	"text": "Excelente ideia! Isso resolve um problema que estávamos enfrentando há semanas. Mal posso esperar para ver isso implementado.",
    	"sentiment": ""
	},
	{
    	"text": "Esta issue está aberta há meses sem nenhum progresso. Podemos considerar fechá-la se não for mais relevante?",
    	"sentiment": ""
	},
	{
    	"text": "O novo recurso está causando conflitos com o módulo Y. Precisamos de uma solução urgente para isso.",
    	"sentiment": ""
	},
	{
    	"text": "Boa captura! Este edge case não tinha sido considerado. Vou adicionar testes para cobrir este cenário.",
    	"sentiment": ""
	},
	{
    	"text": "Não entendo por que estamos priorizando esta feature. Existem problemas mais críticos que deveríamos estar abordando.",
    	"sentiment": ""
	}
]

def create_prompt(comments):
    return f"""
    Antes de realizar qualquer trabalho, analise cautelosamente os itens entre as tags <EXEMPLO></EXEMPLO> e somente depois de ter entendido todo o conteúdo,
    prossiga com seu processamento. 
    Após entender todos os pontos anteriores, analise profundamente os pontos entre as tags <REGRAS></REGRAS>, e somente depois de ter entendido o conteúdo dela,
    continue com o seu trabalho.

    Nossa equipe de suporte de T.I (Tecnologia da Informação) está sobrecarregada com feedback não estruturado. Sua tarefa é
    analisar o feedback e categorizar os problemas para nossas equipes de produto, desenvolvimento e engenharia de software. Use estas
    categorias: Desempenho, estruturação de código, documentação, leitura do código, prazo para entrega. Avalie também o
    sentimento (Positivo/Neutro/Negativo) e a prioridade (Alta/Média/Baixa). Aqui está um exemplo:

    <EXEMPLO>
        Texto: O código dessa feature está mal organizado, não consigo ler com clareza e entender o que está acontecendo. Podemos não saber se está gargalando ou não!
        Sentimento: Negativo

        Texto: A feature foi entregue rapidamente. O usuário final ficará feliz em poder utilizá-las.
        Sentimento: Positivo
    </EXEMPLO>

    <REGRAS>
        Categorize os comentários com a mesma estrutura:

        Texto:
        Sentimento:

        Você não alterará o texto, descreverá exatamente o que é descrito no documento.
    </REGRAS>

    Comentários: {comments}
    """

def call_llm(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    text_content = response.candidates[0].content.parts[0].text
    return text_content.strip().replace('\n', '\n')

def parse_llm_response(response):
    sentiment_line = [line for line in response.splitlines() if "Sentimento:" in line]
    return sentiment_line[0].split(":")[1].strip() if sentiment_line else "Desconhecido"

def analyze_sentiments(comments):
    for comment in comments:
        prompt = create_prompt(comment["text"])
        llm_response = call_llm(prompt)
        comment["sentiment"] = parse_llm_response(llm_response)

    for comment in comments:
        print(f"Texto: {comment['text']}")
        print(f"Sentimento: {comment['sentiment']}")
        print("-" * 50)

analyze_sentiments(github_comments)
