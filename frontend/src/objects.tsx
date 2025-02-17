const DEFAULT_NUMBER = 0;
const DEFAULT_STRING = "";
const DEFAULT_BOOLEAN = false;

export type CatalogFiltersIn = {
  categoryID?: number;
  productOnlyInStock?: boolean;
  productPriceStart?: number;
  productPriceEnd?: number;
  productColors?: string[];
  productWidth?: string[];
  productDensity?: string[];
  productConsist?: string[];
  productCountry?: string[];
  [key: string]: any;
};

export type CatalogFilters = {
  categoryID: number;
  productOnlyInStock: boolean;
  productPriceStart: number;
  productPriceEnd: number;
  productColors: string[];
  productWidth: string[];
  productDensity: string[];
  productConsist: string[];
  productCountry: string[];
};

export function NewCatalogFilters(obj: CatalogFiltersIn): CatalogFilters {
  return {
    categoryID: obj.categoryID ?? DEFAULT_NUMBER,
    productOnlyInStock: obj.productOnlyInStock ?? DEFAULT_BOOLEAN,
    productPriceStart: obj.productPriceStart ?? DEFAULT_NUMBER,
    productPriceEnd: obj.productPriceEnd ?? DEFAULT_NUMBER,
    productColors: obj.productColors ?? [],
    productWidth: obj.productWidth ?? [],
    productDensity: obj.productDensity ?? [],
    productConsist: obj.productConsist ?? [],
    productCountry: obj.productCountry ?? [],
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
