export const DEFAULT_NUMBER = 0;
export const DEFAULT_STRING = "";
export const DEFAULT_BOOLEAN = false;

export type CatalogSort = {
  sortValue: string;
  sortName: string;
};

export type CatalogFilterByParam = {
  filterByParamValue: string;
  filterByParamName: string;
};

export type PropertyIn = {
  property_id?: number;
  property_name?: string;
  values?: string[];
};

export type Property = {
  propertyID: number;
  propertyName?: string;
  propertyValues: string[];
};

export type ColorIn = {
  color_id?: number;
  color_name?: string;
};

export type Color = {
  colorID: number;
  colorName: string;
};

export type CatalogFiltersIn = {
  productOnlyInStock?: boolean;
  productPriceStart?: number;
  productPriceEnd?: number;
  properties?: Property[];
  colors?: number[];
};

export type CatalogFilters = {
  productOnlyInStock: boolean;
  productPriceStart: number;
  productPriceEnd: number;
  properties: Property[];
  colors: number[];
};

export type CatalogFilterSortOut = {
  filters: {
    categoryID: number;
    productOnlyInStock: boolean;
    productPriceStart?: number;
    productPriceEnd?: number;
    properties: {
      propertyID: number;
      propertyValues: string[];
    }[];
    colors: number[];
  };
  sort_by: string;
  filter_by_params: string;
};

export function GetCatalogFilterSortOut(
  _filters: CatalogFilters,
  categoryID: number,
  sort: string,
  filterByParams: string,
): CatalogFilterSortOut {
  const filters = structuredClone(_filters);
  const obj: CatalogFilterSortOut = {
    filters: {
      categoryID: categoryID,
      productOnlyInStock: filters.productOnlyInStock,
      properties: filters.properties.filter(
        (property) => property.propertyValues.length > 0,
      ),
      colors: filters.colors,
    },
    sort_by: sort,
    filter_by_params: filterByParams,
  };
  if (filters.productPriceEnd > 0) {
    obj.filters.productPriceEnd = filters.productPriceEnd;
  }
  if (filters.productPriceStart > 0) {
    obj.filters.productPriceStart = filters.productPriceStart;
  }
  return obj;
}

export function NewCatalogFilters(obj: CatalogFiltersIn): CatalogFilters {
  return {
    productOnlyInStock: obj.productOnlyInStock ?? DEFAULT_BOOLEAN,
    productPriceStart: obj.productPriceStart ?? DEFAULT_NUMBER,
    productPriceEnd: obj.productPriceEnd ?? DEFAULT_NUMBER,
    properties: obj.properties ?? [],
    colors: obj.colors ?? [],
  };
}

export type CategoryIn = {
  category_id?: number;
  category_name?: string;
  category_parent_id?: number;
  [key: string]: any;
};

export type Category = {
  categoryID: number;
  categoryName: string;
  categoryParentID: number;
};

export function NewCategory(obj: CategoryIn): Category {
  return {
    categoryID: obj.category_id ?? DEFAULT_NUMBER,
    categoryName: obj.category_name ?? DEFAULT_STRING,
    categoryParentID: obj.category_parent_id ?? DEFAULT_NUMBER,
  };
}

export type ProductCatalogIn = {
  product_id?: number;
  category_id?: number;
  product_name?: string;
  product_measured_in?: string;
  product_in_stock?: boolean;
  product_price?: number;
  product_new?: boolean;
  product_hit?: boolean;
  product_promotion?: boolean;
  product_percent_promotion?: number;
  product_new_price?: number;
  product_in_wishlist?: boolean;
};

export type ProductCatalog = {
  productID: number;
  categoryID: number;
  productName: string;
  productMeasuredIn: string;
  productInStock: boolean;
  productPrice: number;
  productNew: boolean;
  productHit: boolean;
  productPromotion: boolean;
  productPercentPromotion: number;
  productNewPrice: number;
  productInWishlist: boolean;
};

