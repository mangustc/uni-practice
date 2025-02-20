import { createSearchParams, useSearchParams } from "react-router-dom";
import * as objects from "../objects";
import * as requests from "../requests";
import CatalogFilter from "../components/catalog-filter";
import { useEffect, useState } from "react";
import CatalogSort from "../components/catalog-sort";

export const Catalog = function () {
  const [searchParams, setSearchParams] = useSearchParams();
  const [currentValues, setCurrentValues] = useState<{
    categories: objects.Category[];
    properties: objects.Property[];
    colors: objects.Color[];
    sorts: objects.CatalogSort[];
    currentFilters: objects.CatalogFilters;
    currentSort: string;
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
    currentFilters: objects.NewCatalogFilters(
      JSON.parse(searchParams.get("currentFilters") ?? "{}"),
    ),
    currentSort: searchParams.get("currentSort") ?? "price",
  });

  useEffect(() => {
    requests.GET_GetCategoryList().then((categories) => {
      setCurrentValues({
        ...currentValues,
        categories: categories,
        colors: [
          { colorID: 1, colorName: "Green" },
          { colorID: 2, colorName: "GREEEN" },
        ],
        properties: [
          {
            propertyID: 1,
            propertyName: "Shirina",
            propertyValues: ["long", "short", "extra long"],
          },
          {
            propertyID: 2,
            propertyName: "material",
            propertyValues: ["gold", "silver", "copper"],
          },
        ],
      });
    });
  }, []);

  function updateSearchParams(
    newFilters?: objects.CatalogFilters,
    newSort?: string,
  ) {
    const _newFilters = newFilters ?? currentValues.currentFilters;
    const _newSort = newSort ?? currentValues.currentSort;
    setCurrentValues({
      ...currentValues,
      currentFilters: _newFilters,
      currentSort: _newSort,
    });
    setSearchParams(
      createSearchParams({
        currentFilters: JSON.stringify(_newFilters),
        currentSort: _newSort,
      }),
    );
  }

  return (
    <>
      <div style={{ display: "flex", flexDirection: "row" }}>
        <CatalogFilter
          initFilters={currentValues.currentFilters}
          updateFilters={(newFilters: objects.CatalogFilters) =>
            updateSearchParams(newFilters, undefined)
          }
          categories={currentValues.categories}
          properties={currentValues.properties}
          colors={currentValues.colors}
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
            updateSearchParams(undefined, newSort)
          }
        />
      </div>
    </>
  );
};
