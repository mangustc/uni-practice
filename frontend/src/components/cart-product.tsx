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
    
    return (
        <div className="cart-product-container">
            <div className="cart-product-line">
                <div style={{display: "flex"}}>
                    <img style={{ width: "78px", maxHeight: "54px", marginRight: "16px" }} src="/cart-empty.svg" alt=""></img>
                    <div>
                        <div className="cart-opt-name">Арт. {productInfo.articleID}</div>
                        <div className="cart-product-name">Хлопок рубашечный полоска 47560 (2, голубой)</div>
                    </div>
                </div>
                <img src="/trash-alt.svg" alt=""></img>
            </div>
            <div className="cart-product-line">
                
            </div>
        </div>
    )
}