export function NewProductCatalogList(
  objs: ProductCatalogIn[],
): ProductCatalog[] {
  const productCatalogList: ProductCatalog[] = [];
  for (const i of objs ?? []) {
    productCatalogList.push({
      productHit: i.product_hit ?? DEFAULT_BOOLEAN,
      productInStock: i.product_in_stock ?? DEFAULT_BOOLEAN,
      productInWishlist: i.product_in_wishlist ?? DEFAULT_BOOLEAN,
      productNew: i.product_new ?? DEFAULT_BOOLEAN,
      productNewPrice: i.product_new_price ?? DEFAULT_NUMBER,
      productPercentPromotion: i.product_percent_promotion ?? DEFAULT_NUMBER,
      productPrice: i.product_price ?? DEFAULT_NUMBER,
      productPromotion: i.product_promotion ?? DEFAULT_BOOLEAN,
      productMeasuredIn: i.product_measured_in ?? DEFAULT_STRING,
      productName: i.product_name ?? DEFAULT_STRING,
      productID: i.product_id ?? DEFAULT_NUMBER,
      categoryID: i.category_id ?? DEFAULT_NUMBER,
    });
  }
  return productCatalogList;
}

export type CatalogPageInfoIn = {
  number_of_products?: number;
  categories?: CategoryIn[];
  min_price?: number;
  max_price?: number;
  colors?: ColorIn[];
  properties?: PropertyIn[];
  products?: ProductCatalogIn[];
};

export type CatalogPageValues = {
  categories: Category[];
  properties: Property[];
  colors: Color[];
  productCatalogList: ProductCatalog[];
  priceMin: number;
  priceMax: number;
  productAmount: number;
};

export function GetCatalogPageValues(
  obj: CatalogPageInfoIn,
): CatalogPageValues {
  const categories: Category[] = [];
  for (const i of obj.categories ?? []) {
    categories.push(NewCategory(i));
  }

  const properties: Property[] = [];
  for (const i of obj.properties ?? []) {
    properties.push({
      propertyID: i.property_id ?? DEFAULT_NUMBER,
      propertyValues: structuredClone(i.values ?? []),
      propertyName: i.property_name ?? DEFAULT_STRING,
    });
  }

  const colors: Color[] = [];
  for (const i of obj.colors ?? []) {
    colors.push({
      colorID: i.color_id ?? DEFAULT_NUMBER,
      colorName: i.color_name ?? DEFAULT_STRING,
    });
  }

  const productCatalogList: ProductCatalog[] = NewProductCatalogList(
    obj.products ?? [],
  );

  return {
    categories: categories,
    properties: properties,
    colors: colors,
    productCatalogList: productCatalogList,
    priceMin: obj.min_price ?? DEFAULT_NUMBER,
    priceMax: obj.max_price ?? DEFAULT_NUMBER,
    productAmount: obj.number_of_products ?? DEFAULT_NUMBER,
  };
}

export type ProductInCartIn = {
  product_id?: number;
  article_id?: number;
  product_name?: string;
  product_measured_in?: string;
  product_amount?: number;
  product_amount_in_cart?: number;
  product_price?: number;
  product_percent_promotion?: number;
  product_new_price?: number;
  total_price?: number;
  product_in_wishlist?: boolean;
}

export type CartIn = {
  items?: ProductInCartIn[];
  total_products_price?: number;
  total_promotion_price?: number;
  total_cart_price?: number;
}

export type ProductInCart = {
  productID: number;
  articleID: number;
  productName: string;
  productMeasuredIn: string;
  productAmount: number;
  productAmountInCart: number;
  productPrice: number;
  productPercentPromotion: number;
  productNewPrice: number;
  totalPrice: number;
  productInWishlist: boolean;
}

export type Cart = {
  items: ProductInCart[];
  totalProductsPrice: number;
  totalPromotionPrice: number;
  totalCartPrice: number;
}

