import csv
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_links(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        links = set()
        for anchor in soup.find_all("a", href=True):
            link = anchor["href"]
            full_url = urljoin(url, link)
            links.add(full_url)

        return list(links)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return []


def load_links(webpage_url, csv_filename="links.csv"):
    links = set([link.strip("/") for link in get_links(webpage_url)])
    final_links = []

    inclusion_patterns = ["https://www.gov.uk/"]
    exclusion_patterns = [
        "mailto",
        "terms-conditions",
        "#",
        "/search",
        "/contact",
        "/browse",
        "/cymraeg",
        "/help",
    ]

    with open(csv_filename, "w", newline="") as f:
        link_writer = csv.writer(f)
        for link in links:
            is_included = all(pattern in link for pattern in inclusion_patterns)
            is_excluded = any(pattern in link for pattern in exclusion_patterns)
            if is_included and (not is_excluded):
                link_writer.writerow([link])
                final_links.append(link)
    return final_links


def get_url_content(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        main = soup.find("main")
        full_text = main.get_text()
        clean_text = full_text
        try:
            clean_text = full_text.split("Updates to this page")[0]
        except:
            pass
        lines = clean_text.split(".")
        chunks = []
        chunk_size = 5
        for i in range(0, len(lines), chunk_size):
            try:
                chunk = ". ".join(lines[i : i + chunk_size])
            except:
                chunk = ". ".join(lines[i:])
            chunks.append(chunk)
        clean_chunks = []
        for clean_text in chunks:
            clean_text = clean_text.strip()
            clean_text = clean_text.replace("\n\n", "\n")
            clean_text = clean_text.replace("  ", " ")
            clean_chunks.append(clean_text.strip())
        return clean_chunks
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return "Error"


base_url = "https://www.gov.uk/guidance/funding-for-farmers"
links = load_links(base_url, "funding-for-farmers.csv")

for i, link in enumerate(links):
    print(f"Processing[{i+1}]: {link}")
    chunks = get_url_content(link)
    with open(f"./docs/page_{i+1}.json", "w") as f:
        json.dump({"url": link, "chunks": chunks}, f)
