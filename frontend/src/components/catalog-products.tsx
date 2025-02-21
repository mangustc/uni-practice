import * as objects from "../objects";
import * as requests from "../requests";
import Card from "./card";

export function CatalogProducts({
  products,
}: {
  products: objects.ProductCatalog[];
}) {
  return (
    <div style={{ display: "flex", flexDirection: "row", flexWrap: "wrap" }}>
      {products.map((product) => (
        <Card
          key={product.productID}
          productCatalog={product}
          photoSrc={`${requests.BACKEND_URL}/product/get_photo/${product.productID}`}
        />
      ))}
    </div>
  );
}
