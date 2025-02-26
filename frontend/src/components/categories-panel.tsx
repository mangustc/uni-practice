import { useNavigate } from "react-router-dom";

export default function CategoriesPanel() {
    const navigate = useNavigate();
    return (
        <div className="screen-container">
            <div className="categories-panel-container">
                <div onClick={() => navigate("/catalog?currentCategoryID=1")} className="categories-panel-category" id="fabrics" >
                    <h6>Ткани</h6>
                </div>
                <div onClick={() => navigate("/catalog?currentCategoryID=2")} className="categories-panel-category" id="for-art">
                    <h6>Для творчества</h6>
                </div>
                <div onClick={() => navigate("/catalog?currentCategoryID=3")} className="categories-panel-category" id="for-interior">
                    <h6>Для интерьера</h6>
                </div>
                <div onClick={() => navigate("/catalog?currentCategoryID=4")} className="categories-panel-category" id="accessories">
                    <h6>Фурнитура</h6>
                </div>
            </div>
        </div>
    );
}
