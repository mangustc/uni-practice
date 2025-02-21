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
    let totalProductsPrice = 0, totalPromotionPrice = 0, totalCartPrice = 0,
    itemPrice, totalPrice, priceDifference, promotionDifference;

    const newItems = cart.items.map((item) => {
      if (item.productID == productID) {
        priceDifference = item.productPrice * amount - item.productPrice * item.productAmountInCart;
        totalProductsPrice = cart.totalProductsPrice + priceDifference;

        if (item.productNewPrice != objects.DEFAULT_NUMBER) {
          promotionDifference = item.productPrice * amount - item.productNewPrice * amount;
          promotionDifference -= item.productPrice * item.productAmountInCart - item.productNewPrice * item.productAmountInCart;
          totalPromotionPrice = cart.totalPromotionPrice + promotionDifference;
          itemPrice = item.productNewPrice;
        } else {
          totalPromotionPrice = cart.totalPromotionPrice;
          itemPrice = item.productPrice;
        }

        totalPrice = itemPrice * amount;
        totalCartPrice = totalProductsPrice - totalPromotionPrice;
        
        const newProductInCart: objects.ProductInCart = {
          ...item,
          productAmountInCart: amount,
          totalPrice: totalPrice
        };
        return newProductInCart;
      } else {
        return item;
      }
    });

    const newCart: objects.Cart = {
      items: newItems,
      totalProductsPrice: totalProductsPrice,
      totalPromotionPrice: totalPromotionPrice,
      totalCartPrice: totalCartPrice
    };
    setCart(newCart);
  }

  function deleteProduct(productInfo: objects.ProductInCart) {
    requests.DELETE_deleteProductFromCart(productInfo.productID);

    let totalProductsPrice = cart.totalProductsPrice - productInfo.productPrice * productInfo.productAmountInCart;
    let totalPromotionPrice;
    if (productInfo.productNewPrice != objects.DEFAULT_NUMBER) {
      let priceDifference = productInfo.productPrice * productInfo.productAmountInCart - productInfo.productNewPrice * productInfo.productAmountInCart;
      totalPromotionPrice = cart.totalPromotionPrice - priceDifference;
    } else {
      totalPromotionPrice = cart.totalPromotionPrice;
    }
    let totalCartPrice = totalProductsPrice - totalPromotionPrice;
    const newCart = {
      items: cart.items.filter(a => a.productID !== productInfo.productID),
      totalProductsPrice: totalProductsPrice,
      totalPromotionPrice: totalPromotionPrice,
      totalCartPrice: totalCartPrice
    }
    setCart(newCart);
  }

  function clearCart() {
    requests.DELETE_clearCart();
    setCart({items: [], totalProductsPrice: 0, totalPromotionPrice: 0, totalCartPrice: 0})
  }

  return (
    <>
    {cart.items.map((item, index) => (
        <CartProduct key={index} productInfo={item} changeProductAmount={changeProductAmount} deleteProduct={deleteProduct}/>
    ))}
    <div style={{ paddingLeft: "10px" }}>
      <button onClick={clearCart}>Очистить корзину</button>
      <p>Товары: {cart.totalProductsPrice.toFixed(2)} ₽</p>
      <p>Скидка: {cart.totalPromotionPrice.toFixed(2)} ₽</p>
      <p>Итоговая цена: {cart.totalCartPrice.toFixed(2)} ₽</p>
    </div>
    </>
);
};
