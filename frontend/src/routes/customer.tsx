import React from 'react';
import { useContext } from "react";
import CustomerComponent from '../components/customer';
import { Navigate } from 'react-router-dom';
import { AuthContext } from "../routes/root";

function CustomerPage() {
  const { authenticated, setAuthenticated } = useContext(AuthContext);
  if (authenticated) {
    return <CustomerComponent />;
  } else {
    return <Navigate to="/login" />;
  }
};

export default CustomerPage;