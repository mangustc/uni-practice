import { useState, useEffect, useRef } from "react";
import CategoriesPanel from "../components/categories-panel";
import { useNavigate } from 'react-router-dom';
import { ProductList } from "../components/product-list";
import * as objects from "../objects";
import * as requests from "../requests";

export default function Main() {
    const navigate = useNavigate();
    const [popularProducts, setPopularProducts] = useState<objects.ProductCatalog[]>([]);
    const [newProducts, setNewProducts] = useState<objects.ProductCatalog[]>([]);
    const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
    const [className1, setClassName1] = useState("main-animated-photo");
    const [className2, setClassName2] = useState("main-animated-photo");
    const [className3, setClassName3] = useState("main-animated-photo");
    const [className4, setClassName4] = useState("main-animated-photo");
    const [className5, setClassName5] = useState("main-animated-photo");

    const idToClassName = {"1": setClassName1, "2": setClassName2, "3": setClassName3, "4": setClassName4, "5": setClassName5};

    useEffect(() => {
        requests.GET_GetProducts().then((prod) => { // для тестов
          setPopularProducts([...prod, ...prod, ...prod]);
          setNewProducts([...prod, ...prod, ...prod]);
        })
      }, []);

    function onMouseEnter(e: React.MouseEvent<HTMLElement>) {
        const photoId = e.currentTarget.getAttribute("id");
        if (photoId)
            idToClassName[photoId as keyof typeof idToClassName]("main-animated-photo--show");
    }
    function onMouseMove(e: React.MouseEvent<HTMLElement>) {
        setMousePosition({ x: e.pageX+16, y: e.pageY+16 });
    };
    function onMouseLeave(e: React.MouseEvent<HTMLElement>) {
        const photoId = e.currentTarget.getAttribute("id");
        if (photoId)
            idToClassName[photoId as keyof typeof idToClassName]("main-animated-photo");
    }

    const values = {onMouseEnter, onMouseMove, onMouseLeave}

    return (
        <div className="main-container">
            <CategoriesPanel></CategoriesPanel>
            <div className="main-image" onClick={() => {navigate("/catalog?currentCategoryID=1")}}>
                <button className="main-image-button">Выбрать</button>
            </div>
            <ProductList title="Популярные товары" products={popularProducts}/>
            <ProductList title="Новинки" products={newProducts}/>
            <div>
                <section className="main-text-container"><h1 className="main-name">Белая роза</h1><h1>&nbsp;— крупный магазин&nbsp;</h1>
                    <div className="main-underline-text"><h1 id="1" { ...values }>тканей</h1> <div className="main-line-red"/><div className="main-line-white"/></div>
                    <h1>,&nbsp;</h1>
                    <div className="main-underline-text"><h1 id="2" { ...values }>аксессуаров</h1> <div className="main-line-red"/><div className="main-line-white"/></div>
                    <h1>,</h1>
                </section>
                <section className="main-text-container">
                    <div className="main-underline-text"><h1 id="3" { ...values }>фурнитуры</h1> <div className="main-line-red"/><div className="main-line-white"/></div>
                    <h1>&nbsp;высокого качества и товаров для&nbsp;</h1>
                    <div className="main-underline-text"><h1 id="4" { ...values }>вышивки</h1> <div className="main-line-red"/><div className="main-line-white"/></div>
                    <h1>&nbsp;и</h1>
                </section>
                <section className="main-text-container">
                    <div className="main-underline-text"><h1 id="5" { ...values }>вязания</h1> <div className="main-line-red"/><div className="main-line-white"/></div>
                    <h1>&nbsp;в Томске</h1>
                </section>
            </div>

            <div className="main-animated-container"
                style={{
                    left: mousePosition.x,
                    top: mousePosition.y,
                }}>
                <img
                id="photo1"
                src="main-photo-1.png"
                alt=""
                className={className1}
                />
                <img
                id="photo2"
                src="main-photo-2.png"
                alt=""
                className={className2}
                />
                <img
                id="photo3"
                src="main-photo-3.png"
                alt=""
                className={className3}
                />
                <img
                id="photo4"
                src="main-photo-4.png"
                alt=""
                className={className4}
                />
                <img
                id="photo5"
                src="main-photo-5.png"
                alt=""
                className={className5}
                />
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
                    <div className="main-advantages-last-elem">
                        <h4 className="main-advantages-num">4</h4>
                        <p style={{ maxWidth: "196px" }}>широкому ассортименту товаров для рукоделия</p>
                    </div>
                </div>
            </div>
        </div>
    );
}