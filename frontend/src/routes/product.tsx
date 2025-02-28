import { createSearchParams, useSearchParams } from "react-router-dom";
import * as objects from "../objects"
import * as requests from "../requests"
import { useEffect, useState } from "react";

function newCatalogSearchParams(obj: {
  productID: number,
}): URLSearchParams {
  return createSearchParams({
    productID: String(obj.productID)
  });
}

function getCatalogSearchParams(searchParams: URLSearchParams) {
  return {
    productID: searchParams.get("productID") ? Number(searchParams.get("productID")) : objects.DEFAULT_NUMBER,
  }
}

export function Product({}: {}) {
  const [searchParams, setSearchParams] = useSearchParams();
  const [productForPage, setProductForPage] = useState<objects.ProductForPage>(objects.NewProductForPage({}));
  useEffect(() => {
    requests.GET_GetProductForPage(getCatalogSearchParams(searchParams).productID).then((obj) => {
      setProductForPage(obj);
    }) 
  }, [searchParams]);

  return (
    <>
      <textarea value={JSON.stringify(productForPage, null, 2)} readOnly/>
      <div></div>
    </>
  )
}
