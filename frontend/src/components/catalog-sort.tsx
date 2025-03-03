import * as objects from "../objects";

const NO_FILTER_BY_PARAM_VALUE = "none"

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
    <>
      <div className="categories-card-filter-line">
        {filterByParams.map((filterByParam) => filterByParam.filterByParamValue != NO_FILTER_BY_PARAM_VALUE ? (
          <div
            className={
              currentFilterByParam == filterByParam.filterByParamValue
                ? "categories-card-filter-active"
                : "categories-card-filter"
            }
            key={filterByParam.filterByParamValue}
            onClick={(e) => {
              currentFilterByParam == filterByParam.filterByParamValue
                ? updateSort(currentSort, NO_FILTER_BY_PARAM_VALUE)
                : updateSort(currentSort, filterByParam.filterByParamValue);
            }}
          >
            {filterByParam.filterByParamName}
          </div>
        ) : null)}
      </div>
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
      </div>
    </>
  );
}
