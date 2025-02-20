export default function Card() {
    return(
        <div className="card-container">
            <div className="card-photo">
                <div>
                <div className="card-filter">Хит</div>
                <div className="card-filter">Новинка</div>
                <div className="card-filter">Акция</div>
                </div>
                <div className="card-like"></div>
                
            </div>
            <span className="card-name">Text</span>
            <span className="card-descr">Цена, м</span>
            <span className="card-cost">14 Р</span>
            <button className="card-add-btn">В корзину</button>
        </div>
    );
}