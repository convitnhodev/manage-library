import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { createRoot } from 'react-dom/client';

import App from '@/App';
import '@/assets/scss/style.scss';
import { Provider } from 'mobx-react';
import initializeStores from './store/initializeStore';
import { AuthProvider } from 'react-auth-kit';

const container = document.getElementById('root');
const root = createRoot(container!);
const stores = initializeStores();

const app = (
  <AuthProvider
    authType={'cookie'}
    authName={'_auth'}
    cookieDomain={window.location.hostname}
    cookieSecure={window.location.protocol === 'https:'}
  >
    <Provider {...stores}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </Provider>
  </AuthProvider>
);
root.render(app);
