import { createSearchParams, useSearchParams } from "react-router-dom";
import * as objects from "../objects";
import * as requests from "../requests";
import CatalogFilter from "../components/catalog-filter";
import { useEffect, useState } from "react";
import CatalogSort from "../components/catalog-sort";
import { CatalogCategories } from "../components/catalog-categories";

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
    currentSort: searchParams.get("currentSort") ?? "price",
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

  function updateSearchParams(
    newFilters?: objects.CatalogFilters,
    newSort?: string,
    newCategoryID?: number,
  ) {
    const _newFilters = newFilters ?? currentValues.currentFilters;
    const _newSort = newSort ?? currentValues.currentSort;
    const _newCategoryID = newCategoryID ?? currentValues.currentCategoryID;
    setCurrentValues({
      ...currentValues,
      currentFilters: _newFilters,
      currentSort: _newSort,
      currentCategoryID: _newCategoryID,
    });
    setSearchParams(
      createSearchParams({
        currentFilters: JSON.stringify(_newFilters),
        currentSort: _newSort,
        currentCategoryID: String(_newCategoryID),
      }),
    );
  }

  return (
    <>
      <div style={{ display: "flex", flexDirection: "row" }}>
        <CatalogCategories
          categories={currentValues.categories}
          currentCategoryID={currentValues.currentCategoryID}
          updateCategoryID={(newCategoryID: number) =>
            updateSearchParams(undefined, undefined, newCategoryID)
          }
        />
        <CatalogFilter
          initFilters={currentValues.currentFilters}
          updateFilters={(newFilters: objects.CatalogFilters) =>
            updateSearchParams(newFilters, undefined, undefined)
          }
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
          updateSort={(newSort: string) =>
            updateSearchParams(undefined, newSort, undefined)
          }
        />
      </div>
    </>
  );
};