export function mapCart(obj: CartIn): Cart {
  const cart: Cart = {items: [], totalProductsPrice: obj.total_products_price ?? DEFAULT_NUMBER,
    totalPromotionPrice: obj.total_promotion_price ?? DEFAULT_NUMBER, totalCartPrice: obj.total_cart_price ?? DEFAULT_NUMBER};
  for (const i of obj.items ?? []) {
    cart.items.push({
    productID: i.product_id ?? DEFAULT_NUMBER,
    articleID: i.article_id ?? DEFAULT_NUMBER,
    productName: i.product_name ?? DEFAULT_STRING,
    productMeasuredIn: i.product_measured_in ?? DEFAULT_STRING,
    productAmount: i.product_amount ?? DEFAULT_NUMBER,
    productAmountInCart: i.product_amount_in_cart ?? DEFAULT_NUMBER,
    productPrice: i.product_price ?? DEFAULT_NUMBER,
    productPercentPromotion: i.product_percent_promotion ?? DEFAULT_NUMBER,
    productNewPrice: i.product_new_price ?? DEFAULT_NUMBER,
    totalPrice: i.total_price ?? DEFAULT_NUMBER,
    productInWishlist: i.product_in_wishlist ?? DEFAULT_BOOLEAN
    });
  }
  return cart;
}

export type ResponseInfo = {
  status: number;
  detail: string;
}

export class UserInfo {
  user_id: number;
  email: string;
  name: string | null;
  surname: string | null;
  number: string | null;
  role: string;

  constructor(data: any) {
      this.user_id = data?.user_id ?? 0;
      this.email = data?.email ?? "";
      this.name = data?.name ?? null;
      this.surname = data?.surname ?? null;
      this.number = data?.number ?? null;
      this.role = data?.role ?? "";
  }
}

export type ProductForPageIn = {
  categories?: CategoryIn[];
  article_id?: number;
  color_id?: number;
  color_name?: string;
  product_name?: string;
  product_description?: string;
  product_measured_in?: string;
  product_amount?: number;
  product_price?: number;
  product_new?: boolean;
  product_hit?: boolean;
  product_promotion?: boolean;
  product_percent_promotion?: number;
  product_new_price?: number;
  product_in_wishlist?: boolean;
  get_products_by_article?: ProductCatalogIn[];
  similar_products?: ProductCatalogIn[];
  characteristics?: {
    property_id?: number;
    property_name?: string;
    property_value?: string;
  }[];
}

export type ProductForPage = {
  categories: Category[];
  articleID: number;
  colorID: number;
  colorName: string;
  productName: string;
  productDescription: string;
  productMeasuredIn: string;
  productAmount: number;
  productPrice: number;
  productNew: boolean;
  productHit: boolean;
  productPromotion: boolean;
  productPercentPromotion: number;
  productNewPrice: number;
  productInWishlist: boolean;
  productsByArcticle: ProductCatalog[];
  productsSimilar: ProductCatalog[];
  properties: {
    propertyID: number;
    propertyName: string;
    propertyValue: string;
  }[];
}

export function NewProductForPage(obj: ProductForPageIn): ProductForPage {
  const properties = [];
  for (const i of obj.characteristics ?? []) {
    properties.push({
      propertyID: i.property_id ?? DEFAULT_NUMBER,
      propertyValue: i.property_value ?? DEFAULT_STRING,
      propertyName: i.property_name ?? DEFAULT_STRING,
    });
  }

  const categories: Category[] = [];
  for (const i of obj.categories ?? []) {
    categories.push(NewCategory(i));
  }

  return {
    categories: categories,
    colorID: obj.color_id ?? DEFAULT_NUMBER,
    colorName: obj.color_name ?? DEFAULT_STRING,
    productAmount: obj.product_amount ?? DEFAULT_NUMBER,
    productDescription: obj.product_description ?? DEFAULT_STRING,
    articleID: obj.article_id ?? DEFAULT_NUMBER,
    properties: properties,
    productsByArcticle: NewProductCatalogList(obj.get_products_by_article ?? []),
    productsSimilar: NewProductCatalogList(obj.similar_products ?? []),
    productHit: obj.product_hit ?? DEFAULT_BOOLEAN,
    productInWishlist: obj.product_in_wishlist ?? DEFAULT_BOOLEAN,
    productNew: obj.product_new ?? DEFAULT_BOOLEAN,
    productNewPrice: obj.product_new_price ?? DEFAULT_NUMBER,
    productPercentPromotion: obj.product_percent_promotion ?? DEFAULT_NUMBER,
    productPrice: obj.product_price ?? DEFAULT_NUMBER,
    productPromotion: obj.product_promotion ?? DEFAULT_BOOLEAN,
    productMeasuredIn: obj.product_measured_in ?? DEFAULT_STRING,
    productName: obj.product_name ?? DEFAULT_STRING,
  };
}
