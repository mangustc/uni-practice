// import { useNavigate } from "react-router-dom";
// import "./ForgotPassword.css";

// export function WishlistEmpty() {
//   const navigate = useNavigate();
//   return (
//     <div className="wishlist-empty-main">
//       <aside className="personal-aside" style={{ marginRight: "90px",marginTop: "-20px"}} >
//         <ul className="personal-aside-list">
//           <li><a href="#" className="personal-aside-link">Личные данные</a></li>
//           <li><a href="#" className="personal-aside-link">Заказы</a></li>
//           <li><a href="#" className="personal-aside-link">Профили заказов</a></li>
//           <li><a href="#" className="personal-aside-link">Избранное</a></li>
//           <button className="personal-exit-button">Выход</button>
//         </ul>
//       </aside>
//       <div className="wishlist-empty-container">
//         <div className="wishlist-empty-navigation">
//           <h3>В избранном ничего нет</h3>
//           <p>
//             Выберите понравившийся Вам товар из каталога интернет-магазина и
//             добавьте его в избранное
//           </p>
//           <section className="wishlist-categories-row">
//             <div
//               onClick={() => navigate("/catalog?currentCategoryID=1")}
//               className="wishlist-categories-panel-category"
//               id="fabrics"
//             >
//               <h6>Ткани</h6>
//             </div>
//             <div
//               onClick={() => navigate("/catalog?currentCategoryID=2")}
//               className="wishlist-categories-panel-category"
//               id="for-art"
//             >
//               <h6>Для творчества</h6>
//             </div>
//           </section>
//           <section className="wishlist-categories-row">
//             <div
//               onClick={() => navigate("/catalog?currentCategoryID=3")}
//               className="wishlist-categories-panel-category"
//               id="for-interior"
//             >
//               <h6>Для интерьера</h6>
//             </div>
//             <div
//               onClick={() => navigate("/catalog?currentCategoryID=4")}
//               className="wishlist-categories-panel-category"
//               id="accessories"
//             >
//               <h6>Фурнитура</h6>
//             </div>
//           </section>
//         </div>

//         <img
//             className="wishlist-empty-image"
//             src="/favorites-empty.svg"
//             alt="Избранное пустое"
//             />
        
//         </div>
//     </div>
//   );
// }


import { useNavigate } from "react-router-dom";
import "./ForgotPassword.css";

export function WishlistEmpty() {
  const navigate = useNavigate();
  return (
    <div className="wishlist-empty-navigation">
      <h3>В избранном ничего нет</h3>
      <p>
        Выберите понравившийся Вам товар из каталога интернет-магазина и
        добавьте его в избранное
      </p>
      <section className="wishlist-categories-row">
        <div
          onClick={() => navigate("/catalog?currentCategoryID=1")}
          className="wishlist-categories-panel-category"
          id="fabrics"
        >
          <h6>Ткани</h6>
        </div>
        <div
          onClick={() => navigate("/catalog?currentCategoryID=2")}
          className="wishlist-categories-panel-category"
          id="for-art"
        >
          <h6>Для творчества</h6>
        </div>
      </section>
      <section className="wishlist-categories-row">
        <div
          onClick={() => navigate("/catalog?currentCategoryID=3")}
          className="wishlist-categories-panel-category"
          id="for-interior"
        >
          <h6>Для интерьера</h6>
        </div>
        <div
          onClick={() => navigate("/catalog?currentCategoryID=4")}
          className="wishlist-categories-panel-category"
          id="accessories"
        >
          <h6>Фурнитура</h6>
        </div>
      </section>
      <img
          className="wishlist-empty-image"
          src="/favorites-empty.svg"
          alt="Избранное пустое"
          />
    </div>
  );
}
