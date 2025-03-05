import * as objects from "../objects";
import * as requests from "../requests";
import { useEffect, useState } from "react";
import { CartProduct } from "../components/cart-product";
import { CartEmpty } from "../components/cart-empty";
import { ProductList } from "../components/product-list";


export function Cart() {
  const [cart, setCart] = useState<objects.Cart>({items: [], totalProductsPrice: 0, totalPromotionPrice: 0, totalCartPrice: 0});
  const [products, setProducts] = useState<objects.ProductCatalog[]>([]);

  function refreshCart() {
    requests.GET_GetCart()
    .then((obj) => {
        setCart({...obj});
    });
  }
  
  useEffect(() => {
    refreshCart();
    requests.GET_GetProducts().then((prod) => { // для тестов
      setProducts([...prod, ...prod, ...prod].splice(0, 10));
    })
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
    <div className="cart-container">
    {cart.items.length == 0 && <CartEmpty />}
    {cart.items.length > 0 && <>
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
          <section className="cart-section-line">
            <div className="cart-opt-name">Товары:</div>
            <div className="cart-dotted-line"></div>
            <div className="cart-num-value">{cart.totalProductsPrice} ₽</div>
          </section>
          <section className="cart-section-line">
            <div className="cart-opt-name">Скидка:</div>
            <div className="cart-dotted-line"></div>
            <div className="cart-num-value">{cart.totalPromotionPrice} ₽</div>
          </section>
          <section className="cart-section-line" style={{marginTop: "10px"}}>
            <h4>Итого:</h4>
            <div className="cart-dotted-line"></div>
            <h4>{cart.totalCartPrice} ₽</h4>
          </section>
          <button className="cart-button">Оформить заказ</button>
          <div className="cart-opt-name" style={{ textAlign: "center", width: "200px" }}>Стоимость доставки определяется при оформлении заказа</div>
        </div>
      </div>
      </>}
      <ProductList title="Популярные товары" products={products} onAddListener={refreshCart}/>
    </div>
    );
};
