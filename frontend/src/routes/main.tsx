import {Outlet} from "react-router-dom";
import Header from "../components/header";
import {createContext, useState} from "react";
import Cookies from "universal-cookie";
import Footer from "../components/footer";
import CategoriesPanel from "../components/categories-panel";
import { ToastContainer } from "react-toastify";

export default function Main() {
    return (
        <>
        <CategoriesPanel></CategoriesPanel>
        <div className="root-container">
            <span>Hello world</span>
        </div>
        </>
    );
}