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

export const Catalog = function () {
  const [searchParams, setSearchParams] = useSearchParams();
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
    currentFilterByParam: DEFAULT_FILTER_BY_PARAM,
    priceMin: 0,
    priceMax: 0,
    productAmount: 0,
    currentCategoryID: searchParams.get("currentCategoryID")
      ? Number(searchParams.get("currentCategoryID"))
      : 0,
    currentFilters: objects.NewCatalogFilters(
      JSON.parse(searchParams.get("currentFilters") ?? "{}"),
    ),
    currentSort: searchParams.get("currentSort") ?? DEFAULT_SORT,
  });
  const [products, setProducts] = useState<objects.ProductCatalog[]>([]);
  const [tempFilters, setTempFilters] = useState(currentValues.currentFilters);

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
        setProducts(obj.productCatalogList);
      });
  }, []);

  function updateFilters(newFilters: objects.CatalogFilters) {
    setCurrentValues({
      ...currentValues,
      currentFilters: newFilters,
    });
    setSearchParams(
      createSearchParams({
        currentFilters: JSON.stringify(newFilters),
        currentSort: currentValues.currentSort,
        currentFilterByParam: currentValues.currentFilterByParam,
        currentCategoryID: String(currentValues.currentCategoryID),
      }),
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
        categories: obj.categories,
        colors: obj.colors,
        properties: obj.properties,
        priceMin: obj.priceMin,
        priceMax: obj.priceMax,
      });
      setProducts(obj.productCatalogList);
      setSearchParams(
        createSearchParams({
          currentFilters: JSON.stringify(newFilters),
          currentSort: newSort,
          currentCategoryID: String(newCategoryID),
          currentFilterByParam: newFilterByParam,
        }),
      );
    });
  }
  function updateSort(newSort: string, newFilterByParam: string) {
    setCurrentValues({
      ...currentValues,
      currentSort: newSort,
      currentFilterByParam: newFilterByParam,
    });
    setSearchParams(
      createSearchParams({
        currentFilters: JSON.stringify(currentValues.currentFilters),
        currentSort: newSort,
        currentCategoryID: String(currentValues.currentCategoryID),
        currentFilterByParam: newFilterByParam,
      }),
    );
  }

  return (
    <>
      <div style={{ display: "flex", flexDirection: "row" }}>
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
        <textarea
          value={
            "categoryID value: " +
            JSON.stringify(currentValues.currentCategoryID, null, 2) +
            "\nfiltering values:\n" +
            JSON.stringify(currentValues.currentFilters, null, 2) +
            "\nsorting value: " +
            JSON.stringify(currentValues.currentSort, null, 2) +
            "\nfilterByParam value: " +
            JSON.stringify(currentValues.currentFilterByParam, null, 2)
          }
          readOnly
        ></textarea>
        <CatalogSort
          currentSort={currentValues.currentSort}
          currentFilterByParam={currentValues.currentFilterByParam}
          filterByParams={currentValues.filterByParams}
          sorts={currentValues.sorts}
          updateSort={updateSort}
        />
        <CatalogProducts products={products} />
      </div>
    </>
  );
};
