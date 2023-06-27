import React, { useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import { Layout } from 'antd';
import SiderMenu from '@/components/SiderMenu';
import Header from '@/components/Header/header';
import RuleStore from '@/store/ruleStore';
import { inject } from 'mobx-react';
import Stores from '@/store';

const { Content } = Layout;

interface IAppLayoutProps {
  ruleStore?: RuleStore;
}

const AppLayout = ({ ruleStore }: IAppLayoutProps) => {
  useEffect(() => {
    (async () => {
      try {
        await ruleStore?.getAll();
      } catch (error) {
        console.log(error);
      }
    })();
  }, []);

  const [collapsed, setCollapsed] = React.useState(false);

  const onCollapse = (collapsed: boolean) => {
    setCollapsed(collapsed);
  };

  const toggle = () => {
    setCollapsed(!collapsed);
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <SiderMenu onCollapse={onCollapse} collapsed={collapsed} />
      <Layout>
        <Layout.Header style={{ background: '#fff', minHeight: 52, padding: 0 }}>
          <Header collapsed={collapsed} toggle={toggle} />
        </Layout.Header>
        <Content style={{ margin: '24px 16px 0' }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};

export default inject(Stores.RuleStore)(AppLayout);
