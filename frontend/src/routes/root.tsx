import { Outlet } from "react-router-dom";
import Header from "../components/header";
import { createContext, useState } from "react";
import Cookies from "universal-cookie";
import Footer from "../components/footer";
import CategoriesPanel from "../components/categories-panel";

const cookies = new Cookies();
export const AuthContext = createContext({
  authenticated: (() => {
    return cookies.get("token") ? true : false;
  })(),
  setAuthenticated: (auth: boolean) => {},
});

export default function Root() {
  const [authenticated, setAuthenticated] = useState(
    (() => {
      return cookies.get("token") ? true : false;
    })(),
  );
  return (
    <AuthContext.Provider value={{ authenticated, setAuthenticated }}>
      <Header></Header>
      <CategoriesPanel></CategoriesPanel>
      <div className="root-container">
        <span>Hello world</span>
        <div className="outlet-container">
          <Outlet />
        </div>
      </div>
      <Footer></Footer>
    </AuthContext.Provider>
  );
}
