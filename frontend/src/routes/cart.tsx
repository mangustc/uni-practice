import * as objects from "../objects";
import * as requests from "../requests";
import { useEffect, useState } from "react";
import { CartProduct } from "../components/cart-product";


export const Cart = function () {
  const [cart, setCart] = useState<objects.Cart>({items: [], totalProductsPrice: 0, totalPromotionPrice: 0, totalCartPrice: 0});
  
  useEffect(() => {
    requests
    .GET_GetCart()
    .then((obj) => {
        setCart({...obj});
    });
  }, []);

  function changeProductAmount(productID: number, amount: number) {
    requests.PUT_ChangeProductAmountInCart(productID, amount);
    requests.GET_GetCart()
    .then((obj) => {
        setCart({...obj});
    });
  }
  return (
    <>
    {cart.items.map((item, index) => (
        <CartProduct key={index} productInfo={item} changeProductAmount={changeProductAmount}/>
    ))}
    <div style={{ paddingLeft: "10px" }}>
        <p>Товары: {cart.totalProductsPrice} ₽</p>
        <p>Скидка: {cart.totalPromotionPrice} ₽</p>
        <p>Итоговая цена: {cart.totalCartPrice} ₽</p>
    </div>
    </>
);
};
