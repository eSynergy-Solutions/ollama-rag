import requests
import bs4

visited = set()

def recursiveURLSearch(url, depth):
    if url in visited:
        return []
    visited.add(url)
    if depth == 0:
        return []
    else:
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        urls = [a["href"] for a in soup.find_all("a", href=True) if "www.gov.uk" in a["href"] and "pet" in a["href"]]
        result = []
        print("currentDepth", depth)
        for new_url in urls:
            result.extend(recursiveURLSearch(new_url, depth-1))
        return urls + result
    
final_list = recursiveURLSearch("https://www.gov.uk/bring-pet-to-great-britain", 2)
print(len(final_list))
print(len(set(final_list)))
print(len(visited))
print(visited)