import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

baseUrl = "https://en.wikipedia.org/wiki/"

def getDataFromWiki(userParam):
    url = getUrl(baseUrl, userParam)
    
    response = requests.get(url)
    response.raise_for_status()
    soup = getHtmlFromWiki(response)

    paragraphs = getLinks(soup)
    return paragraphs

def getUrl(baseUrl, active):
    return baseUrl + active.replace(" ", "_")

def getHtmlFromWiki(data):
    return BeautifulSoup(data.text, 'html.parser')

def getLinks(soup):
    paragraphs = []
    body_content = soup.find('div', id='bodyContent')
    
    if body_content:
        for p in body_content.find_all('p'):
            para_text = p.get_text(strip=True)
            links = [
                a.get('title') for a in p.find_all('a') 
                if a.get('href') and a.get('title') 
                and "wikipedia/commons" not in a.get('href') 
                and a.parent.name not in ['i', 'em']
            ]
            paragraphs.append((para_text, links))
    return paragraphs

def getValidLinks(links):
    valid_links = []
    for title in links:
        if not any(char in title for char in [':', '#']):
            valid_links.append(title)
    return valid_links

def goToPhilosophy(starting_article):
    visited = set()
    current_article = starting_article
    count = 0

    while current_article != "Philosophy":
        if current_article in visited:
            return "It leads to an infinite loop!"
        
        visited.add(current_article)
        count += 1

        url = f'https://en.wikipedia.org/wiki/{quote(current_article)}'
        response = requests.get(url)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print(f"{current_article}")
        
        paragraphs = getLinks(soup)

        valid_links = getValidLinks([link for _, links in paragraphs for link in links])
        if not valid_links:
            return "It leads to a dead end!"
        
        current_article = valid_links[0]

    return f"{count} roads from {starting_article} to philosophy!"

def main():
    if len(sys.argv) < 2:
        print("Por favor, forneça uma palavra ou grupo de palavras.")
        return
    
    userParam = sys.argv[1]
    
    result = goToPhilosophy(userParam)
    print(result)

if __name__ == "__main__":
    main()
