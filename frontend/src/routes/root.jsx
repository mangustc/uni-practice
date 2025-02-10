import { Outlet } from "react-router-dom";
// import Navigation from "../components/navigation";
import { createContext, useState } from "react";
import Cookies from "universal-cookie";

const cookies = new Cookies();
export const AuthContext = createContext({
  authenticated: (() => {
    return cookies.get("token") ? true : false;
  })(),
  setAuthenticated: (auth) => { },
});

export default function Root() {
  const [authenticated, setAuthenticated] = useState(
    (() => {
      return cookies.get("token") ? true : false;
    })(),
  );
  return (
    <AuthContext.Provider value={{ authenticated, setAuthenticated }}>
      <div className="root-container">
        {/* <Navigation></Navigation> */}
        <span>Hello world</span>
        <div className="outlet-container">
          <Outlet />
        </div>
      </div>
    </AuthContext.Provider>
  );
}
