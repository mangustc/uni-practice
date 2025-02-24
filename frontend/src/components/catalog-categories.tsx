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
  function JSX_PrintTree(treeObj: Tree) {
    return (
      <ul key={treeObj.val.categoryID}>
        <span
          onClick={
            treeObj.val.categoryID != 0
              ? () => updateCategoryID(treeObj.val.categoryID)
              : () => {}
          }
          style={{ cursor: "pointer" }}
        >
          {currentCategoryID == treeObj.val.categoryID ? (
            <h6>{treeObj.val.categoryName}</h6>
          ) : (
            treeObj.val.categoryName
          )}
        </span>
        {treeObj.children.map((childTreeObj) => JSX_PrintTree(childTreeObj))}
      </ul>
    );
  }

  const categoryTree = getCategoryTreeFromList(categories);
  return (
    <div className="catalog-categories-container">
      <div>
        {JSX_PrintTree({
          val: objects.NewCategory({ category_name: "Категории" }),
          children: categoryTree,
        })}
      </div>
    </div>
  );
}
