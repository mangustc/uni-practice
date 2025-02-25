from fastapi import APIRouter, UploadFile, File, Request
from schemas import ShopCreate, ShopUpdate, ShopResponse
from services import ShopService

router = APIRouter(prefix="/shops", tags=["Shops"])

@router.post("/", response_model=ShopResponse)
async def create_shop(request: Request, shop: ShopCreate):
    return await ShopService.create_shop(request, shop)

@router.get("/", response_model=list[ShopResponse])
async def get_shops():
    return await ShopService.get_shops()

@router.get("/{shop_id}", response_model=ShopResponse)
async def get_shop(shop_id: int):
    return await ShopService.get_shop(shop_id)

@router.put("/{shop_id}", response_model=ShopResponse)
async def update_shop(request: Request, shop_id: int, shop_update: ShopUpdate):
    return await ShopService.update_shop(request, shop_id, shop_update)

@router.delete("/{shop_id}")
async def delete_shop(request: Request, shop_id: int):
    return await ShopService.delete_shop(request, shop_id)

@router.get("/{shop_id}/photo")
async def get_shop_photo(shop_id: int):
    return await ShopService.get_shop_photo(shop_id)

@router.post("/{shop_id}/photo")
async def upload_shop_photo(request: Request, shop_id: int, file: UploadFile = File(...)):
    return await ShopService.update_shop_photo(request, shop_id, file)


@router.delete("/{shop_id}/photo")
async def delete_shop_photo(request: Request, shop_id: int):
    return await ShopService.delete_shop_photo(request, shop_id)
