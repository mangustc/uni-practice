import * as objects from "./objects.tsx";
import { ResponseInfoFromResponse } from "./util.tsx";

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

export async function GET_GetProductForPage(
  productID: number,
): Promise<objects.ProductForPage> {
  let response = await fetch(
    BACKEND_URL + `/product/get_product_for_page/${productID}`,
    {
      method: "GET",
      headers: HEADER_JSON,
      credentials: "include",
    },
  );
  const json: objects.ProductForPageIn = await response.json();

  // TODO: HANDLE ERROR
  const status = response.status;

  return objects.NewProductForPage(json);
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

export async function GET_GetProducts() { // для тестов
  const response = await fetch(BACKEND_URL + '/product/get_all_products', {
    method: "GET",
    headers: HEADER_JSON,
    credentials: "include",
  });
  return objects.NewProductCatalogList(await response.json());
}

export async function PUT_ChangeWishlistState(productID: number): Promise<{
  message: string;
  status: boolean;
}> {
  let response = await fetch(`${BACKEND_URL}/product/change_wishlist_state/${productID}`, {
    method: "PUT",
    headers: HEADER_JSON,
    credentials: "include",
  });

  const json = await response.json();
  // TODO: Handle Error

  return json;
}

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

export async function POST_AddInCart(productID: number, amount: number): Promise<any> {
  let response = await fetch(
    BACKEND_URL + `/cart/add_in_cart/${productID}/${amount}`,
    {
      method: "POST",
      headers: HEADER_JSON,
      credentials: "include",
    },
  );
  // TODO: Handle error or success

  return await response.json();
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

export async function PUT_Login(
  email: string,
  password: string
) {
  const request = {email: email, password: password};
  const response = await fetch(BACKEND_URL + `/user/login`, {
    method: "PUT",
    headers: HEADER_JSON,
    body: JSON.stringify(request),
    credentials: "include",
  });

  const info = await ResponseInfoFromResponse(response);
  return(info);
}

export async function POST_Register(
  email: string,
  password: string,
  confirmPassword: string,
  phone: string
) {
  const request = {email: email, password: password, re_password: confirmPassword, number: phone};
  const response = await fetch(BACKEND_URL + `/user/register`, {
    method: "POST",
    headers: HEADER_JSON,
    body: JSON.stringify(request),
    credentials: "include",
  });
  
  const info = await ResponseInfoFromResponse(response);
  return(info);
}

export async function POST_RegisterLegal(
  email: string,
  password: string,
  confirmPassword: string,
  phone: string,
  organizationName: string,
  inn: string
) {
  const request = {email: email, password: password, re_password: confirmPassword,
    number: phone, organization_name: organizationName, INN: inn};
  const response = await fetch(BACKEND_URL + `/user/register_legal_entity`, {
    method: "POST",
    headers: HEADER_JSON,
    body: JSON.stringify(request),
    credentials: "include",
  });
  
  const info = await ResponseInfoFromResponse(response);
  return(info);
}

export async function POST_RegisterIP(
  email: string,
  password: string,
  confirmPassword: string,
  phone: string,
  organizationName: string,
  inn: string
) {
  const request = {email: email, password: password, re_password: confirmPassword,
    number: phone, organization_name: organizationName, INN: inn};
  const response = await fetch(BACKEND_URL + `/user/register_ip`, {
    method: "POST",
    headers: HEADER_JSON,
    body: JSON.stringify(request),
    credentials: "include",
  });
  
  const info = await ResponseInfoFromResponse(response);
  return(info);
}


export async function POST_Logout() {
  const response = await fetch(BACKEND_URL + `/user/logout`, {
      method: "POST",
      headers: HEADER_JSON,
      credentials: "include",
  });

  const info = await ResponseInfoFromResponse(response);
  return info;
}


export async function GET_GetUserInfo() {
  const response = await fetch(BACKEND_URL + `/user/me`, {
    method: "GET",
    headers: HEADER_JSON,
    credentials: "include",
  });

  if (!response.ok) {
    throw new Error(`Ошибка при получении данных пользователя: ${response.status}`);
  }

  return await response.json();
}

export async function PUT_UpdateUserInfo(
  name: string,
  surname: string,
  number: string,
  password: string,
  confirmPassword: string
) {
  const request = {
    name,
    surname,
    number,
    password,
    confirm_password: confirmPassword,
  };

  const response = await fetch(BACKEND_URL + `/user/update_info`, {
    method: "PUT",
    headers: HEADER_JSON,
    body: JSON.stringify(request),
    credentials: "include",
  });

  if (!response.ok) {
    throw new Error(`Ошибка при обновлении данных пользователя: ${response.status}`);
  }

  return await response.json();
}


export async function POST_RequestPasswordReset(email: string) {
  try {
    const request = { email: email };
    console.log("Отправляем запрос на сброс пароля с email:", email);

    const response = await fetch(BACKEND_URL + `/user/request_password_reset`, {
      method: "POST",
      headers: {
        ...HEADER_JSON,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
      credentials: "include",
    });

    console.log("Получен ответ от сервера:", response);

    const info = await ResponseInfoFromResponse(response);
    console.log("Результат обработки ответа:", info);
    return info;
  } catch (error) {
    console.error("Ошибка при отправке запроса:", error);
    throw error;
  }
}