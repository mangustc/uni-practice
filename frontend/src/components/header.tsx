// import { useContext } from "react";
// import { Link, useNavigate } from "react-router-dom";

export default function Header() {
  // const navigate = useNavigate();
  // const { authenticated, setAuthenticated } = useContext(AuthContext);
  // const logout = function () {
  //   requests.PUT_logout().then(() => {
  //     setAuthenticated(false);
  //     navigate("/auth");
  //   });
  // };
  return (
    <div className="navigation-container-container">
      <div className="navigation-info">
        <span className="nav-info-text">8-800-250-8045</span>
        <div className="nav-panel-group" style={{ gap: "24px" }}>
          <span className="nav-info-text-gray"> Оптовым покупателям</span>
          <span className="nav-info-text-gray">О компании</span>
          <span className="nav-info-text-gray">Мастер-классы</span>
          <span className="nav-info-text-gray">Контакты</span>
        </div>
      </div>
      <div className="navigation-container">
        {/* <nav
        className="links-container"
        style={{
          borderBottom: "1px solid #c2c2c2",
        }}
      >
        <Link className="link-button" to={`orders`}>
          <button style={{ width: "126px", marginBottom: "12px" }}>
            Заказы
          </button>
        </Link>
      </nav> */}
        <div>
          <img src="/logo.svg" alt="" />
        </div>
        <div className="nav-panel-group">
          <div className="catalog-button">
            <img
              src="/menu.svg"
              alt=""
              style={{ marginLeft: "15px", marginRight: "15px" }}
            />
            <p style={{ color: "white", fontWeight: 700 }}>Каталог</p>
          </div>
          <div className="search">
            <p style={{ color: "var(--text-color-black-main-50)" }}>
              Поиск по каталогу
            </p>
            <img src="/search.svg" alt="" />
          </div>
          <div className="nav-panel-icons">
            <div id="nav-heart" className="nav-panel-icon">
              <img src="/heart.svg" alt="" />
              <span
                style={{ fontWeight: 700, fontSize: "10px", height: "12px" }}
              >
                Избранное
              </span>
            </div>
            <div id="nav-cart" className="nav-panel-icon">
              <img src="/shopping-cart.svg" alt="" />
              <span
                style={{ fontWeight: 700, fontSize: "10px", height: "12px" }}
              >
                Корзина
              </span>
            </div>
            <div id="nav-user" className="nav-panel-icon">
              <img src="/user.svg" alt="" />
              <span
                style={{
                  fontWeight: 700,
                  fontSize: "10px",
                  height: "12px",
                }}
              >
                Кабинет
              </span>
            </div>
            <div
              id="nav-login"
              className="nav-panel-icon"
              style={{ display: "none" }}
            >
              <img src="/login.svg" alt="" />
              <span
                style={{
                  fontWeight: 700,
                  fontSize: "10px",
                  height: "12px",
                }}
              >
                Вход
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
