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
          <textarea value={JSON.stringify(productForPage, null, 2)} readOnly/>
        </div>
      </div>
    </div>
    <div></div>
    </>
  )
}
