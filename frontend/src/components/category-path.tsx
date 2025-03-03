import * as objects from "../objects";
export function CategoryPath({
  categories,
}: {
  categories: objects.Category[];
}) {
  return (
    <div className="category-path__container">
      <a className="category-path__category" href="/">
        Главная
      </a>
      {categories.map((category) => (
        <a
          className="category-path__category"
          href={`/catalog/?currentCategoryID=${category.categoryID}`}
        >
          {category.categoryName}
        </a>
      ))}
    </div>
  );
}
