import * as objects from "./objects.tsx";

export const BACKEND_URL: string = import.meta.env.VITE_BACKEND_URL;
const HEADER_JSON = {
  "Content-Type": "application/json",
  accept: "application/json",
};

export async function GET_GetInfoForCatalogPage(
  categoryID: number,
): Promise<objects.CatalogPageValues> {
  let response = await fetch(
    BACKEND_URL + `/filter/get_info_for_catalog_page/${categoryID}`,
    {
      method: "GET",
      headers: HEADER_JSON,
      credentials: "include",
    },
  );
  const json: objects.CatalogPageInfoIn = await response.json();

  // TODO: HANDLE ERROR
  const status = response.status;

  return objects.GetCatalogPageValues(json);
}

export async function POST_GetProductsByCategory(
  catalogFilterSort: objects.CatalogFilterSortOut,
): Promise<objects.ProductCatalog[]> {
  let response = await fetch(
    BACKEND_URL +
      `/filter/products/by-category?` +
      new URLSearchParams({
        sort_by: catalogFilterSort.sort_by,
        filter_by_params: catalogFilterSort.filter_by_params,
      }),
    {
      method: "POST",
      headers: HEADER_JSON,
      body: JSON.stringify(catalogFilterSort.filters),
      credentials: "include",
    },
  );
  const json: objects.ProductCatalogIn[] = await response.json();

  // TODO: HANDLE ERROR
  const status = response.status;

  return objects.NewProductCatalogList(json);
}

// export async function GET_GetCategoryList() {
//   // let response = await fetch(BACKEND_URL + "/dish/get_dishes", {
//   //   method: "POST",
//   //   headers: HEADER_JSON,
//   //   credentials: "include",
//   // });
//   return [
//     objects.NewCategory({
//       category_id: 1,
//       category_name: "test",
//     }),
//     objects.NewCategory({
//       category_id: 2,
//       category_name: "test2",
//     }),
//     objects.NewCategory({
//       category_id: 3,
//       category_name: "test3",
//       category_parent_id: 1,
//     }),
//     objects.NewCategory({
//       category_id: 4,
//       category_name: "test4",
//       category_parent_id: 1,
//     }),
//     objects.NewCategory({
//       category_id: 5,
//       category_name: "test6",
//       category_parent_id: 1,
//     }),
//     objects.NewCategory({
//       category_id: 6,
//       category_name: "testunder",
//       category_parent_id: 3,
//     }),
//   ];
// }

export async function GET_GetCart() {
  let response = await fetch(BACKEND_URL + "/cart/get_user_cart", {
    method: "GET",
    headers: HEADER_JSON,
    credentials: "include",
  });
  return objects.mapCart(await response.json());
  /*
  return objects.mapCart({
    items: [{
      product_id: 1,
      article_id: 262,
      product_name: "test",
      product_measured_in: "м",
      product_amount: 5,
      product_amount_in_cart: 2.5,
      product_price: 110,
      product_percent_promotion: null,
      product_new_price: null,
      total_price: 275
    },
    {
      product_id: 7,
      article_id: 631,
      product_name: "test2",
      product_measured_in: "шт",
      product_amount: 7,
      product_amount_in_cart: 1,
      product_price: 230,
      product_percent_promotion: 10,
      product_new_price: 207,
      total_price: 207
    }
  ],
    total_products_price: 505,
    total_promotion_price: 23,
    total_cart_price: 482
  });
  */
}

export async function DELETE_deleteProductFromCart(productID: number) {
  await fetch(BACKEND_URL + `/cart/delete_from_cart/${productID}`, {
    method: "DELETE",
    headers: HEADER_JSON,
    credentials: "include",
  });
}

export async function DELETE_clearCart() {
  await fetch(BACKEND_URL + `/cart/clear_cart`, {
    method: "DELETE",
    headers: HEADER_JSON,
    credentials: "include",
  });
}

export async function PUT_ChangeProductAmountInCart(
  productID: number,
  amount: number,
) {
  await fetch(
    BACKEND_URL + `/cart/change_amount_in_cart/${productID}/${amount}`,
    {
      method: "PUT",
      headers: HEADER_JSON,
      credentials: "include",
    },
  );
}

