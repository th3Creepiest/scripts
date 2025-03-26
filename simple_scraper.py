import requests
from bs4 import BeautifulSoup


def get_html(url: str) -> str:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def scrape_html(html_str: str):
    soup = BeautifulSoup(html_str, "html.parser")

    print("Extracting title:")
    print(soup.title.string if soup.title else "No title found")

    print("\nExtracting text:")
    print(soup.get_text(strip=True))

    print("\nExtracting links:")
    for link in soup.find_all("a"):
        print(link.get("href"))  # type: ignore

    print("\nExtracting images:")
    for img in soup.find_all("img"):
        print(f"Image source: {img.get('src')}")  # type: ignore
        print(f"Alt text: {img.get('alt')}")  # type: ignore
        print(f"Class: {img.get('class')}")  # type: ignore
        print(f"Width: {img.get('width')}")  # type: ignore
        print(f"Height: {img.get('height')}")  # type: ignore
        print("-" * 30)


if __name__ == "__main__":
    with open("example.html", "r", encoding="utf-8") as file:
        html = file.read()
        scrape_html(html)
