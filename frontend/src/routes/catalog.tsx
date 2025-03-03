import { createSearchParams, useSearchParams } from "react-router-dom";
import * as objects from "../objects";
import * as requests from "../requests";
import CatalogFilter from "../components/catalog-filter";
import { useEffect, useState } from "react";
import CatalogSort from "../components/catalog-sort";
import { CatalogCategories } from "../components/catalog-categories";
import { CatalogProducts } from "../components/catalog-products";

const DEFAULT_SORT = "price";
const DEFAULT_FILTER_BY_PARAM = "none";

function newCatalogSearchParams(obj: {
  currentFilters: objects.CatalogFilters,
  currentSort: string,
  currentCategoryID: number,
  currentFilterByParam: string,
}): URLSearchParams {
  return createSearchParams({
    currentFilters: JSON.stringify(obj.currentFilters),
    currentSort: obj.currentSort,
    currentCategoryID: String(obj.currentCategoryID),
    currentFilterByParam: obj.currentFilterByParam
  });
}

function getCatalogSearchParams(searchParams: URLSearchParams) {
  return {
    currentFilterByParam: searchParams.get("currentFilterByParam") ?? DEFAULT_FILTER_BY_PARAM,
    currentCategoryID: searchParams.get("currentCategoryID")
      ? Number(searchParams.get("currentCategoryID"))
      : 0,
    currentFilters: objects.NewCatalogFilters(
      JSON.parse(searchParams.get("currentFilters") ?? "{}"),
    ),
    currentSort: searchParams.get("currentSort") ?? DEFAULT_SORT,
  }
}

export const Catalog = function () {
  const [searchParams, setSearchParams] = useSearchParams();
  const catalogSearchParams = getCatalogSearchParams(searchParams);
  const [currentValues, setCurrentValues] = useState<{
    currentCategoryID: number;
    categories: objects.Category[];
    properties: objects.Property[];
    colors: objects.Color[];
    sorts: objects.CatalogSort[];
    currentFilters: objects.CatalogFilters;
    currentSort: string;
    currentFilterByParam: string;
    priceMin: number;
    priceMax: number;
    productAmount: number;
    filterByParams: objects.CatalogFilterByParam[];
  }>({
    categories: [],
    properties: [],
    colors: [],
    sorts: [
      {
        sortValue: "price",
        sortName: "По возрастанию цены",
      },
      {
        sortValue: "-price",
        sortName: "По убыванию цены",
      },
      {
        sortValue: "name",
        sortName: "От А до Я",
      },
      {
        sortValue: "-name",
        sortName: "От Я до А",
      },
    ],
    filterByParams: [
      {
        filterByParamValue: "new",
        filterByParamName: "Новинки",
      },
      {
        filterByParamValue: "hit",
        filterByParamName: "Хиты",
      },
      {
        filterByParamValue: "promotion",
        filterByParamName: "Акция",
      },
      {
        filterByParamValue: "none",
        filterByParamName: "-",
      },
    ],
    currentFilterByParam: catalogSearchParams.currentFilterByParam,
    priceMin: 0,
    priceMax: 0,
    productAmount: 0,
    currentCategoryID: catalogSearchParams.currentCategoryID,
    currentFilters: catalogSearchParams.currentFilters,
    currentSort: catalogSearchParams.currentSort,
  });
  const [products, setProducts] = useState<objects.ProductCatalog[]>([]);
  const [tempFilters, setTempFilters] = useState(currentValues.currentFilters);

  // used for filters on the same category
  function updateSearch(
    newFilters: objects.CatalogFilters,
    newSort: string,
    newFilterByParam: string,
  ) {
    setCurrentValues({
      ...currentValues,
      currentFilters: newFilters,
      currentFilterByParam: newFilterByParam,
      currentSort: newSort,
    });
    setSearchParams(
      newCatalogSearchParams({
        currentFilters: newFilters,
        currentSort: newSort,
        currentFilterByParam: newFilterByParam,
        currentCategoryID: currentValues.currentCategoryID,
      }),
    );
    requests
      .POST_GetProductsByCategory(
        objects.GetCatalogFilterSortOut(
          newFilters,
          currentValues.currentCategoryID,
          newSort,
          newFilterByParam,
        ),
      )
      .then((obj2) => {
        setProducts(obj2);
      });
  }

  useEffect(() => {
    requests
      .GET_GetInfoForCatalogPage(currentValues.currentCategoryID)
      .then((obj) => {
        setCurrentValues({
          ...currentValues,
          categories: obj.categories,
          colors: obj.colors,
          properties: obj.properties,
          priceMin: obj.priceMin,
          priceMax: obj.priceMax,
        });
        requests
          .POST_GetProductsByCategory(
            objects.GetCatalogFilterSortOut(
              currentValues.currentFilters,
              currentValues.currentCategoryID,
              currentValues.currentSort,
              currentValues.currentFilterByParam,
            ),
          )
          .then((obj2) => {
            setProducts(obj2);
          });
      });
  }, []);

  function updateFilters(newFilters: objects.CatalogFilters) {
    updateSearch(
      newFilters,
      currentValues.currentSort,
      currentValues.currentFilterByParam,
    );
  }
  function updateCategoryID(newCategoryID: number) {
    requests.GET_GetInfoForCatalogPage(newCategoryID).then((obj) => {
      const newFilters = objects.NewCatalogFilters({});
      const newSort = DEFAULT_SORT;
      const newFilterByParam = DEFAULT_FILTER_BY_PARAM;
      setTempFilters(objects.NewCatalogFilters({}));
      setCurrentValues({
        ...currentValues,
        currentCategoryID: newCategoryID,
        currentFilters: newFilters,
        currentSort: newSort,
        currentFilterByParam: newFilterByParam,
        categories: obj.categories,
        colors: obj.colors,
        properties: obj.properties,
        priceMin: obj.priceMin,
        priceMax: obj.priceMax,
      });
      setProducts(obj.productCatalogList);
      setSearchParams(
        newCatalogSearchParams({
          currentFilters: newFilters,
          currentSort: newSort,
          currentCategoryID: newCategoryID,
          currentFilterByParam: newFilterByParam,
        }),
      );
    });
  }
  function updateSort(newSort: string, newFilterByParam: string) {
    updateSearch(currentValues.currentFilters, newSort, newFilterByParam);
  }

  return (
    <>
    <div className="screen-container">
      <div className="categories-page-container">
        <div className="catalog-container">
        <CatalogCategories
          categories={currentValues.categories}
          currentCategoryID={currentValues.currentCategoryID}
          updateCategoryID={updateCategoryID}
        />
        <CatalogFilter
          filters={tempFilters}
          setFilters={setTempFilters}
          updateFilters={updateFilters}
          properties={currentValues.properties}
          colors={currentValues.colors}
          priceMax={currentValues.priceMax}
          priceMin={currentValues.priceMin}
        />
        </div>
        <div className="catalog-products-container">
          <div className="catalog-sort-line">
            <CatalogSort
              currentSort={currentValues.currentSort}
              currentFilterByParam={currentValues.currentFilterByParam}
              filterByParams={currentValues.filterByParams}
              sorts={currentValues.sorts}
              updateSort={updateSort}
            />
          </div>
          <CatalogProducts products={products} />
        </div>
      </div>
      </div>
    </>
  );
};
