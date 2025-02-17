import os
from typing import List
import requests
from bs4 import BeautifulSoup
import re

import html2text
from requests_html import HTMLSession

MAX_URL = 150 # max number of URLs to be scraped
page = requests.get('https://yourwebpage/') # initial page
keyword = 'page' # mandatory word to filter the links
soup = BeautifulSoup(page.content, 'lxml')
data = []
links = []

def download_and_save_in_markdown(url: str, dir_path: str) -> None:
    """Download the HTML content from the web page and save it as a markdown file."""
    # Extract a filename from the URL
    if url.endswith("/"):
        url = url[:-1]

    filename = url.split("/")[-1] + ".md"
    print(f"Downloading {url} into {filename}...")

    session = HTMLSession()
    response = session.get(url, timeout=30)

    # Render the page, which will execute JavaScript
    response.html.render()

    # Convert the rendered HTML content to markdown
    h = html2text.HTML2Text()
    markdown_content = h.handle(response.html.raw_html.decode("utf-8"))

    # Write the markdown content to a file
    filename = os.path.join(dir_path, filename)
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(markdown_content)


def download(pages: List[str]) -> str:
    """Download the HTML content from the pages and save them as markdown files."""
    # Create the content/notion directory if it doesn't exist
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dir_path = os.path.join(base_dir, "content", "blogs")
    os.makedirs(dir_path, exist_ok=True)
    for page in pages:
        download_and_save_in_markdown(page, dir_path)
    return dir_path


def remove_duplicates(l): # remove duplicates and unURL string
    for item in l:
        match = re.search("(?P<url>https?://[^\s]+)", item)
        if match is not None:
            links.append((match.group("url")))


for link in soup.find_all('a', href=True):
    href = link.get('href')
    if keyword in href:
        data.append(str(href))

flag = True
remove_duplicates(data)
while flag:
    try:
        for link in links:
            for j in soup.find_all('a', href=True):
                temp = []
                page = requests.get(link)
                soup = BeautifulSoup(page.content, 'lxml')
                temp.append(str(j.get('href')))
                remove_duplicates(temp)

                if len(links) > MAX_URL: # set limitation to number of URLs
                    break
            if len(links) > MAX_URL:
                break
        if len(links) > MAX_URL:
            break
    except Exception as e:
        print(e)
        if len(links) > MAX_URL:
            break

PAGES = links

if __name__ == "__main__":
    download(PAGES)
