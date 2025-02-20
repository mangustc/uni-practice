import { createSearchParams, useSearchParams } from "react-router-dom";
import * as objects from "../objects";
import * as requests from "../requests";
import CatalogFilter from "../components/catalog-filter";
import { useEffect, useState } from "react";
import CatalogSort from "../components/catalog-sort";
import { CatalogCategories } from "../components/catalog-categories";

const DEFAULT_SORT = "price";

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
    priceMin: number;
    priceMax: number;
    productAmount: number;
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
        currentCategoryID: String(currentValues.currentCategoryID),
      }),
    );
  }
  function updateCategoryID(newCategoryID: number) {
    setCurrentValues({
      ...currentValues,
      currentCategoryID: newCategoryID,
    });
    setSearchParams(
      createSearchParams({
        currentFilters: JSON.stringify(currentValues.currentFilters),
        currentSort: currentValues.currentSort,
        currentCategoryID: String(newCategoryID),
      }),
    );
  }
  function updateSort(newSort: string) {
    setCurrentValues({
      ...currentValues,
      currentSort: newSort,
    });
    setSearchParams(
      createSearchParams({
        currentFilters: JSON.stringify(currentValues.currentFilters),
        currentSort: newSort,
        currentCategoryID: String(currentValues.currentCategoryID),
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
          initFilters={currentValues.currentFilters}
          updateFilters={updateFilters}
          properties={currentValues.properties}
          colors={currentValues.colors}
          priceMax={currentValues.priceMax}
          priceMin={currentValues.priceMin}
        />
        <textarea
          value={
            "filtering values:\n" +
            JSON.stringify(currentValues.currentFilters, null, 2) +
            "\nsorting value: " +
            JSON.stringify(currentValues.currentSort, null, 2)
          }
          readOnly
        ></textarea>
        <CatalogSort
          currentSort={currentValues.currentSort}
          sorts={currentValues.sorts}
          updateSort={updateSort}
        />
      </div>
    </>
  );
};
