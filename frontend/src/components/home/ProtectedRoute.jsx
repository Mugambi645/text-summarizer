import React from "react";
import { Navigate } from "react-router-dom";
import { getAccessToken } from "../api";

export default function ProtectedRoute({ children }) {
  const token = getAccessToken();

  if (!token) {
    // redirect to login if no token
    return <Navigate to="/login" replace />;
  }

  return children;
}
