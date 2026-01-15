import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from html_to_markdown import convert

def fetch_doc_content_urls(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    docs_wrapper = soup.find("div", class_="documentation_info")
    docs_list = docs_wrapper.find_all("article", class_="documentation_body")
    
    for doc in docs_list:
        id = doc.get("id")
        content = convert(str(doc))
        with open(f"../docs/histudy/{id}.md", "w") as f:
            f.write(content)
            print(f"Saved {id}")



url = "https://rainbowthemes.net/docs/histudy-wp/"
fetch_doc_content_urls(url)