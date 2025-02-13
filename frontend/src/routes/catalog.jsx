import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import * as requests from "../requests";
import * as objects from "../objects";
import CatalogFilter from "../components/catalog-filter";

export const Catalog = function () {
  const [searchParams, setSearchParams] = useSearchParams();
  const updateSearchParams = function (newFilters) {
    const newSearchParams = new URLSearchParams();
    for (let filter in newFilters) {
      newSearchParams.set(filter, newFilters[filter]);
    }
    setSearchParams(newParams);
  };

  const catalogFilters = objects.NewCatalogFilters(
    Object.fromEntries(searchParams),
  );
  return (
    <>
      <CatalogFilter
        initFilters={catalogFilters}
        updateSearchParams={updateSearchParams}
      />
    </>
  );
};
