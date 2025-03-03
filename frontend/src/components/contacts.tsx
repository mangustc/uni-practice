import "../index.css";
import "./ForgotPassword.css";


const Contacts = () => {
  return (
    <div className="contacts-container">
      <h1 className="contacts-title">Контакты</h1>

      <div className="contacts-blocks">
        <div className="contacts-block">
          <h4 className="contacts-block-title small-title">Офис</h4>
          <a href="tel:+73822903040" className="contacts-phone small-text">+7 (3822) 90-30-40</a>
          <a href="mailto:whiterose70@mail.ru" className="contacts-email small-text">whiterose70@mail.ru</a>
          <p className="contacts-time small-text">пн-пт: 10:00-18:00</p>
          <p className="contacts-dayoff small-text">сб-вс: выходной</p>
        </div>

        <div className="contacts-block">
          <h4 className="contacts-block-title small-title">Отдел продаж</h4>
          <a href="tel:+73822903040" className="contacts-phone small-text">+7 (3822) 90-30-40</a>
          <a href="mailto:whiterose70@mail.ru" className="contacts-email small-text">whiterose70@mail.ru</a>
        </div>

        <div className="contacts-block">
          <h4 className="contacts-block-title small-title">Отдел закупок</h4>
          <a href="tel:+73822903040" className="contacts-phone small-text">+7 (3822) 90-30-40</a>
          <a href="mailto:bel.roza70@mail.ru" className="contacts-email small-text">bel.roza70@mail.ru</a>
          <p className="contacts-additional small-text">Доб. 1016</p>
        </div>
      </div>

      <div className="contacts-additional-info">
        <div className="contacts-commercial">
          <h4 className="contacts-block-title small-title">Для коммерческих предложений</h4>
          <a href="mailto:whiterose70@mail.ru" className="contacts-email small-text">whiterose70@mail.ru</a>
        </div>

        <div className="contacts-general">
          <h4 className="contacts-block-title small-title">Общие вопросы</h4>
          <a href="mailto:whiterose70@mail.ru" className="contacts-email small-text">whiterose70@mail.ru</a>
        </div>
      </div>

      <div className="contacts-requisites">
        <h4 className="contacts-requisites-title small-title">Реквизиты</h4>
        <p className="contacts-block-title small-title">Контакты</p>
        <p className="contacts-requisites-text small-text">Юридический адрес: 634021, г. Томск, ул. Елизаровых, 93</p>
        <p className="contacts-requisites-text small-text">ОГРН: 1117017028149</p>
        <p className="contacts-requisites-text small-text">ИНН: 7017297507</p>
        <p className="contacts-requisites-text small-text">КПП: 701701001</p>
      </div>
    </div>
  );
};

export default Contacts;

