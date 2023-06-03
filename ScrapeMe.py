import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Global set of visited URLs
visited = set()
processed = set()

# Global list of unique paragraphs
paragraphs = []

def ScrapeMe(base_url, url):

    def gather_links(base_url, url):
        global visited

        # Add the URL to the visited set
        visited.add(url)

        print(f"Gathering links from: {url}")
        
        try:
            # Send a GET request to the URL and store the response
            response = requests.get(url)
        except Exception as e:
            print(f"Failed to get URL: {url} due to exception: {e}")
            return []
        
        # Parse the HTML content of the response using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all the <a> tags in the HTML and extract the href attribute
        links = [urljoin(base_url, link.get("href")) for link in soup.find_all("a") if link.get("href") and urljoin(base_url, link.get("href")).startswith(base_url)]

        # Recursively gather links from each linked site
        for link in links:
            if link not in visited:
                links.extend(gather_links(base_url, link))

        return links


    def process_link(url):
        global paragraphs

        print(f"Processing: {url}")
        
        try:
            # Send a GET request to the URL and store the response
            response = requests.get(url)
        except Exception as e:
            print(f"Failed to get URL: {url} due to exception: {e}")
            return
        
        # Parse the HTML content of the response using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all the <p> tags in the HTML and extract the text content
        for p in soup.find_all("p"):
            text = p.get_text().strip()
            if len(text) >= 5 and text not in paragraphs:
                paragraphs.append(text)
                print(f"Added paragraph: {text}")

    # Define the URL to scrape
    #base_url = input("Provide Base URL to scrape from!: ")
    #https://www.swisslog.com/en-us/case-studies-and-resources/blog/
    #base_url = "https://books.toscrape.com/"

    # Gather all the links
    links = gather_links(base_url, base_url)

    # Process all the links
    for link in links:
            if link not in processed:
                process_link(link)
                processed.add(link)

    # Merge the paragraphs into a single string
    merged_paragraphs = ' '.join(paragraphs)

    # Save the string to a text file
    with open('output.txt', 'w') as f:
        f.write(merged_paragraphs)

    # for paragraph in paragraphs:
    #     print(paragraph)
    