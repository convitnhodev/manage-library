import { BrowserRouter } from 'react-router-dom';
import { createRoot } from 'react-dom/client';
import App from '@/App';
import '@/assets/scss/style.scss';
import { AuthProvider } from 'react-auth-kit';

const container = document.getElementById('root');
const root = createRoot(container!);

const app = (
  <AuthProvider
    authType={'cookie'}
    authName={'_auth'}
    cookieDomain={window.location.hostname}
    cookieSecure={window.location.protocol === 'https:'}
  >
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </AuthProvider>
);
root.render(app);
