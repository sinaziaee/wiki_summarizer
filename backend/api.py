from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from scraper import scrape
from summarizer import load_chat_model_and_template, summarize

app = FastAPI()

class SummarizeRequest(BaseModel):
    query: str

class SummarizeResponse(BaseModel):
    query: str
    summary: str
    source_url: str

chat, prompt = load_chat_model_and_template()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/summarize", response_model=SummarizeResponse)
def summarize_endpoint(payload: SummarizeRequest):
    try:
        page, source_url = scrape(payload.query)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    title   = page["title"]
    content = page["content"]
    # summarize
    try:
        summary = summarize(chat, prompt, content)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Summarization failed: {e}")

    return SummarizeResponse(
        query=payload.query,
        summary=summary,
        source_url=source_url
    )