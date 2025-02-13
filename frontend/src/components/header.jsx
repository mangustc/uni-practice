// import { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Header() {
  const navigate = useNavigate();
  // const { authenticated, setAuthenticated } = useContext(AuthContext);
  // const logout = function () {
  //   requests.PUT_logout().then(() => {
  //     setAuthenticated(false);
  //     navigate("/auth");
  //   });
  // };
  return (
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
      <div className="catalog-button">
        <img
          src="/menu.svg"
          alt=""
          style={{ marginLeft: "15px", marginRight: "15px" }}
        />
        <p style={{ color: "white", fontWeight: 700 }}>Каталог</p>
      </div>
      <div className="search" style={{ width: "507px" }}>
        <p>Поиск</p>
        <img src="/search.svg" alt="" />
      </div>
      <div
        style={{
          width: "fit-content",
          display: "flex",
          flexDirection: "row",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <div className="nav-panel-icons">
          <img src="/heart.svg" alt="" />
          <span style={{ fontWeight: 700, fontSize: "10px", height: "12px" }}>
            Избранное
          </span>
        </div>
        <div className="nav-panel-icons">
          <img src="/shopping-cart.svg" alt="" />
          <span style={{ fontWeight: 700, fontSize: "10px", height: "12px" }}>
            Корзина
          </span>
        </div>
        <div className="nav-panel-icons">
          <img src="/user.svg" alt="" />
          <span style={{ fontWeight: 700, fontSize: "10px", height: "12px" }}>
            Кабинет
          </span>
        </div>
      </div>
    </div>
  );
}
