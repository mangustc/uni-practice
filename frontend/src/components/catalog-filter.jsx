import PropTypes from "prop-types";
import { useState } from "react";

const CatalogFilter = function ({ initFilters, updateSearchParams }) {
  const [filters, setFilters] = useState(initFilters);
  return <></>;
};

CatalogFilter.propTypes = {
  updateSearchParams: PropTypes.func,
  initFilters: PropTypes.object,
};

export default CatalogFilter;
