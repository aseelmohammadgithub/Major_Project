import React from 'react';
import { Navigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';  // Make sure this is imported correctly

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');  // Get token from localStorage

  if (!token) {
    // If no token, redirect to login page
    return <Navigate to="/login" replace />;
  }

  try {
    const decoded = jwtDecode(token);  // Decode the token
    const currentTime = Date.now() / 1000;

    if (decoded.exp < currentTime) {
      // Token expired
      localStorage.removeItem('token');
      return <Navigate to="/login" replace />;
    }

    return children;  // Render the protected component if the token is valid
  } catch (error) {
    // Invalid token
    localStorage.removeItem('token');
    return <Navigate to="/login" replace />;
  }
};

export default ProtectedRoute;
