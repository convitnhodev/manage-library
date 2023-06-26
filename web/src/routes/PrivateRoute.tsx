import React from 'react';
import { useIsAuthenticated } from 'react-auth-kit';
import { useLocation, Navigate } from 'react-router-dom';

interface PrivateRouteProps {
  children: React.ReactNode;
  loginPath: string;
}

const PrivateRoute: React.FC<PrivateRouteProps> = ({ children, loginPath }) => {
  const isAuthenticated = useIsAuthenticated();
  const location = useLocation();

  if (isAuthenticated()) {
    return <>{children}</>;
  }

  return <Navigate to={loginPath} state={{ from: location }} replace />;
};

export default PrivateRoute;
