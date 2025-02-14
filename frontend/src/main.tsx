// import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Root from "./routes/root";
import "./index.css";
import ErrorPage from "./error-page";
import { Catalog } from "./routes/catalog";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "catalog",
        element: <Catalog />,
      },
    ],
  },
]);

const root = ReactDOM.createRoot(document.getElementById("root")!);
root.render(<RouterProvider router={router} />);
