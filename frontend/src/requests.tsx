import * as objects from "./objects.tsx";

const BACKEND_URL: string = import.meta.env.VITE_BACKEND_URL;
const HEADER_JSON = {
  "Content-Type": "application/json",
  accept: "application/json",
};

export async function GET_GetCategoryList() {
  // let response = await fetch(BACKEND_URL + "/dish/get_dishes", {
  //   method: "POST",
  //   headers: HEADER_JSON,
  //   credentials: "include",
  // });
  return [
    objects.NewCategory({
      category_id: 1,
      category_name: "test",
    }),
    objects.NewCategory({
      category_id: 2,
      category_name: "test2",
    }),
    objects.NewCategory({
      category_id: 3,
      category_name: "test3",
      category_parent_id: 1,
    }),
    objects.NewCategory({
      category_id: 4,
      category_name: "test4",
      category_parent_id: 1,
    }),
    objects.NewCategory({
      category_id: 5,
      category_name: "test6",
      category_parent_id: 1,
    }),
    objects.NewCategory({
      category_id: 6,
      category_name: "testunder",
      category_parent_id: 3,
    }),
  ];
}
