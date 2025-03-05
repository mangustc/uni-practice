import { createSearchParams, useSearchParams } from "react-router-dom";
import * as objects from "../objects"
import * as requests from "../requests"
import { useEffect, useState } from "react";
import { CategoryPath } from "../components/category-path";

function newProductSearchParams(obj: {
  productID: number,
}): URLSearchParams {
  return createSearchParams({
    productID: String(obj.productID)
  });
}

function getProductSearchParams(searchParams: URLSearchParams) {
  return {
    productID: searchParams.get("productID") ? Number(searchParams.get("productID")) : objects.DEFAULT_NUMBER,
  }
}

export function Product({}: {}) {
  const [searchParams, setSearchParams] = useSearchParams();
  const [productForPage, setProductForPage] = useState<objects.ProductForPage>(objects.NewProductForPage({}));
  useEffect(() => {
    requests.GET_GetProductForPage(getProductSearchParams(searchParams).productID).then((obj) => {
      setProductForPage(obj);
    }) 
  }, [searchParams]);

  return (
    <>
    <div className="screen-container">
      <div className="center-container" style={{paddingTop: "20px", paddingBottom: "12px"}}>
        <CategoryPath categories={productForPage.categories}/>
      </div>
      <div className="product-container">
        <div className="product-photos-container">
          <div className="product-photos-column">
            <div className="product-mini-photo-box-active">
              <div
                className="product-mini-photo"
                style={{
                  cursor: "pointer",
                  backgroundImage: `url("${requests.BACKEND_URL}/product/get_photo/${getProductSearchParams(searchParams).productID}")`
                }}
              ></div>
            </div>
          </div>
          <div 
            className="product-big-photo"
            style={{
              cursor: "pointer",
              backgroundImage: `url("${requests.BACKEND_URL}/product/get_photo/${getProductSearchParams(searchParams).productID}")`
            }}
          ></div>
        </div>
        <div className="product-info-container">
          <div className="product-info-article">Артикул <b className="product-info-article-number">361365</b> </div>
          <h3>Название продукта</h3>
          <div className="product-info-price-line">
            <div className="product-info-amount-container">
              <div className="product-info-article">Количество, м</div>
              <div className="product-info-amount-input-line">
                <img src="/minus-circle.svg" alt="" />
                <div className="product-info-amount-input">0.1</div>
                <img src="/plus-circle.svg" alt="" />
              </div>
            </div>
            <div className="product-info-price-container">
            <div className="product-info-article">Цена, м</div>
            <h3>719.20 ₽</h3>
            </div>
            <div className="product-info-sale-container">
              <div className="product-info-sale-full-price">899 ₽</div>
              <div className="product-info-sale-discount">-20%</div>
            </div>
          </div>
          {/* <textarea value={JSON.stringify(productForPage, null, 2)} readOnly/> */}
        </div>
      </div>
    </div>
    <div></div>
    </>
  )
}
