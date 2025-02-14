import { useSearchParams } from "react-router-dom";
import * as objects from "../objects";
import CatalogFilter from "../components/catalog-filter";

export const Catalog = function () {
  const [searchParams, setSearchParams] = useSearchParams();
  const updateSearchParams = function (newFilters: objects.CatalogFilter) {
    const newSearchParams = new URLSearchParams();
    for (let filter in newFilters) {
      // @ts-expect-error
      newSearchParams.set(filter, newFilters[filter]);
    }
    setSearchParams(newSearchParams);
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
