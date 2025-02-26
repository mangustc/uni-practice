import { useNavigate } from "react-router-dom";

export function CartEmpty() {
    const navigate = useNavigate();
    return (
        <div className="cart-empty-container">
            <div className="cart-empty-navigation">
                <h3>Ваша корзина пуста</h3>
                <p>Выберите нужный Вам товар из каталога интернет-магазина и добавьте его в корзину</p>
                <section style={{ display: "flex", gap: "20px" }}>
                    <div onClick={() => navigate("/catalog?currentCategoryID=1")} className="categories-panel-category" id="fabrics" style={{ width: "100%" }}>
                        <h6>Ткани</h6>
                    </div>
                    <div onClick={() => navigate("/catalog?currentCategoryID=2")} className="categories-panel-category" id="for-art" style={{ width: "100%" }}>
                        <h6>Для творчества</h6>
                    </div>
                </section>
                <section style={{ display: "flex", gap: "20px" }}>
                    <div onClick={() => navigate("/catalog?currentCategoryID=3")} className="categories-panel-category" id="for-interior" style={{ width: "100%" }}>
                        <h6>Для интерьера</h6>
                    </div>
                    <div onClick={() => navigate("/catalog?currentCategoryID=4")} className="categories-panel-category" id="accessories" style={{ width: "100%" }}>
                        <h6>Фурнитура</h6>
                    </div>
                </section>
            </div>

            <img className="cart-empty-image" src="/cart-empty.svg" alt="" />
        </div>
    )
}