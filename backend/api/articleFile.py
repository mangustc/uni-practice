from fastapi import APIRouter, UploadFile, File, status, Response, Request
from schemas import *
from services import ArticleService

router = APIRouter(tags=["Article"], prefix="/article")


@router.post("/create_article", response_model=GetArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article(request: Request):
    return await ArticleService.create_article(request)


@router.get("/get_all_articles", response_model=list[GetArticleResponse], status_code=status.HTTP_200_OK)
async def get_all_articles():
    return await ArticleService.get_all_articles()


@router.delete("/delete_article/{article_id}", response_model=Message, status_code=status.HTTP_200_OK)
async def delete_article(request: Request, article_id: int):
    return await ArticleService.delete_article(request, article_id)
