import sys
import requests
import dewiki
from pprint import pprint

def getGeneralDataFromWiki(userParam):
    baseUrl = "https://pt.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": userParam,
    }

    response = requests.get(baseUrl, params=params)

    if response.status_code == 200:
        return response.json()
    return None

def getPageIdFromFirstObject(data):
    if "query" in data and "search" in data["query"]:
        search_results = data["query"]["search"]
        if search_results:
            return search_results[0]["pageid"]
        if "searchinfo" in data["query"] and "suggestion" in data["query"]["searchinfo"]:
            return data["query"]["searchinfo"]["suggestion"]
    return None

def getSpecificDataFromWiki(pageId):
    baseUrl = "https://pt.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "pageid": pageId,
        "format": "json",
        "prop": "wikitext",
        "disableeditsection": 1,
    }

    response = requests.get(baseUrl, params=params)

    if response.status_code == 200:
        return dewiki.from_string(response.json()["parse"]["wikitext"]["*"])
    return None

def saveFile(userParam, content):
    filename = userParam.replace(" ", "_") + ".wiki"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)
    print("Arquivo salvo com sucesso!")

def main():
    userParam = sys.argv[1]
    data = getGeneralDataFromWiki(userParam)

    if data:
        pageId = getPageIdFromFirstObject(data)
        if isinstance(pageId, str):
            print(f"Não foi encontrado nenhum resultado para {userParam}, você quis dizer'{pageId}'?")
            userParam = input("Digite um novo termo: ")
            data = getGeneralDataFromWiki(userParam)
            pageId = getPageIdFromFirstObject(data)

        if pageId is not None:
            content = getSpecificDataFromWiki(pageId)
            if content:
                saveFile(userParam, content)
            else:
                print("Nenhum conteúdo encontrado para a página.")
        else:
            print("Nenhum resultado encontrado.")
    else:
        print("Erro ao buscar dados da Wikipedia.")

if __name__ == "__main__":
    main()
