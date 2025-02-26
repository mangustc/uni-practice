import { createContext, useState, useEffect } from "react";
import Card from "../components/card";

export default function forTesting() {
    return (
        <Card productCatalog={{
            productPrice: 100,
            productID: 1,
            productName: "fdsa",
            productMeasuredIn: "м",
            productHit: true,
            productNew: false,
            productPromotion: false,
            productPercentPromotion: 0,
            productNewPrice: 0,
            productInWishlist: false,
            productInStock: true,
            categoryID: 1
        }} photoSrc={""}></Card>
    );
}


