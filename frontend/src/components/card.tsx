import { useState } from "react";
import * as objects from "../objects.tsx";
import * as requests from "../requests.tsx";
import * as util from "../util.tsx";


export default function Card({productCatalog, photoSrc}: {
    productCatalog: objects.ProductCatalog;
    photoSrc: string;
}) {
    const [wishlist, setWishlist] = useState(productCatalog.productInWishlist)
    return (
        <div className="card-container">
            <div className="card-photo" style={{backgroundImage: `url("${photoSrc}")`}}>
                <div>
                    {productCatalog.productHit ? <div className="card-filter">Хит</div> : null}
                    {productCatalog.productNew ? <div className="card-filter">Новинка</div> : null}
                    {productCatalog.productPromotion ? <div className="card-filter">Акция</div> : null}
                </div>
                <div 
                    className={wishlist ? "card-like-wishlist" : "card-like"} 
                    onClick={() => {
                        requests.PUT_ChangeWishlistState(productCatalog.productID)
                        setWishlist(!wishlist);
                    }}
                ></div>
            </div>
            <span className="card-name">{productCatalog.productName}</span>
            <span className="card-descr">Цена, {productCatalog.productMeasuredIn}</span>
            <span className="card-cost">{productCatalog.productPrice} ₽</span>
            <button className="card-add-btn" onClick={() => {
                util.NewNotification.success("Товар успешно добавлен в корзину", `Товар ${productCatalog.productName} в количестве 1`);
                requests.POST_AddInCart(productCatalog.productID, 1);
            }}>В корзину</button>
        </div>
    );
}
