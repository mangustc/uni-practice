import PropTypes from "prop-types";
import { useEffect, useState } from "react";
import * as requests from "../requests";
import * as util from "../util";

const treePushCategory = function (tree, category) {
  tree.push({ val: category, children: [] });
};

// return 0 - pushed, return 1 - no action
const pushToParent = function (tree, category) {
  for (let i of tree) {
    if (i.val.categoryID == category.categoryParentID) {
      treePushCategory(i.children, category);
      return 0;
    }
    let code = pushToParent(i.children, category);
    if (code == 0) {
      return 0;
    }
  }
  return 1;
};

const getCategoryTreeFromList = function (categoryList) {
  let list = util.DeepClone(categoryList);
  let tree = [];

  const listLen = list.length;
  let addedAmount = 0;
  while (addedAmount < listLen) {
    for (let i of list) {
      if (i.categoryParentID == 0) {
        treePushCategory(tree, i);
        addedAmount++;
        continue;
      }
      const code = pushToParent(tree, i);
      if (code == 0) {
        addedAmount++;
      }
    }
  }

  return tree;
};

const pushAllChildrenToList = function (list, treeObj) {
  list.push(treeObj.val);
  for (let i of treeObj.children) {
    pushAllChildrenToList(list, i);
  }
};

const HTML_PrintTree = function (treeObj) {
  return (
    <ul key={treeObj.val ? treeObj.val.categoryID : "main"}>
      {treeObj.val ? treeObj.val.categoryName : "Категории"}
      {treeObj.children.map((childTreeObj) => HTML_PrintTree(childTreeObj))}
    </ul>
  );
};

const CatalogFilter = function ({ initFilters, updateSearchParams }) {
  const [filters, setFilters] = useState(util.DeepClone(initFilters));
  const setFiltersAttr = util.GetSetObjectAttrtibuteFunc(setFilters);

  const [categoryList, setCategoryList] = useState([]);
  useEffect(() => {
    requests.GET_GetCategoryList().then((categoryList) => {
      setCategoryList(categoryList);
    });
  }, []);
  const categoryTree = getCategoryTreeFromList(categoryList);
  return (
    <>
      <div>{HTML_PrintTree({ val: null, children: categoryTree })}</div>
      <div style={{ display: "flex", flexDirection: "row" }}>
        <input
          type="number"
          value={filters.articlePriceStart}
          onChange={(e) => {
            setFiltersAttr("articlePriceStart", e.target.value);
          }}
        />
        <input
          type="number"
          value={filters.articlePriceEnd}
          onChange={(e) => setFiltersAttr("articlePriceEnd", e.target.value)}
        />
      </div>
    </>
  );
};

CatalogFilter.propTypes = {
  updateSearchParams: PropTypes.func,
  initFilters: PropTypes.object,
};

export default CatalogFilter;
