import { useState } from "react";
import * as objects from "../objects";

export default function CatalogSort({
  currentFilterByParam,
  filterByParams,
  currentSort,
  sorts,
  updateSort,
}: {
  currentSort: string;
  currentFilterByParam: string;
  sorts: objects.CatalogSort[];
  filterByParams: objects.CatalogFilterByParam[];
  updateSort: (newSort: string, newFilterByParam: string) => void;
}) {
  return (
    <div>
      <select
        value={currentSort}
        onChange={(e) => updateSort(e.target.value, currentFilterByParam)}
      >
        {sorts.map((sort) => (
          <option key={sort.sortValue} value={sort.sortValue}>
            {sort.sortName}
          </option>
        ))}
      </select>
      <select
        value={currentFilterByParam}
        onChange={(e) => updateSort(currentSort, e.target.value)}
      >
        {filterByParams.map((filterByParam) => (
          <option
            key={filterByParam.filterByParamValue}
            value={filterByParam.filterByParamValue}
          >
            {filterByParam.filterByParamName}
          </option>
        ))}
      </select>
    </div>
  );
}
