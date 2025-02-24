import * as objects from "../objects.tsx";
import * as requests from "../requests.tsx";

export default function Card({productCatalog, photoSrc}: {
    productCatalog: objects.ProductCatalog;
    photoSrc: string;

}) {
    return (
        <div className="card-container">
            <div className="card-photo">
                <div>
                    {productCatalog.productHit ? <div className="card-filter">Хит</div> : null}
                    {productCatalog.productNew ? <div className="card-filter">Новинка</div> : null}
                    {productCatalog.productPromotion ? <div className="card-filter">Акция</div> : null}
                </div>
                <div className="card-like"></div>

            </div>
            <span className="card-name">{productCatalog.productName}</span>
            <span className="card-descr">Цена, {productCatalog.productMeasuredIn}</span>
            <span className="card-cost">{productCatalog.productPrice} ₽</span>
            <button className="card-add-btn" onClick={() => requests.POST_AddInCart(productCatalog.productID, 1)}>В корзину</button>
        </div>
    );
}
