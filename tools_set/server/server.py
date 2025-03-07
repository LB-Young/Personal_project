# -*- coding: utf-8 -*-
from fastapi import FastAPI, Body, HTTPException
from typing import List, Optional, Union, Dict
import uvicorn
from pydantic import BaseModel
from paper_with_code_full import paper_with_code_search_full
from send_email import send_email
from list_to_multiline_string import list_to_multiline_string
from web_content import web_content_extractor

def clean_text(text):
    """清理文本，确保所有字符都是有效的UTF-8字符"""
    if isinstance(text, str):
        return text.encode('utf-8', errors='ignore').decode('utf-8')
    return text

def clean_paper_data(paper):
    """清理论文数据中的所有文本字段"""
    cleaned = {}
    for key, value in paper.items():
        if isinstance(value, str):
            cleaned[key] = clean_text(value)
        elif isinstance(value, list):
            cleaned[key] = [clean_text(item) if isinstance(item, str) else item for item in value]
        else:
            cleaned[key] = value
    return cleaned

app = FastAPI(
    title="Paper With Code API",
    description="论文搜索服务API",
    version="1.0.0"
)

class PaperInfo(BaseModel):
    title: str
    url: str
    team: str
    abstract: str
    published_date: str
    stars: int
    authors: List[str]
    content: str

class PaperRequest(BaseModel):
    nums: int

class EmailInfo(BaseModel):
    subject: str
    content: str
    to: List[str]

class List2Str(BaseModel):
    list_content: List[str]

class WebContentRequest(BaseModel):
    urls: List[str]

class ResponseModel(BaseModel):
    answer: Dict[str, Union[List[PaperInfo], str, Dict[str, str]]]

@app.post("/papers/list", response_model=ResponseModel)
async def get_papers(request: PaperRequest):
    try:
        papers = await paper_with_code_search_full(nums=request.nums)
        # 清理每篇论文的数据
        cleaned_papers = [clean_paper_data(paper) for paper in papers]
        return {"answer": {"answer": [PaperInfo(**paper) for paper in cleaned_papers]}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send_email", response_model=ResponseModel)
async def send_email_endpoint(request: EmailInfo):
    try:
        result = await send_email(content=request.content, subject=request.subject, to=request.to)
        return {"answer": {"answer": result}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/list_to_multiline_string", response_model=ResponseModel)
async def list_to_multiline_string_endpoint(request: List2Str):
    try:
        result = await list_to_multiline_string(request.list_content)
        return {"answer": {"answer": result}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/web_content", response_model=ResponseModel)
async def web_content_endpoint(request: WebContentRequest):
    try:
        result = await web_content_extractor(urls=request.urls)
        return {"answer": {"answer": result}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3389)