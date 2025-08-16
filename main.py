# main.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import arxiv_papers  # your existing backend logic

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "papers": [], "keyword": ""})

@app.post("/", response_class=HTMLResponse)
def submit_form(request: Request, keyword: str = Form(...)):
    papers = arxiv_papers.fetch_arxiv_papers(keyword)
    return templates.TemplateResponse("index.html", {"request": request, "papers": papers, "keyword": keyword})