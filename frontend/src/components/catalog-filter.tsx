import { useEffect, useState } from "react";
import * as requests from "../requests.tsx";
import * as util from "../util.tsx";
import * as objects from "../objects.tsx";

type Tree = {
  val: objects.Category;
  children: TreeChildren;
};

type TreeChildren = Tree[];

function treePushCategory(tree: TreeChildren, category: objects.Category) {
  tree.push({ val: category, children: [] });
}

// return 0 - pushed, return 1 - no action
function pushToParent(tree: TreeChildren, category: objects.Category) {
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
}

function getCategoryTreeFromList(categoryList: objects.Category[]) {
  let list = structuredClone(categoryList);
  let tree: TreeChildren = [];

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
}

function HTML_PrintTree(treeObj: Tree) {
  return (
    <ul key={treeObj.val.categoryID}>
      {treeObj.val.categoryName}
      {treeObj.children.map((childTreeObj) => HTML_PrintTree(childTreeObj))}
    </ul>
  );
}

function CatalogFilter({
  initFilters,
  updateSearchParams,
}: {
  initFilters: objects.CatalogFilter;
  updateSearchParams: (newFilters: objects.CatalogFilter) => any;
}) {
  const [filters, setFilters] = useState(structuredClone(initFilters));

  const [categoryList, setCategoryList] = useState<objects.Category[]>([]);
  useEffect(() => {
    requests.GET_GetCategoryList().then((categoryList) => {
      setCategoryList(categoryList);
    });
  }, []);
  console.log(filters);
  const categoryTree = getCategoryTreeFromList(categoryList);
  return (
    <>
      <div>
        {HTML_PrintTree({
          val: objects.NewCategory({ category_name: "Категории" }),
          children: categoryTree,
        })}
      </div>
      <div style={{ display: "flex", flexDirection: "row" }}>
        <input
          type="number"
          value={filters.productPriceStart}
          onChange={(e) => {
            setFilters({
              ...filters,
              productPriceStart: util.Num(e.target.value),
            });
          }}
        />
        <input
          type="number"
          value={filters.productPriceEnd}
          onChange={(e) => {
            setFilters({
              ...filters,
              productPriceEnd: util.Num(e.target.value),
            });
          }}
        />
      </div>
    </>
  );
}

export default CatalogFilter;
