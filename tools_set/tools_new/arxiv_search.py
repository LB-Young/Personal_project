import arxiv
import PyPDF2
import requests


class ArxivSearch:
  name = "arxiv_search"
  description = "搜索arxiv上相关主题的论文"
  inputs = {
    "keyword": {
      "type": "string",
      "description": "搜索的关键词"
    },
    "nums": {
      "type": "int",
      "description": "搜索的论文数量，最多20篇"
    }
  }
  outputs = {
    "papers": {
      "type": "list",
      "description": "搜索到的论文列表"
    }
  }
  props = {}

  async def run(keyword="", nums=1, params_format=False):
    if params_format:
      return ['keyword', 'nums']
    client = arxiv.Client()
    if nums > 20:
      nums = 20
    search = arxiv.Search(
      query = keyword,
      max_results = nums,
      sort_by = arxiv.SortCriterion.SubmittedDate
    )
    papers = []
    for r in client.results(search):
      try:
        down_load_path = r.download_pdf("F:/logs/orca/download_pdf/")
        pdf_text = await read_pdf(down_load_path)
        papers.append(
          {
            "title": r.title,
            "authors": r.authors,
            "published": r.published,
            "summary": r.summary,
            "pdf_text": pdf_text,
            "down_load_path": down_load_path
          }
        )
      except Exception as e:
        print(e)
        papers.append(
          {
            "title": r.title,
            "authors": r.authors,
            "published": r.published,
            "summary": r.summary,
            "pdf_text": r.summary,
            "down_load_path": down_load_path
          }
        )
    return papers


async def read_pdf(path):
  with open(path, "rb") as f:
    pdf_reader = PyPDF2.PdfReader(f)
    text = ""
    for page in pdf_reader.pages:
      text += page.extract_text()
    if len(text) > 50000:
      return text[:50000]
    else:
      return text

