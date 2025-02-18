export default function Card() {
    return(
        <div className="card-container">
            <div className="card-photo"></div>
            <span className="card-name">Text</span>
            <span className="card-descr">Цена, м</span>
            <span className="card-cost">14 Р</span>
            <button className="card-add-btn">В корзину</button>
        </div>
    );
}