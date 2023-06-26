import { RouteObject } from 'react-router-dom';
import AppLayout from '@/pages/layout/appLayout';
import { IRoute, appRouters, authRouter } from '@/routes/route.config';
import AuthLayout from '@/pages/layout/authLayout';
import PrivateRoute from './PrivateRoute';

export default [
  {
    path: '/',
    element: (
      <PrivateRoute loginPath="/auth/login">
        <AppLayout />
      </PrivateRoute>
    ),
    children: appRouters.map((route: IRoute) => {
      return {
        path: route.path,
        element: <route.component />,
      };
    }),
  },
  {
    path: '/auth',
    element: <AuthLayout />,
    children: authRouter.map((route: IRoute) => {
      return {
        path: route.path,
        element: <route.component />,
      };
    }),
  },
] as RouteObject[];
