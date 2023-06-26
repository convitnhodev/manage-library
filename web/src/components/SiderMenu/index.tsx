import '@/assets/scss/components/sider.scss';

import { Avatar, Col, Layout, Menu } from 'antd';
import AppLogo from '@/assets/images/logo.png';
import { appRouters } from '@/routes/route.config';

import { Link, useLocation } from 'react-router-dom';

const { Sider } = Layout;

export interface ISiderMenuProps {
  collapsed: boolean;
  onCollapse: any;
}

const SiderMenu = (props: ISiderMenuProps) => {
  const { collapsed, onCollapse } = props;
  const location = useLocation();

  return (
    <Sider
      trigger={null}
      className={'sidebar'}
      width={256}
      collapsedWidth={60}
      collapsible
      collapsed={collapsed}
      onCollapse={onCollapse}
    >
      {collapsed ? (
        <Col className="app-logo">
          <Avatar shape="square" style={{ height: 42, width: 42 }} src={AppLogo} />
        </Col>
      ) : (
        <Col className="app-logo">
          <Avatar shape="square" style={{ height: 200, width: 200 }} src={AppLogo} />
        </Col>
      )}

      <Menu theme="dark" mode="inline" defaultSelectedKeys={['/']} selectedKeys={[location.pathname]}>
        {appRouters
          .filter((item: any) => !item.isLayout && item.showInMenu)
          .map((route: any, index: number) => {
            return (
              <Menu.Item key={route.path}>
                <Link to={route.path}>
                  <route.icon />
                  <span>{route.name}</span>
                </Link>
              </Menu.Item>
            );
          })}
      </Menu>
    </Sider>
  );
};

export default SiderMenu;
