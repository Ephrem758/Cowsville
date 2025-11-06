import React, { createContext, useContext, useState, useEffect } from "react";
import PropTypes from "prop-types";

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user is already authenticated on app load
    const token = localStorage.getItem("authToken") || sessionStorage.getItem("authToken");
    const username = localStorage.getItem("username") || sessionStorage.getItem("username");
    if (token && username) {
      setIsAuthenticated(true);
    }
    setIsLoading(false);
  }, []);

  const login = (token, rememberMe = false, username = null) => {
    if (rememberMe) {
      localStorage.setItem("authToken", token);
      if (username) localStorage.setItem("username", username);
    } else {
      sessionStorage.setItem("authToken", token);
      if (username) sessionStorage.setItem("username", username);
    }
    setIsAuthenticated(true);
  };

  const logout = () => {
    localStorage.removeItem("authToken");
    localStorage.removeItem("username");
    localStorage.removeItem("password");
    sessionStorage.removeItem("authToken");
    sessionStorage.removeItem("username");
    sessionStorage.removeItem("password");
    setIsAuthenticated(false);
  };

  const value = {
    isAuthenticated,
    isLoading,
    login,
    logout,
  };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

AuthProvider.propTypes = {
  children: PropTypes.node.isRequired,
};
