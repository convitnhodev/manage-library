import { Outlet } from 'react-router-dom';
import { Layout } from 'antd';
import '@/assets/scss/pages/authLayout.scss';
const { Content } = Layout;

const AuthLayout = () => {
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <div className="authLayout__background" />
      <Content className="authLayout__content">
        <Outlet />
      </Content>
    </Layout>
  );
};

export default AuthLayout;
