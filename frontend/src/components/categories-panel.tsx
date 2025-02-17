export default function CategoriesPanel() {
    return (
        <div className="screen-container">
            <div className="categories-panel-container">
                <div className="categories-panel-category" id="fabrics" >
                    <h6>Ткани</h6>
                </div>
                <div className="categories-panel-category" id="for-art">
                    <h6>Для творчества</h6>
                </div>
                <div className="categories-panel-category" id="for-interior">
                    <h6>Для интерьера</h6>
                </div>
                <div className="categories-panel-category" id="accessories">
                    <h6>Фурнитура</h6>
                </div>
            </div>
        </div>
    );
}