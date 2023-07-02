import { Outlet } from 'react-router-dom';
import { Layout } from 'antd';
import { useState } from 'react';
import '@/assets/scss/pages/authLayout.scss';

const { Content } = Layout;

const AuthLayout = () => {
  const [imageLoaded, setImageLoaded] = useState(false);

  const handleImageLoad = () => {
    setImageLoaded(true);
  };

  return (
    <Layout className="authLayout">
      <img
        className={`authLayout__background ${imageLoaded ? 'loaded' : ''}`}
        src="../../src/assets/images/auth-bg.jpg"
        alt="Background"
        onLoad={handleImageLoad}
      />
      {imageLoaded && (
        <Content className="authLayout__content">
          <Outlet />
        </Content>
      )}
    </Layout>
  );
};

export default AuthLayout;
