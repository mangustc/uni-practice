from fastapi import APIRouter, UploadFile, File, status, Response, Request, Query
from schemas import *
from services import ProductService

router = APIRouter(tags=["Product"], prefix="/product")


@router.post("/CreateProduct")
async def create_product(request: Request, data: CreateProduct):
    return await ProductService.create_product(request, data)


@router.get("/{product_id}/GetProduct")
async def get_product(product_id: int):
    return await ProductService.get_product(product_id)


@router.get("/{product_id}/GetProductSmallCard")
async def get_product_small_card(product_id: int):
    return await ProductService.get_product_small_card(product_id)


@router.get("/GetAllProducts")
async def get_all_products():
    return await ProductService.get_all_products()


@router.get("/{product_id}/GetPhoto")
async def get_product_photo(product_id):
    return await ProductService.get_product_photo(product_id)


@router.put("/{product_id}/UpdatePhoto")
async def update_product_photo(request: Request, product_id: int, file: UploadFile = File(...)):
    return await ProductService.update_product_photo(request, product_id, file)


@router.put("/{product_id}/Update")
async def update_product_information(request: Request, product_id: int, data: CreateProduct):
    return await ProductService.update_product_information(request, product_id, data)


@router.delete("/{product_id}/Delete")
async def delete_product(request: Request, product_id: int):
    return await ProductService.delete_product(request, product_id)


@router.put("/{product_id}/ChangeWishlistState")
async def change_wishlist_state(request: Request, product_id: int):
    return await ProductService.change_wishlist_state(request, product_id)


@router.put("/{product_id}/{amount}/AddInCart")
async def add_in_cart(request: Request, product_id: int, amount: float):
    return await ProductService.add_in_cart(request, product_id, amount)


@router.put("/{product_id}/{amount}/ChangeAmountInCart")
async def change_product_amount_in_cart(request: Request, product_id: int, amount: int):
    return await ProductService.change_product_amount_in_cart(request, product_id, amount)


@router.put("/{product_id}/DeleteFromCart")
async def delete_from_cart(request: Request, product_id: int):
    return await ProductService.delete_from_cart(request, product_id)


@router.put("/products/{product_id}/new")
async def set_product_new_endpoint(
    request: Request, product_id: int, is_new: bool = Query(..., description="Set product as new (true/false)")
):
    return await ProductService.set_product_new(request, product_id, is_new)


@router.put("/products/{product_id}/hit")
async def set_product_hit_endpoint(
    request: Request, product_id: int, is_hit: bool = Query(..., description="Set product as hit (true/false)")
):
    return await ProductService.set_product_hit(request, product_id, is_hit)


@router.put("/products/{product_id}/promotion")
async def set_product_promotion_endpoint(
    request: Request,
    product_id: int,
    is_promotion: bool = Query(..., description="Set product as promotion (true/false)"),
    procent_promotion: Optional[float] = Query(
        None, description="Promotion percentage (1-100), required if is_promotion=true"
    ),
):
    return await ProductService.set_product_promotion(request, product_id, is_promotion, procent_promotion)


@router.get("/products/new", response_model=list[dict])
async def get_new_products_endpoint():
    return await ProductService.get_new_products()


@router.get("/products/promotion", response_model=list[dict])
async def get_promotion_products_endpoint():
    return await ProductService.get_promotion_products()


@router.get("/products/hit", response_model=list[dict])
async def get_hit_products_endpoint():
    return await ProductService.get_hit_products()
