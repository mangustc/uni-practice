export default function Footer() {
  return (
    <div className="footer-container-container">
      <div className="footer-container">
        <div className="footer-upper">
          <div className="footer-categories">
            <div className="footer-category">
              <h6 style={{ marginBottom: "5px" }}>Каталог</h6>
              <span className="footer-text-gray">Ткани</span>
              <span className="footer-text-gray">Для интерьера</span>
              <span className="footer-text-gray">Для творчества</span>
              <span className="footer-text-gray">Фурнитура</span>
              <span className="footer-text-gray">Акции</span>
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
              <span className="footer-text-gray">Контакты</span>
            </div>
          </div>
          <div className="footer-contacts">
            <span>Phone</span>
            <span>Офис продаж</span>
            <span>pochta</span>
          </div>
        </div>
      </div>
    </div>
  );
}
