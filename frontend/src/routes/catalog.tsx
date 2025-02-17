import { useSearchParams } from "react-router-dom";
import * as objects from "../objects";
import * as util from "../util";
import CatalogFilter from "../components/catalog-filter";

export const Catalog = function () {
  const [searchParams, setSearchParams] = useSearchParams();
  const updateSearchParams = function (newFilters: objects.CatalogFilters) {
    const newSearchParams = new URLSearchParams();
    for (let filter in newFilters) {
      // @ts-expect-error
      newSearchParams.set(filter, newFilters[filter]);
    }
    setSearchParams(newSearchParams);
  };

  const catalogFilters = objects.NewCatalogFilters({
    categoryID: JSON.parse(searchParams.get("categoryID") as string),
    productOnlyInStock: JSON.parse(
      searchParams.get("productOnlyInStock") as string,
    ),
    productPriceStart: JSON.parse(
      searchParams.get("productPriceStart") as string,
    ),
    productPriceEnd: JSON.parse(searchParams.get("productPriceEnd") as string),
    productColors: util.ArrFromURLSearchParam(
      searchParams.get("productColors") ?? "",
    ),
    productWidth: util.ArrFromURLSearchParam(
      searchParams.get("productWidth") ?? "",
    ),
    productDensity: util.ArrFromURLSearchParam(
      searchParams.get("productDensity") ?? "",
    ),
    productConsist: util.ArrFromURLSearchParam(
      searchParams.get("productConsist") ?? "",
    ),
    productCountry: util.ArrFromURLSearchParam(
      searchParams.get("productCountry") ?? "",
    ),
  });
  console.log(catalogFilters);
  return (
    <>
      <div style={{ display: "flex", flexDirection: "row" }}>
        <CatalogFilter
          initFilters={catalogFilters}
          updateSearchParams={updateSearchParams}
        />
        <textarea
          value={
            "filtering values:\n" + JSON.stringify(catalogFilters, null, 2)
          }
          readOnly
        ></textarea>
      </div>
    </>
  );
};
