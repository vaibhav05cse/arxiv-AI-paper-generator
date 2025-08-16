import feedparser
import urllib.parse
import requests
from datetime import datetime, timedelta

# Take input from user
search_query = input("Enter keyword to search arXiv: ")
encoded_query = urllib.parse.quote(search_query)

# API URL
base_url = "https://export.arxiv.org/api/query?"
query = f"search_query=all:{encoded_query}&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending"
url = base_url + query
print(f"Request URL: {url}")

# Fetch with requests
response = requests.get(url, timeout=10)
print(f"HTTP status: {response.status_code}, response size: {len(response.text)}")

# Parse with feedparser
feed = feedparser.parse(response.text)
print(f"Total entries fetched: {len(feed.entries)}")

# Time filter: last 10 days
cutoff_date = datetime.utcnow() - timedelta(days=10)
print("Cutoff date (UTC):", cutoff_date)

results = []
for entry in feed.entries:
    published = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%SZ")
    if published >= cutoff_date:
        authors = ", ".join(author.name for author in entry.authors)
        abstract = ' '.join(entry.summary.strip().split()[:50]) + '...'

        pdf_url = ""
        for link in entry.links:
            if link.type == "application/pdf":
                pdf_url = link.href
                break

        results.append({
            "title": entry.title.strip().replace('\n', ' '),
            "authors": authors,
            "abstract": abstract,
            "published": published.date().isoformat(),
            "abstract_url": entry.link,
            "pdf_url": pdf_url
        })

    if len(results) == 10:
        break

# Display results
if not results:
    print("\nNo recent papers found for this keyword in the last 10 days.")
else:
    for i, paper in enumerate(results, 1):
        print(f"\n{i}. {paper['title']}")
        print(f"   Authors: {paper['authors']}")
        print(f"   Published: {paper['published']}")
        print(f"   Abstract: {paper['abstract']}")
        print(f"   Abstract Link: {paper['abstract_url']}")
        print(f"   PDF Link: {paper['pdf_url']}")