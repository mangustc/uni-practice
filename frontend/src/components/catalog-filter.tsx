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

function CatalogFilter({
  initFilters,
  updateSearchParams,
}: {
  initFilters: objects.CatalogFilters;
  updateSearchParams: (newFilters: objects.CatalogFilters) => any;
}) {
  function JSX_PrintTree(treeObj: Tree) {
    return (
      <ul key={treeObj.val.categoryID}>
        <span
          onClick={() => {
            const newFilters: objects.CatalogFilters = {
              ...initFilters,
              categoryID: util.Num(treeObj.val.categoryID),
            };
            updateSearchParams(newFilters);
            setFilters(newFilters);
          }}
          style={{ cursor: "pointer" }}
        >
          {treeObj.val.categoryName}
        </span>
        {treeObj.children.map((childTreeObj) => JSX_PrintTree(childTreeObj))}
      </ul>
    );
  }
  const [filters, setFilters] = useState(structuredClone(initFilters));

  const [categoryList, setCategoryList] = useState<objects.Category[]>([]);
  useEffect(() => {
    requests.GET_GetCategoryList().then((categoryList) => {
      setCategoryList(categoryList);
    });
  }, []);
  const categoryTree = getCategoryTreeFromList(categoryList);
  return (
    <div style={{ display: "flex", flexDirection: "column" }}>
      <div>
        {JSX_PrintTree({
          val: objects.NewCategory({ category_name: "Категории" }),
          children: categoryTree,
        })}
      </div>
      <div style={{ display: "flex", flexDirection: "row", gap: "20px" }}>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
          }}
        >
          <label
            onClick={() => {
              setFilters({
                ...filters,
                productOnlyInStock: false,
              });
            }}
          >
            Все товары
          </label>
          <input
            type="checkbox"
            checked={!filters.productOnlyInStock}
            onChange={(e) => {
              if (e.target.checked)
                setFilters({
                  ...filters,
                  productOnlyInStock: false,
                });
            }}
          />
        </div>
        <div style={{ display: "flex", flexDirection: "column" }}>
          <label
            onClick={() => {
              setFilters({
                ...filters,
                productOnlyInStock: true,
              });
            }}
          >
            В наличии
          </label>
          <input
            type="checkbox"
            checked={filters.productOnlyInStock}
            onChange={(e) => {
              if (e.target.checked)
                setFilters({
                  ...filters,
                  productOnlyInStock: true,
                });
            }}
          />
        </div>
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
      <button onClick={() => updateSearchParams(structuredClone(filters))}>
        Применить фильтры
      </button>
    </div>
  );
}

export default CatalogFilter;
