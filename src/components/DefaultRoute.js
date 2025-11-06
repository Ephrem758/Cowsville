import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "context/AuthContext";

const DefaultRoute = () => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return <Navigate to="/authentication/sign-in" replace />;
};

export default DefaultRoute;
