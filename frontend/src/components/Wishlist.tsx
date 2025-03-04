import React, { useState, useEffect, useContext } from "react";
import { WishlistEmpty } from "./wishlist-empty";
import Card from "./card";
import * as objects from "../objects"; // Импортируйте тип ProductCatalog
import * as requests from "../requests";
import { Navigate } from 'react-router-dom';
import { AuthContext } from "../routes/root";

export function Wishlist() {
  const [wishlist, setWishlist] = useState<objects.ProductCatalog[]>([]);
  const { authenticated, setAuthenticated } = useContext(AuthContext);
  if (!authenticated) {
    return <Navigate to="/login" />;
  }

  useEffect(() => {
    requests.GET_GetWishlist().then((objs) => {
      setWishlist(objs);
    })
  }, []);


  return (
    <div className="wishlist-empty-main" style={{ position: "relative" }}>
      <aside className="personal-aside" style={{ position: "sticky", top: 0, marginRight: "90px", marginTop: "-20px", width: 250 }}>
        <ul className="personal-aside-list">
          <li><a href="/customer" className="personal-aside-link">Личные данные</a></li>
          <li><a href="#" className="personal-aside-link">Заказы</a></li>
          <li><a href="#" className="personal-aside-link">Профили заказов</a></li>
          <li><a href="#" className="personal-aside-link">Избранное</a></li>
          <button className="personal-exit-button">Выход</button>
        </ul>
      </aside>
      {wishlist.length === 0 && (
        <div className="wishlist-empty-container">
          <WishlistEmpty />
        </div>
      )}
      {wishlist.length > 0 && (
    <div className="wishlist-products-container">
      <h3>Избранное</h3>
      <div className="wishlist-products">
        {wishlist.map((item, index) => (
          <div key={index} className="wishlist-card-container">
            <Card
              productCatalog={item}
              photoSrc={`${requests.BACKEND_URL}/product/get_photo/${item.productID}`}
              refreshOnAdd={false}
              />
          </div>
          ))}
          </div>
        </div>
      )}
    </div>
  );
}








