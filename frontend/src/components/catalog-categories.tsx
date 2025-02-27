import * as objects from "../objects";

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

function getCategoryTreeFromList(categories: objects.Category[]) {
  let list = structuredClone(categories);
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

export function CatalogCategories({
  currentCategoryID,
  updateCategoryID,
  categories,
}: {
  currentCategoryID: number;
  updateCategoryID: (newCategoryID: number) => void;
  categories: objects.Category[];
}) {
  function JSX_PrintTree(treeObj: Tree, depth: number) {
    return (
      <div key={treeObj.val.categoryID} style={{display: "flex", flexDirection: "column", gap: "6px"}}>
        <span
          onClick={
            treeObj.val.categoryID != 0
              ? () => updateCategoryID(treeObj.val.categoryID)
              : () => {}
          }
          className={ depth <= 1 
            ? (currentCategoryID == treeObj.val.categoryID
              ? "catalog-categories__root-category text-link-active"
              : "catalog-categories__root-category")
            : (currentCategoryID == treeObj.val.categoryID
              ? "catalog-categories__subcategory text-link-active"
              : "catalog-categories__subcategory")
          }
        >
            {treeObj.val.categoryID == 0 ? (<h5>{treeObj.val.categoryName}</h5>) : treeObj.val.categoryName}
        </span>
        <div style={{marginLeft: `${depth*14}px`}}>
          {treeObj.children.map((childTreeObj) => JSX_PrintTree(childTreeObj, depth + 1))}
        </div>
      </div>
    );
  }

  const categoryTree = getCategoryTreeFromList(categories);
  return (
    <div className="catalog-categories-container">
      <div>
        {JSX_PrintTree({
          val: objects.NewCategory({ category_name: "Категории" }),
          children: categoryTree,
        }, 0)}
      </div>
    </div>
  );
}
