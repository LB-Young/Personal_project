from fastapi import FastAPI, Query
from typing import List, Optional
import uvicorn
from pydantic import BaseModel
from paper_with_code_full import paper_with_code_search_full

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

class PaperInfoList(BaseModel):
    res: List[PaperInfo]

@app.get("/papers/list", response_model=PaperInfoList)
async def get_papers(
    page: str = Query(..., description="页码"),
    size: str = Query(..., description="每页数量")
):
    try:
        page_num = int(page)
        size_num = int(size)
        papers = await paper_with_code_search_full(nums=size_num)
        return PaperInfoList(res=papers)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8221)