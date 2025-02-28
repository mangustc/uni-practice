import * as objects from "../objects";
import * as requests from "../requests";
import { useEffect, useState } from "react";

export function CartProduct({
    productInfo,
    changeProductAmount,
    deleteProduct
}: {
    productInfo: objects.ProductInCart;
    changeProductAmount: (productID: number, amount: number) => void;
    deleteProduct: (productInfo: objects.ProductInCart) => void;
}) {
    const [amount, setAmount] = useState<string>(productInfo.productAmountInCart.toString());
    const [wishlist, setWishlist] = useState<boolean>(productInfo.productInWishlist);
    const [imageSrc, setImageSrc] = useState<string>("");

    useEffect(() => {
        requests.GET_getProductPhotoURL(productInfo.productID).then((imageURL) => {
            setImageSrc(imageURL);
        });
    }, []);

    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setAmount(event.target.value);
      };

    const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
        if (event.key === 'Enter') {
          let amountNumber = Number(amount);
          if (Number.isNaN(amountNumber) || amountNumber < 0.1) {
            if (productInfo.productMeasuredIn != "м") {
                amountNumber = 1;
            } else {
                amountNumber = 0.1;
            }
          }
          if (productInfo.productMeasuredIn != "м") {
            amountNumber = Math.floor(amountNumber);
          }
          if (amountNumber > productInfo.productAmount)
            amountNumber = productInfo.productAmount;
          amountNumber = Number(amountNumber.toFixed(1));
          changeProductAmount(productInfo.productID, amountNumber);
        }
      };

    const handleBlur = () => {
        let amountNumber = Number(amount);
        if (Number.isNaN(amountNumber) || amountNumber < 0.1) {
            if (productInfo.productMeasuredIn != "м") {
                amountNumber = 1;
            } else {
                amountNumber = 0.1;
            }
        }
        if (productInfo.productMeasuredIn != "м") {
            amountNumber = Math.floor(amountNumber);
        }
        if (amountNumber > productInfo.productAmount)
            amountNumber = productInfo.productAmount;
        amountNumber = Number(amountNumber.toFixed(1));
        changeProductAmount(productInfo.productID, amountNumber);
    };

    function downProductAmount() {
        let amountNumber = Number(amount);
        if (Number.isNaN(amountNumber)) {
            if (productInfo.productMeasuredIn != "м") {
                amountNumber = 1;
            } else {
                amountNumber = 0.1;
            }
        } else {
            if (productInfo.productMeasuredIn != "м") {
                amountNumber -= 1;
                amountNumber = Number(amountNumber.toFixed(1))
            } else {
                amountNumber -= 0.1;
                amountNumber = Number(amountNumber.toFixed(1))
            }
            if (amountNumber < 0.1)
                return;
        }
        changeProductAmount(productInfo.productID, amountNumber);
    }

    function upProductAmount() {
        let amountNumber = Number(amount);
        if (Number.isNaN(amountNumber)) {
            if (productInfo.productMeasuredIn != "м") {
                amountNumber = 1;
            } else {
                amountNumber = 0.1;
            }
        } else {
            if (productInfo.productMeasuredIn != "м") {
                amountNumber += 1;
                amountNumber = Number(amountNumber.toFixed(1))
            } else {
                amountNumber += 0.1;
                amountNumber = Number(amountNumber.toFixed(1))
            }
            if (amountNumber > productInfo.productAmount)
                return;
        }
        changeProductAmount(productInfo.productID, amountNumber);
    }

    useEffect(() => {
        setAmount(productInfo.productAmountInCart.toString());
      }, [productInfo]);
    
    /*<div style={{ padding: "10px", display: "flex" }}>
            <textarea value={JSON.stringify(productInfo, null, 2)}></textarea>
            <button onClick={downProductAmount}>-</button>
            <input value={amount} onChange={handleChange} onKeyDown={handleKeyDown} onBlur={handleBlur}></input>
            <button onClick={upProductAmount}>+</button>
            <button onClick={() => {deleteProduct(productInfo)}}>Удалить</button>
        </div>*/
    
    function handleWishlist() {
        requests.PUT_ChangeWishlistState(productInfo.productID);
        setWishlist(!wishlist);
    }
    
    return (
        <div className="cart-product-container">
            <div className="cart-product-line">
                <div style={{display: "flex"}}>
                    <img className="cart-product-image" src={imageSrc != "" ? imageSrc : undefined} alt=""></img>
                    <div>
                        <div className="cart-opt-name">Арт. {productInfo.articleID}</div>
                        <div className="cart-product-name">{productInfo.productName}</div>
                    </div>
                </div>
                <div className="cart-product-trash" onClick={() => {deleteProduct(productInfo)}}></div>
            </div>
            <div className="cart-product-line">
                <div style={{ display: "flex" }}>
                    <div style={{ marginRight: "52px" }}>
                        <div className="cart-opt-name">Цена, {productInfo.productMeasuredIn}</div>
                        <div style={{ display: "flex", alignItems: "end", gap: "12px" }}>
                            <div className="cart-num-value" style={{ lineHeight: "18px" }}>{productInfo.productNewPrice != 0 ? productInfo.productNewPrice : productInfo.productPrice} ₽</div>
                            {productInfo.productNewPrice != 0 && <>
                            <div className="cart-opt-name" style={{ lineHeight: "16px", textDecoration: "line-through" }}>{productInfo.productPrice} ₽</div>
                            <div className="cart-product-percent">-{productInfo.productPercentPromotion}%</div>
                            </>
                            }
                        </div>
                    </div>
                    <div>
                        <div className="cart-opt-name">Сумма</div>
                        <div className="cart-num-value">{productInfo.totalPrice} ₽</div>
                    </div>
                </div>
                <div style={{ display: "flex", alignItems: "center"}}>
                    <div className="cart-product-minus" onClick={downProductAmount}></div>
                    <input className="cart-product-input" value={amount} onChange={handleChange} onKeyDown={handleKeyDown} onBlur={handleBlur}></input>
                    <div className="cart-product-plus" onClick={upProductAmount}></div>
                    <div className={wishlist ? "cart-product-like" : "cart-product-not-like"} onClick={handleWishlist}></div>
                </div>
            </div>
        </div>
    )
}