from fastapi import APIRouter, UploadFile, File, status, Response, Request
from schemas import *
from services import ArticleService

router = APIRouter(tags=["Article"], prefix="/article")


@router.post("/CreateArticle")
async def create_article(request: Request, data: CreateArticle):
    return await ArticleService.create_article(request, data)


@router.get("/{article_id}/GetArticle")
async def get_article(article_id: int):
    return await ArticleService.get_article(article_id)


@router.get("/GetAllArticles")
async def get_all_articles():
    return await ArticleService.get_all_articles()


@router.put("/{article_id}/Update")
async def update_article_information(request: Request, article_id: int, data: CreateArticle):
    return await ArticleService.update_article_information(request, article_id, data)


@router.patch("/{article_id}/characteristics", response_model=ArticleResponse)
async def update_article_characteristics_endpoint(request: Request, article_id: int, data: UpdateArticleCharacteristics):
    return await ArticleService.update_article_characteristics(request, article_id, data)


@router.delete("/{article_id}/Delete")
async def delete_article(request: Request, article_id: int):
    return await ArticleService.delete_article(request, article_id)
