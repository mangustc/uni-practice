import { useState } from "react";
import * as objects from "../objects.tsx";
import * as requests from "../requests.tsx";
import * as util from "../util.tsx";
import { useNavigate } from "react-router-dom";


export default function Card({productCatalog, photoSrc, refreshOnAdd = false, onAddListener}: {
    productCatalog: objects.ProductCatalog;
    photoSrc: string;
    refreshOnAdd?: boolean;
    onAddListener?: () => void;
}) {
    const navigate = useNavigate();
    const [wishlist, setWishlist] = useState(productCatalog.productInWishlist)

    function navigateProductPage(productID: number) {
        navigate(`/product?productID=${productID}`)
    }
    return (
        <div className="card-container">
            <div onClick={() => navigateProductPage(productCatalog.productID)}
                className="card-photo" style={{cursor: "pointer", backgroundImage: `url("${photoSrc}")`}}>
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
            <span className="card-name text-link" onClick={() => navigateProductPage(productCatalog.productID)}>{productCatalog.productName}</span>
            <span className="card-descr">Цена, {productCatalog.productMeasuredIn}</span>
            <span className="card-cost">{productCatalog.productPrice} ₽</span>
            <button className="card-add-btn" onClick={() => {
                requests.POST_AddInCart(productCatalog.productID, 1).then(() => {
                    util.NewNotification.success("Товар успешно добавлен в корзину", `Товар ${productCatalog.productName} в количестве 1`);
                    if (refreshOnAdd) {
                        window.location.reload();
                    }
                    if (onAddListener) {
                        onAddListener();
                    }
                });
            }}>В корзину</button>
        </div>
    );
}
