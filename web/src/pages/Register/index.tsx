import { Form, Input, Button, Avatar, Col, Row, DatePicker, notification } from 'antd';
import AppLogo from '@/assets/images/logo.png';
import { AimOutlined, LockOutlined, MailOutlined, PhoneOutlined, UserOutlined } from '@ant-design/icons';
import { Link, useNavigate } from 'react-router-dom';
import '@/assets/scss/pages/register.scss';
import authService from '@/service/authService';

const RegisterPage = () => {
  const navigate = useNavigate();
  const onFinish = async (values: any) => {
    console.log('Received values of form: ', values);
    const res = await authService.signup(values);
    if (res.username) {
      notification.destroy('registerSuccess');
      notification.success({
        key: 'registerSuccess',
        message: 'Đăng ký thành công',
        description: 'Vui lòng đăng nhập để tiếp tục sử dụng dịch vụ!',
        placement: 'top',
      });
      navigate('/auth/login');
    }
  };

  return (
    <Form name="register-form" onFinish={onFinish} className="register">
      <div className="register__logo">
        <Avatar shape="square" style={{ height: 100, width: 100 }} src={AppLogo} />
      </div>

      <Form.Item name="username" rules={[{ required: true, message: 'Please input your Username!' }]}>
        <Input prefix={<UserOutlined />} placeholder="Username" />
      </Form.Item>
      <Form.Item name="name" rules={[{ required: true, message: 'Please input your name!' }]}>
        <Input prefix={<UserOutlined />} placeholder="name" />
      </Form.Item>
      <Form.Item name="address" rules={[{ required: true, message: 'Please input your address!' }]}>
        <Input prefix={<AimOutlined />} placeholder="address" />
      </Form.Item>
      <Form.Item name="dob" rules={[{ required: true, message: 'Please input your birthday!' }]}>
        <DatePicker placeholder="Birthday" className="date-input" />
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
      <Form.Item name="numberphone" rules={[{ required: true, message: 'Please input your phone number!' }]}>
        <Input prefix={<PhoneOutlined />} placeholder="phone number" />
      </Form.Item>
      <Form.Item>
        <Button type="primary" danger htmlType="submit" block>
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
