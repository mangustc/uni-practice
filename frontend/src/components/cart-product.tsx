import * as objects from "../objects";
import * as requests from "../requests";
import { useEffect, useState } from "react";

export function CartProduct({
    productInfo,
    changeProductAmount
}: {
    productInfo: objects.ProductInCart;
    changeProductAmount: (productID: number, amount: number) => void;
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
          setAmount(amountNumber.toString());
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
        setAmount(amountNumber.toString());
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
        setAmount(amountNumber.toString());
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
        setAmount(amountNumber.toString());
    }

    return (
        <div style={{ padding: "10px", display: "flex" }}>
            <textarea value={JSON.stringify(productInfo, null, 2)}></textarea>
            <button onClick={downProductAmount}>-</button>
            <input value={amount} onChange={handleChange} onKeyDown={handleKeyDown} onBlur={handleBlur}></input>
            <button onClick={upProductAmount}>+</button>
        </div>
    )
}