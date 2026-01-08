import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from html_to_markdown import convert

def fetch_doc_content_urls(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    docs_wrapper = soup.find("div", class_="article-child")
    docs_list = docs_wrapper.find_all("a", href=True)
    docs_urls = {}

    for doc in docs_list:
        docs_urls[doc.text] = doc["href"]

    return docs_urls

def fetch_docs(doc_url):
    page = requests.get(doc_url)
    soup = BeautifulSoup(page.content, "html.parser")

    docs_wrapper = soup.find("div", class_="wedocs-single-content")
    docs_article = docs_wrapper.find("article")
    docs_body = docs_article.find("div", class_="entry-content")

    return docs_body

def save_docs_as_md(doc_name, doc_url):
    with open(f"../docs/extensions/{doc_name}.md", "w") as f:
        docs_body = fetch_docs(doc_url)
        f.write(convert(docs_body))
        print(f"Saved {doc_name}")

def get_doc_urls(url):
    links_json_path = Path("../docs/extensions/docs_urls.json")

    if links_json_path.is_file():
        with open(links_json_path, "r") as f:
            return json.load(f)
    else:
        docs_urls = fetch_doc_content_urls(url)
        with open(links_json_path, "w") as f:
            json.dump(docs_urls, f)
        return docs_urls


url = "https://diviessential.com/docs/divi-essential/extensions/"

doc_urls = get_doc_urls(url)

for doc_name, doc_url in doc_urls.items():
    save_docs_as_md(doc_name, doc_url)