from fastapi import APIRouter, UploadFile, File, status, Response, Request
from schemas import *
from services import ArticleService

router = APIRouter(tags=["Article"], prefix="/article")


@router.post("/CreateArticle", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article(request: Request, data: CreateArticle):
    return await ArticleService.create_article(request, data)


@router.post("/AddCharacteristic/{article_id}", response_model=AddCharacteristicResponse,
             status_code=status.HTTP_201_CREATED)
async def add_characteristic(request: Request, article_id: int, data: AddCharacteristic):
    return await ArticleService.add_characteristic(request, article_id, data)


@router.get("/GetCharacteristicsByArticleId/{article_id}", response_model=list[GetCharacteristicResponse],
            status_code=status.HTTP_200_OK)
async def get_characteristics_by_article_id(article_id: int):
    return await ArticleService.get_characteristics_by_article_id(article_id)


@router.put("/UpdateCharacteristic/{article_id}", response_model=GetCharacteristicResponse,
            status_code=status.HTTP_200_OK)
async def update_characteristic(request: Request, article_id: int, data: AddCharacteristic):
    return await ArticleService.update_characteristic(request, article_id, data)


@router.delete("/DeleteCharacteristicByPropertyName/{article_id}", response_model=Message,
               status_code=status.HTTP_200_OK)
async def delete_characteristic_by_property_name(request: Request, article_id: int, property_name: str):
    return await ArticleService.delete_characteristic_by_property_name(request, article_id, property_name)


@router.get("/{article_id}/GetArticle", response_model=GetArticleResponse, status_code=status.HTTP_200_OK)
async def get_article(article_id: int):
    return await ArticleService.get_article(article_id)


@router.get("/GetAllArticles", response_model=list[GetArticleResponse], status_code=status.HTTP_200_OK)
async def get_all_articles():
    return await ArticleService.get_all_articles()


@router.put("/{article_id}/Update", response_model=ArticleResponse, status_code=status.HTTP_200_OK)
async def update_article_information(request: Request, article_id: int, data: CreateArticle):
    return await ArticleService.update_article_information(request, article_id, data)


@router.patch("/{article_id}/characteristics", response_model=ArticleResponse, status_code=status.HTTP_200_OK)
async def update_article_characteristics_endpoint(request: Request, article_id: int, data: UpdateArticleCharacteristics):
    return await ArticleService.update_article_characteristics(request, article_id, data)


@router.delete("/{article_id}/Delete", response_model=Message, status_code=status.HTTP_200_OK)
async def delete_article(request: Request, article_id: int):
    return await ArticleService.delete_article(request, article_id)
