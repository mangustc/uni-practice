import * as objects from "../objects";
import * as requests from "../requests";
import { useEffect, useState } from "react";
import { CartProduct } from "../components/cart-product";
import { CartEmpty } from "../components/cart-empty";


export const Cart = function () {
  const [cart, setCart] = useState<objects.Cart>({items: [], totalProductsPrice: 0, totalPromotionPrice: 0, totalCartPrice: 0});
  
  useEffect(() => {
    requests
    .GET_GetCart()
    .then((obj) => {
        setCart({...obj});
    });
  }, []);

  var rounded = function(number: number){
    return +number.toFixed(2);
  }

  function changeProductAmount(productID: number, amount: number) {
    requests.PUT_ChangeProductAmountInCart(productID, amount);
    let totalProductsPrice = 0, totalPromotionPrice = 0, totalCartPrice = 0,
    itemPrice, totalPrice, priceDifference, promotionDifference;

    const newItems = cart.items.map((item) => {
      if (item.productID == productID) {
        priceDifference = rounded(item.productPrice * amount) - rounded(item.productPrice * item.productAmountInCart);
        totalProductsPrice = cart.totalProductsPrice + priceDifference;

        if (item.productNewPrice != objects.DEFAULT_NUMBER) {
          promotionDifference = rounded(item.productPrice * amount) - rounded(item.productNewPrice * amount);
          promotionDifference -= rounded(item.productPrice * item.productAmountInCart) - rounded(item.productNewPrice * item.productAmountInCart);
          totalPromotionPrice = cart.totalPromotionPrice + promotionDifference;
          itemPrice = item.productNewPrice;
        } else {
          totalPromotionPrice = cart.totalPromotionPrice;
          itemPrice = item.productPrice;
        }

        totalPrice = rounded(itemPrice * amount);
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
      totalProductsPrice: rounded(totalProductsPrice),
      totalPromotionPrice: rounded(totalPromotionPrice),
      totalCartPrice: rounded(totalCartPrice)
    };
    setCart(newCart);
  }

  function deleteProduct(productInfo: objects.ProductInCart) {
    requests.DELETE_deleteProductFromCart(productInfo.productID);

    let totalProductsPrice = cart.totalProductsPrice - rounded(productInfo.productPrice * productInfo.productAmountInCart);
    let totalPromotionPrice;
    if (productInfo.productNewPrice != objects.DEFAULT_NUMBER) {
      let priceDifference = rounded(productInfo.productPrice * productInfo.productAmountInCart) - rounded(productInfo.productNewPrice * productInfo.productAmountInCart);
      totalPromotionPrice = cart.totalPromotionPrice - priceDifference;
    } else {
      totalPromotionPrice = cart.totalPromotionPrice;
    }
    let totalCartPrice = totalProductsPrice - totalPromotionPrice;
    const newCart = {
      items: cart.items.filter(a => a.productID !== productInfo.productID),
      totalProductsPrice: rounded(totalProductsPrice),
      totalPromotionPrice: rounded(totalPromotionPrice),
      totalCartPrice: rounded(totalCartPrice)
    }
    setCart(newCart);
  }

  function clearCart() {
    requests.DELETE_clearCart();
    setCart({items: [], totalProductsPrice: 0, totalPromotionPrice: 0, totalCartPrice: 0})
  }

  return (
    <>
    {cart.items.length == 0 && <CartEmpty />}

    {cart.items.length > 0 && 
    <>
    <div className="cart-container">
      <div className="cart-top">
        <h1>Корзина</h1>
        <a className="cart-clear-button" onClick={clearCart}>Очистить корзину</a>
      </div>
      <div className="cart-information">
        <div className="cart-left-side">
          {cart.items.map((item, index) => (
              <CartProduct key={index} productInfo={item} changeProductAmount={changeProductAmount} deleteProduct={deleteProduct}/>
          ))}
        </div>
        <div className="cart-right-side">
          <p>Товары: {cart.totalProductsPrice} ₽</p>
          <p>Скидка: {cart.totalPromotionPrice} ₽</p>
          <p>Итоговая цена: {cart.totalCartPrice} ₽</p>
        </div>
      </div>
    </div>
    </>}
    </>
);
};
