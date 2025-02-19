import { createSearchParams, useSearchParams } from "react-router-dom";
import * as objects from "../objects";
import * as requests from "../requests";
import CatalogFilter from "../components/catalog-filter";
import { useEffect, useState } from "react";

export const Catalog = function () {
  const [searchParams, setSearchParams] = useSearchParams();
  const [currentValues, setCurrentValues] = useState<{
    categories: objects.Category[];
    properties: objects.Property[];
    colors: objects.Color[];
    filters: objects.CatalogFilters;
  }>({
    categories: [],
    properties: [],
    colors: [],
    filters: objects.NewCatalogFilters(
      JSON.parse(searchParams.get("currentFilters") ?? "{}"),
    ),
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

  function updateSearchParams(newFilters: objects.CatalogFilters) {
    setCurrentValues({ ...currentValues, filters: newFilters });
    setSearchParams(
      createSearchParams({ currentFilters: JSON.stringify(newFilters) }),
    );
  }

  return (
    <>
      <div style={{ display: "flex", flexDirection: "row" }}>
        <CatalogFilter
          initFilters={currentValues.filters}
          updateSearchParams={updateSearchParams}
          categories={currentValues.categories}
          properties={currentValues.properties}
          colors={currentValues.colors}
        />
        <textarea
          value={
            "filtering values:\n" +
            JSON.stringify(currentValues.filters, null, 2)
          }
          readOnly
        ></textarea>
      </div>
    </>
  );
};
