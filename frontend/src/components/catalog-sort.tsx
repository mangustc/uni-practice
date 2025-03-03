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
      <div style={{display: "flex", flexDirection: "row", alignItems: "center"}}>
        <span className="hover-dropdown-caption">Сортировка:</span>
        <div className="hover-dropdown-container">
          <span className="hover-dropdown-caption hover-dropdown-button">{sorts.filter((obj) => obj.sortValue == currentSort)[0].sortName}</span>
          <div className="hover-dropdown-items">
            {sorts.map((sort) => (
              <div
                className={sort.sortValue == currentSort ? "hover-dropdown-caption hover-dropdown-item-active" : "hover-dropdown-caption"}
                onClick={(e) => updateSort(sort.sortValue, currentFilterByParam)}>
                {sort.sortName}
              </div>
            ))}
          </div>
        </div>
        <svg className="hover-dropdown-icon" width="10" height="6"><path d="M9.72.28a.943.943 0 00-1.338 0l-3.406 3.4L1.618.28A.943.943 0 00.073.591a.971.971 0 00.208 1.051l4.022 4.073A.948.948 0 004.976 6a.939.939 0 00.674-.284l4.07-4.073A.961.961 0 0010 .961.971.971 0 009.72.28z" fill="#e32636"></path></svg>
      </div>
    </>
  );
}
