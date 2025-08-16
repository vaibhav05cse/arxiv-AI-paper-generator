from flask import Flask, render_template, request
import feedparser
import urllib.parse
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

def fetch_arxiv_papers(keyword):
    encoded_query = urllib.parse.quote(keyword)
    base_url = "https://export.arxiv.org/api/query?"
    query = f"search_query=all:{encoded_query}&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending"
    url = base_url + query

    response = requests.get(url, timeout=10)
    feed = feedparser.parse(response.text)

    cutoff_date = datetime.utcnow() - timedelta(days=10)
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
    return results

@app.route("/", methods=["GET", "POST"])
def index():
    papers = []
    keyword = ""
    if request.method == "POST":
        keyword = request.form.get("keyword")
        if keyword:
            papers = fetch_arxiv_papers(keyword)
    return render_template("index.html", papers=papers, keyword=keyword)

if __name__ == "__main__":
    app.run(debug=True)
