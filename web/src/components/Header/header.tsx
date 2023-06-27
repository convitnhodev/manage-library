import { useState } from 'react';
import { Avatar, Button, Col, Dropdown, Menu, Row } from 'antd';
import { MenuUnfoldOutlined, MenuFoldOutlined, LogoutOutlined, CaretDownOutlined } from '@ant-design/icons';
import '@/assets/scss/components/header.scss';
import profilePicture from '@/assets/images/avatar.png';
import { useAuthUser, useSignOut } from 'react-auth-kit';

export interface IHeaderProps {
  collapsed: boolean;
  toggle: () => void;
}

const Header = ({ collapsed, toggle }: IHeaderProps) => {
  const auth = useAuthUser();
  const signOut = useSignOut();
  const [user, setUser] = useState<any>(auth());

  const userDropdownMenu = () => (
    <Menu>
      <Menu.Item key="0">
        <div className="user-dropdown">
          <Avatar
            className="avatar"
            style={{ height: 50, width: 50 }}
            shape="circle"
            alt={'profile'}
            src={profilePicture}
          />
          <span className="user-info">
            <div className="full-name">{user}</div>
          </span>
        </div>
      </Menu.Item>
      <Menu.Item key="1">
        <Button type="link" onClick={() => signOut()}>
          <LogoutOutlined />
          Đăng xuất
        </Button>
      </Menu.Item>
    </Menu>
  );

  return (
    <Row className={'header-container'}>
      <Col style={{ textAlign: 'left' }} span={12}>
        {collapsed ? (
          <MenuUnfoldOutlined className="trigger" onClick={toggle} />
        ) : (
          <MenuFoldOutlined className="trigger" onClick={toggle} />
        )}
      </Col>
      <Col style={{ padding: '0px 25px 0px 15px', textAlign: 'right', cursor: 'pointer' }} span={12}>
        <Dropdown arrow overlay={userDropdownMenu()} trigger={['click']}>
          <span className="username">
            <span>Xin chào {user}!</span>
            <CaretDownOutlined />
          </span>
        </Dropdown>
      </Col>
    </Row>
  );
};

export default Header;
