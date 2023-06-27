import { Form, Input, Button, Avatar, Col, Row } from 'antd';
import AppLogo from '@/assets/images/logo.png';
import { LockOutlined, MailOutlined, UserOutlined } from '@ant-design/icons';
import { Link } from 'react-router-dom';
import '@/assets/scss/pages/register.scss';

const RegisterPage = () => {
  const onFinish = (values: any) => {
    console.log('Received values of form: ', values);
  };

  return (
    <Form name="register-form" onFinish={onFinish} className="register">
      <div className="register__logo">
        <Avatar shape="square" style={{ height: 120, width: 120 }} src={AppLogo} />
      </div>

      <Form.Item name="username" rules={[{ required: true, message: 'Please input your Username!' }]}>
        <Input prefix={<UserOutlined />} placeholder="Username" />
      </Form.Item>

      <Form.Item
        name="email"
        rules={[
          { required: true, message: 'Please input your email!' },
          { type: 'email', message: 'Please enter a valid email address!' },
        ]}
      >
        <Input prefix={<MailOutlined />} placeholder="Email" />
      </Form.Item>

      <Form.Item name="password" rules={[{ required: true, message: 'Please input your password!' }]}>
        <Input.Password prefix={<LockOutlined />} type="password" placeholder="Password" />
      </Form.Item>

      <Form.Item
        name="confirmPassword"
        dependencies={['password']}
        rules={[
          { required: true, message: 'Please confirm your password!' },
          ({ getFieldValue }) => ({
            validator(_, value) {
              if (!value || getFieldValue('password') === value) {
                return Promise.resolve();
              }
              return Promise.reject(new Error('The two passwords do not match!'));
            },
          }),
        ]}
      >
        <Input.Password prefix={<LockOutlined />} type="password" placeholder="Confirm Password" />
      </Form.Item>

      <Form.Item>
        <Button disabled type="primary" danger htmlType="submit" block>
          Sign Up
        </Button>
      </Form.Item>

      <div>
        <Row>
          <Col span={12}>
            <Link to="/auth/login">Already have an account?</Link>
          </Col>
        </Row>
      </div>
    </Form>
  );
};

export default RegisterPage;
