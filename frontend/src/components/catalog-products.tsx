import * as objects from "../objects";
import * as requests from "../requests";
import Card from "./card";

export function CatalogProducts({
  products,
}: {
  products: objects.ProductCatalog[];
}) {
  return (
    <div className="product-list-screen">
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
