import { RouteObject } from 'react-router-dom';
import AppLayout from '@/pages/layout/appLayout';
import { IRoute, appRouters, authRouter } from '@/routes/route.config';
import AuthLayout from '@/pages/layout/authLayout';
import PrivateRoute from './PrivateRoute';
import { Provider } from 'mobx-react';
import initializeStores from '@/store/initializeStore';

const stores = initializeStores();

export default [
  {
    path: '/',
    element: (
      <Provider {...stores}>
        <PrivateRoute loginPath="/auth/login">
          <AppLayout />
        </PrivateRoute>
      </Provider>
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
