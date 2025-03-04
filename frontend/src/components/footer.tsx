import { useNavigate } from "react-router-dom";

export default function Footer() {
  const navigate = useNavigate();
  return (
    <div className="footer-container-container">
      <div className="footer-container">
        <div className="footer-upper">
          <div className="footer-categories">
            <div className="footer-category">
              <h6 style={{ marginBottom: "5px" }}>Каталог</h6>
              <span onClick={() => {navigate("/catalog?currentCategoryID=1"); location.reload()}} className="footer-text-gray">Ткани</span>
              <span onClick={() => {navigate("/catalog?currentCategoryID=2"); location.reload()}} className="footer-text-gray">Для интерьера</span>
              <span onClick={() => {navigate("/catalog?currentCategoryID=3"); location.reload()}} className="footer-text-gray">Для творчества</span>
              <span onClick={() => {navigate("/catalog?currentCategoryID=4"); location.reload()}} className="footer-text-gray">Фурнитура</span>
              <span onClick={() => {navigate("/catalog?currentFilterByParam=promotion&currentCategoryID=1"); location.reload()}} className="footer-text-gray">Акции</span>
            </div>
            <div className="footer-category">
              <h6 style={{ marginBottom: "5px" }}>Покупателям</h6>
              <span className="footer-text-gray">Доставка</span>
              <span className="footer-text-gray">Способы оплаты</span>
              <span className="footer-text-gray">Возврат товара</span>
              <span className="footer-text-gray">Оптовым покупателям</span>
              <span className="footer-text-gray">Бюджетным организациям</span>
              <span className="footer-text-gray">Мастер-классы</span>
            </div>
            <div className="footer-category">
              <h6 style={{ marginBottom: "5px" }}>Компания</h6>
              <span className="footer-text-gray">Вакансии</span>
              <span className="footer-text-gray">О компании</span>
              <span className="footer-text-gray">Стать партнером</span>
            </div>
            <div className="footer-category">
              <h6 style={{ marginBottom: "5px" }}>Информация</h6>
              <span className="footer-text-gray">Наши магазины</span>
              <span className="footer-text-gray">Обратная связь</span>
              <span onClick={() => {navigate("/contacts"); location.reload()}} className="footer-text-gray">Контакты</span>
            </div>
          </div>
          <div className="footer-contacts">
            <span className="footer-phone">8-800-250-8045</span>
            <span
              style={{
                fontWeight: 400,
                fontSize: "14px",
                color: "var(--text-color-black-main-50)",
                marginBottom: "40px",
                height: "16px",
              }}
            >
              офис продаж
            </span>
            <span className="footer-mail">support@wrose.ru</span>
            <div className="footer-vk">
              <img src="vk-logo.svg" alt="" />
            </div>
          </div>
        </div>
        <div className="footer-bot">
          <div className="display-column">
            <div className="footer-icons">
              <img src="/mastercard.svg" alt="" />
              <img src="/visa.svg" alt="" />
              <img src="/mir.svg" alt="" />
            </div>
            <span className="footer-bot-text">
              Текстиль-центр "Белая роза" © 2014-2025
            </span>
          </div>
          <div className="footer-info-links">
            <span className="footer-bot-text hover-text">
              Политика конфиденциальности
            </span>
            <span className="footer-bot-text hover-text">Cookies</span>
          </div>
        </div>
      </div>
    </div>
  );
}
