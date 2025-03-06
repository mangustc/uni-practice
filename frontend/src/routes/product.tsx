import { createSearchParams, useNavigate, useSearchParams } from "react-router-dom";
import * as objects from "../objects"
import * as requests from "../requests"
import * as util from "../util"
import { useEffect, useState } from "react";
import { CategoryPath } from "../components/category-path";

function formatNumberLength(num: number, length: number) {
    var r = "" + num;
    while (r.length < length) {
        r = "0" + r;
    }
    return r;
}


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
    requests.GET_GetProductForPage(currentProductID).then((obj) => {
      setProductForPage(obj);
    }) 
  }, [searchParams]);

  const [productAmount, _setProductAmount] = useState(0.1)
  function setProductAmount(newAmount: number): any {
    if (newAmount <= 0)
      return;
    else if (newAmount > productForPage.productAmount)
      return;
    _setProductAmount(+newAmount.toFixed(1));
  }


  const [wishlist, setWishlist] = useState(productForPage.productInWishlist)

  const navigate = useNavigate();
  const currentProductID = getProductSearchParams(searchParams).productID;
  return (
    <>
    <div className="screen-container">
      <div className="center-container" style={{paddingTop: "20px", paddingBottom: "12px"}}>
        <CategoryPath categories={productForPage.categories}/>
      </div>
      <div className="product-page">
        <div className="product-container">
          <div className="product-photos-container">
            <div className="product-photos-column">
              <div className="product-mini-photo-box-active">
                <div
                  className="product-mini-photo"
                  style={{
                    cursor: "pointer",
                    backgroundImage: `url("${requests.BACKEND_URL}/product/get_photo/${currentProductID}")`
                  }}
                ></div>
              </div>
            </div>
            <div className="product-big-photo-container">
              <div 
                className="product-big-photo"
                style={{
                  cursor: "pointer",
                  backgroundImage: `url("${requests.BACKEND_URL}/product/get_photo/${currentProductID}")`
                }}
              ></div>
              <div className="product-info-article" style={{height: "fit-content",  width: "435px", lineHeight: "15px", marginBottom: 0}}>Обращаем ваше внимание, что цвет товара может отличаться по тону, в зависимости от настроек вашего монитора</div>
            </div>
          </div>
          <div className="product-info-container">
            <div className="product-info-article">Артикул <b className="product-info-article-number">{formatNumberLength(productForPage.articleID, 5)}</b> </div>
            <h3 style={{marginBottom: "25px"}}>{productForPage.productName}</h3>
            <div className="product-info-products-article-container" key={JSON.stringify(productForPage.productsByArticle)}>
              {structuredClone(productForPage.productsByArticle)
                .concat({productID: currentProductID, productName: productForPage.productName})
                .sort((a, b) => a.productID - b.productID)
                .map((productInfo) => (
                <img
                  src={`${requests.BACKEND_URL}/product/get_photo/${productInfo.productID}`}
                  key={productInfo.productID + currentProductID}
                  className={productInfo.productID == currentProductID
                      ? "product-info-products-article-product-active"
                      : "product-info-products-article-product"}
                  onClick={(e) => navigate(`/product?productID=${productInfo.productID}`)}
                />
              ))}
            </div>
            <div className="product-info-price-line">
              <div className="product-info-amount-container">
                <div className="product-info-article">Количество, {productForPage.productMeasuredIn}</div>
                <div className="product-info-amount-input-line">
                  <img src="/minus-circle.svg" alt="" onClick={(e) => setProductAmount(productAmount-0.1) } />
                  <div className="product-info-amount-input">{productAmount}</div>
                  <img src="/plus-circle.svg" alt="" onClick={(e) => setProductAmount(productAmount+0.1) } />
                </div>
              </div>
              <div className="product-info-price-container">
              <div className="product-info-article">Цена, {productForPage.productMeasuredIn}</div>
              <h3>{productForPage.productPrice} ₽</h3>
              </div>
              { productForPage.productPromotion ?
              <div className="product-info-sale-container">
                <div className="product-info-sale-full-price">{productForPage.productNewPrice} ₽</div>
                <div className="product-info-sale-discount">-${productForPage.productPercentPromotion}%</div>
              </div> : null}
            </div>
            <div className="product-info-btns-line">
              <button className="product-add-btn"
                onClick={(e) => {
                  requests.POST_AddInCart(currentProductID, productAmount);
                  util.NewNotification.success("Товар успешно добавлен в корзину", `Товар ${productForPage.productName} в количестве ${productAmount}`);
                }}
              >В корзину</button>
              <button className={wishlist ? "product-like-active" : "product-like"}
                onClick={() => {
                  requests.PUT_ChangeWishlistState(currentProductID);
                  setWishlist(!wishlist);
                }}
              ></button>
            </div>
            <div className="product-info-article" style={{marginBottom: "27px"}}>В наличии:  <b className="product-info-article-number">{productForPage.productAmount} {productForPage.productMeasuredIn}</b> </div>
            <div className="product-info-inner">
              <button className="product-info-inner-delivery">Рассчитать доставку
                <img src="/car.svg" alt="" style={{marginLeft: "10px"}}/>
              </button>
              <div className="product-info-inner-share-line">Поделиться: 
                <div className="product-info-inner-share-icon info-vk"/>
                <div className="product-info-inner-share-icon info-wa"/>
                <div className="product-info-inner-share-icon info-tg"/>
                <div className="product-info-inner-share-icon info-ok"/>
              </div>
            </div>
            {/* <textarea value={JSON.stringify(productForPage, null, 2)} readOnly/> */}
          </div>
        </div>
        <div className="product-chars">
          <h4 style={{marginBottom: "16px"}}>Характеристики</h4>
          <div className="product-char-line">
            <p style={{color: "var(--text-color-black-main-70)"}}>Артикул</p>
            <div className="product-char-line-dots"></div>
            <p style={{color: "var(--text-color-black-main)"}}>2356256</p>
          </div>
          
        </div>
      </div>
    </div>
    <div></div>
    </>
  )
}
