function num(obj, defaultValue) {
  const out = Number(obj);
  return out ? out : defaultValue ? defaultValue : 0;
}

function bool(obj, defaultValue) {
  const out = Boolean(obj);
  return out ? out : defaultValue ? defaultValue : false;
}

function str(obj, defaultValue) {
  const out = Number(obj);
  return out ? out : defaultValue ? defaultValue : "";
}

function arr(array, convFunc) {
  let newArray = [];
  let iterArray = array ? array : [];
  for (let i of iterArray) {
    newArray.push(convFunc(i));
  }
  return newArray;
}

export const NewCatalogFilters = function (obj) {
  obj = obj ? obj : {};
  return {
    categoryID: num(obj.categoryID),
    productsOnlyInStock: bool(obj.productsOnlyInStock),
    articlePriceStart: bool(obj.productPriceStart),
    articlePriceEnd: bool(obj.productPriceEnd),
    productColors: arr(obj.productColors, str),
    productWidth: arr(obj.productWidth, str),
    productDensity: arr(obj.productDensity, str),
    productConsist: arr(obj.productConsist, str),
    productCountry: arr(obj.productCountry, str),
  };
};
