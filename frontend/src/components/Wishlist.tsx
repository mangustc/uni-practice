import React, { useState } from "react";
import { WishlistEmpty } from "./wishlist-empty";
import Card from "./card";
import * as objects from "../objects"; // Импортируйте тип ProductCatalog

export function Wishlist() {
  const [wishlist, setWishlist] = useState<objects.ProductCatalog[]>([
    {
      productID: 1,
      productName: "Тестовый товар",
      productPrice: 100,
      productInWishlist: true,
      productHit: false,
      productNew: false,
      productPromotion: false,
      categoryID: 1,
      productMeasuredIn: "шт", 
      productInStock: true, 
      productPercentPromotion: 0, 
      productNewPrice: 0, 
    },
    {
      productID: 2,
      productName: "Тестовый товар",
      productPrice: 100,
      productInWishlist: true,
      productHit: false,
      productNew: false,
      productPromotion: false,
      categoryID: 1,
      productMeasuredIn: "шт", 
      productInStock: true, 
      productPercentPromotion: 0, 
      productNewPrice: 0, 
    },
    {
      productID: 3,
      productName: "Тестовый товар",
      productPrice: 100,
      productInWishlist: true,
      productHit: false,
      productNew: false,
      productPromotion: false,
      categoryID: 1,
      productMeasuredIn: "шт", 
      productInStock: true, 
      productPercentPromotion: 0, 
      productNewPrice: 0, 
    },
    {
      productID: 3,
      productName: "Тестовый товар",
      productPrice: 100,
      productInWishlist: true,
      productHit: false,
      productNew: false,
      productPromotion: false,
      categoryID: 1,
      productMeasuredIn: "шт", 
      productInStock: true, 
      productPercentPromotion: 0, 
      productNewPrice: 0, 
    }
  ]);

  return (
    <div className="wishlist-empty-main" style={{ position: "relative" }}>
      <aside className="personal-aside" style={{ position: "sticky", top: 0, marginRight: "90px", marginTop: "-20px", width: 250 }}>
        <ul className="personal-aside-list">
          <li><a href="#" className="personal-aside-link">Личные данные</a></li>
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
              photoSrc="/test-image.jpg"
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








