import { useState, useEffect } from "react";
import CategoriesPanel from "../components/categories-panel";
import { useNavigate } from 'react-router-dom';
import { ProductList } from "../components/product-list";
import * as objects from "../objects";
import * as requests from "../requests";

export default function Main() {
    const navigate = useNavigate();
    const [popularProducts, setPopularProducts] = useState<objects.ProductCatalog[]>([]);
    const [newProducts, setNewProducts] = useState<objects.ProductCatalog[]>([]);

    useEffect(() => {
        requests.GET_GetProducts().then((prod) => { // для тестов
          setPopularProducts([...prod, ...prod, ...prod]);
          setNewProducts([...prod, ...prod, ...prod]);
        })
      }, []);

    return (
        <div className="main-container">
            <CategoriesPanel></CategoriesPanel>
            <div className="main-image" onClick={() => {navigate("/catalog?currentCategoryID=1")}}>
                <button className="main-image-button">Выбрать</button>
            </div>
            <ProductList title="Популярные товары" products={popularProducts}/>
            <ProductList title="Новинки" products={newProducts}/>
            <div>
                <section className="main-text-container"><h1 className="main-name">Белая роза</h1><h1>&nbsp;— крупный магазин&nbsp;</h1><h1>тканей</h1><h1>,&nbsp;</h1><h1>аксессуаров</h1><h1>,</h1></section>
                <section className="main-text-container"><h1>фурнитуры</h1><h1>&nbsp;высокого качества и товаров для&nbsp;</h1><h1>вышивки</h1><h1>&nbsp;и</h1></section>
                <section className="main-text-container"><h1>вязания</h1><h1>&nbsp;в Томске</h1></section>
            </div>
            <p style={{ maxWidth: "700px" }}>Все необходимое для работы и творчества у нас найдут как представители больших ателье,
                текстильных бутиков, так и частные лица, дизайнеры-оформители и люди, занимающиеся
                шитьем в свое удовольствие.</p>
            <div className="main-advantages">
                <h5 className="main-text-grey">Заглянув в «Белую розу» один раз, многие покупатели становятся постоянными клиентами, благодаря:</h5>
                <div className="main-advantages-list">
                    <div className="main-advantages-elem">
                        <h4 className="main-advantages-num">1</h4>
                        <p style={{ maxWidth: "196px" }}>разнообразию материи, швейной фурнитуры</p>
                        <div className="main-first-line"></div>
                    </div>
                    <div className="main-advantages-elem">
                        <div className="main-second-line"></div>
                        <h4 className="main-advantages-num">2</h4>
                        <p style={{ maxWidth: "196px" }}>высокому качеству тканей, яркому дизайну</p>
                    </div>
                    <div className="main-advantages-elem">
                        <h4 className="main-advantages-num">3</h4>
                        <p style={{ maxWidth: "196px" }}>регулярному обновлению товара</p>
                        <div className="main-third-line"></div>
                    </div>
                    <div className="main-advantages-elem" style={{ alignSelf: "end"}}>
                        <h4 className="main-advantages-num">4</h4>
                        <p style={{ maxWidth: "196px" }}>широкому ассортименту товаров для рукоделия</p>
                    </div>
                </div>
            </div>
        </div>
    );
}