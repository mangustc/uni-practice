from fastapi import APIRouter, UploadFile, File, status, Response, Request, Query
from schemas import *
from services import ProductService

router = APIRouter(tags=["Product"], prefix="/product")


@router.post("/create_product", response_model=GetProductResponse, status_code=status.HTTP_200_OK)
async def create_product(request: Request, data: CreateProduct):
    return await ProductService.create_product(request, data)


@router.get("/get_product/{product_id}", response_model=GetProductResponseWithNames, status_code=status.HTTP_200_OK)
async def get_product(product_id: int):
    return await ProductService.get_product(product_id)


@router.get("/get_product_for_page/{product_id}", response_model=GetProductForPageResponse,
            status_code=status.HTTP_200_OK)
async def get_product_for_page(product_id: int, request: Request):
    return await ProductService.get_product_for_page(product_id, request)


@router.get("/get_all_products", response_model=list[GetProductResponseWithNames], status_code=status.HTTP_200_OK)
async def get_all_products():
    return await ProductService.get_all_products()


@router.get("/get_products_by_category_name/{category_id}", response_model=list[GetProductResponseWithNames],
            status_code=status.HTTP_200_OK)
async def get_products_by_category_id(category_id: int):
    """
    Возвращает продукты указанной категории и дочерних категорий.
    """
    return await ProductService.get_products_by_category_id(category_id)


@router.get("/get_photo/{product_id}", status_code=status.HTTP_200_OK)
async def get_product_photo(product_id):
    return await ProductService.get_product_photo(product_id)


@router.put("/update_photo/{product_id}", status_code=status.HTTP_200_OK)
async def update_product_photo(request: Request, product_id: int, file: UploadFile = File(...)):
    return await ProductService.update_product_photo(request, product_id, file)


@router.put("/update/{product_id}", response_model=GetProductResponse, status_code=status.HTTP_200_OK)
async def update_product_information(request: Request, product_id: int, data: UpdateProduct):
    """
    Все поля, кроме **set_description_null** и **set_color_null** являются необязательными.
    """
    return await ProductService.update_product_information(request, product_id, data)


@router.post("/add_characteristic/{product_id}", response_model=AddCharacteristicResponse,
             status_code=status.HTTP_201_CREATED)
async def add_characteristic(request: Request, product_id: int, data: AddCharacteristic):
    return await ProductService.add_characteristic(request, product_id, data)


@router.get("/get_characteristics_by_product_id/{product_id}", response_model=list[GetCharacteristicResponse],
            status_code=status.HTTP_200_OK)
async def get_characteristics_by_product_id(product_id: int):
    return await ProductService.get_characteristics_by_product_id(product_id)


@router.put("/update_characteristic/{product_id}", response_model=AddCharacteristicResponse,
            status_code=status.HTTP_200_OK)
async def update_characteristic(request: Request, product_id: int, data: AddCharacteristic):
    return await ProductService.update_characteristic(request, product_id, data)


@router.delete("/delete_characteristic_by_property_name/{product_id}", response_model=Message,
               status_code=status.HTTP_200_OK)
async def delete_characteristic_by_property_name(request: Request, product_id: int, property_name: str):
    return await ProductService.delete_characteristic_by_property_name(request, product_id, property_name)


@router.delete("/delete_product/{product_id}", response_model=Message, status_code=status.HTTP_200_OK)
async def delete_product(request: Request, product_id: int):
    return await ProductService.delete_product(request, product_id)


@router.put("/change_wishlist_state/{product_id}", response_model=WishlistUpdateResponse, status_code=status.HTTP_200_OK)
async def change_wishlist_state(request: Request, product_id: int):
    return await ProductService.change_wishlist_state(request, product_id)


@router.put("/products/new/{product_id}", response_model=Message, status_code=status.HTTP_200_OK)
async def set_product_new_endpoint(
    request: Request, product_id: int, is_new: bool = Query(..., description="Set product as new (true/false)")
):
    return await ProductService.set_product_new(request, product_id, is_new)


# @router.post("/orders", response_model=PlaceOrderResponse, status_code=status.HTTP_201_CREATED)
# async def create_order(request: Request):
#     return await ProductService.place_order(request=request)


# @router.put("/products/{product_id}/hit")
# async def set_product_hit_endpoint(
#     request: Request, product_id: int, is_hit: bool = Query(..., description="Set product as hit (true/false)")
# ):
#     return await ProductService.set_product_hit(request, product_id, is_hit)

@router.put("/products/promotion/{product_id}", response_model=Message, status_code=status.HTTP_200_OK)
async def set_product_promotion_endpoint(
    request: Request,
    product_id: int,
    is_promotion: bool = Query(..., description="Set product as promotion (true/false)"),
    percent_promotion: Optional[float] = Query(
        None, description="Promotion percentage (1-100), required if is_promotion=true"
    ),
):
    return await ProductService.set_product_promotion(request, product_id, is_promotion, percent_promotion)


@router.get("/products/new", response_model=list[dict])
async def get_new_products_endpoint():
    return await ProductService.get_new_products()


@router.get("/products/promotion", response_model=list[dict])
async def get_promotion_products_endpoint():
    return await ProductService.get_promotion_products()


@router.get("/products/hit", response_model=list[dict])
async def get_hit_products_endpoint():
    return await ProductService.get_hit_products()
