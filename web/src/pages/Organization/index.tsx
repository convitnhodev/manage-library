import { Button, Card, DatePicker, Form, Input, Modal, Pagination, Popconfirm, Space, Table, Typography } from 'antd';
import React, { useEffect, useState } from 'react';
import '@/assets/scss/pages/organization.scss';
import { DeleteOutlined, EditOutlined, PlusCircleOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import { inject } from 'mobx-react';
import Stores from '@/store';
import OrganizationStore, { IUser } from '@/store/organizationStore';

const { Search } = Input;

interface IOrganizationProps {
  organizationStore?: OrganizationStore;
}

const Organization: React.FC = ({ organizationStore }: IOrganizationProps) => {
  const [usersData, setUsersData] = useState<IUser[]>();
  const [currentPage, setCurrentPage] = useState(1);
  const [searchKeyword, setSearchKeyword] = useState('');
  const [newUserForm] = Form.useForm();
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [selectedUser, setSelectedUser] = useState<IUser | null>(null);
  const [organizationLoading, setOrganizationLoading] = useState(true);

  const getAll = async () => {
    try {
      await organizationStore?.getAllUser();
    } catch (error) {
      console.log(error);
    } finally {
      setOrganizationLoading(false);
    }
  };

  useEffect(() => {
    organizationStore?.organizationData.length ? setOrganizationLoading(false) : getAll();
  }, [organizationStore]);

  useEffect(() => {
    setUsersData(organizationStore?.organizationData);
  }, [organizationStore?.organizationData]);

  const columns = [
    {
      title: 'STT',
      dataIndex: 'id',
      key: 'id',
    },
    {
      title: 'Tên',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Số điện thoại',
      dataIndex: 'phone',
      key: 'phone',
    },
    {
      title: 'Email',
      dataIndex: 'email',
      key: 'email',
    },
    {
      title: 'Địa chỉ',
      dataIndex: 'address',
      key: 'address',
    },
    {
      title: 'Actions',
      dataIndex: 'id',
      key: 'actions',
      render: (id: number) => {
        const record = usersData?.find(user => user.id === id);
        return record ? (
          <Space size="small">
            <Button type="link" onClick={() => viewUserDetails(record)}>
              <EditOutlined />
            </Button>
            <Popconfirm
              title="Are you sure to delete this user?"
              onConfirm={() => handleDelete(id)}
              okText="Yes"
              cancelText="No"
            >
              <Button type="link" danger>
                <DeleteOutlined />
              </Button>
            </Popconfirm>
          </Space>
        ) : null;
      },
    },
  ];

  const showModal = () => {
    newUserForm.resetFields();
    setSelectedUser(null);
    setIsModalVisible(true);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
  };

  const onSearch = (value: string) => {
    setSearchKeyword(value.trim());
    setCurrentPage(1); // Reset current page to 1 when performing a new search
  };

  const handleDelete = (id: number) => {
    const updatedUsersData = usersData?.filter(user => user.id !== id);
    setUsersData(updatedUsersData);
  };

  const handleAddUser = () => {
    newUserForm.validateFields().then(async values => {
      const newUser = {
        id: usersData?.length ? usersData.length + 1 : 1,
        name: values.name,
        username: values.username,
        password: values.password,
        birthday: values.birthday?.toDate(),
        address: values.address,
        email: values.email,
        phone: values.phone,
      };
      setUsersData(usersData ? [...usersData, newUser] : [newUser]);
      newUserForm.resetFields();
      setIsModalVisible(false);
    });
  };

  const handleUpdateUser = () => {
    if (!selectedUser) return;
    newUserForm.validateFields().then(values => {
      const updatedUser = {
        id: selectedUser.id,
        name: values.name,
        username: values.username,
        password: values.password,
        birthday: values.birthday?.toDate(),
        address: values.address,
        email: values.email,
        phone: values.phone,
      };
      let updatedUsersData: IUser[] | undefined;
      if (usersData) {
        updatedUsersData = usersData.map(user => {
          if (user.id === updatedUser.id) {
            return updatedUser;
          }
          return user;
        });
        setUsersData(updatedUsersData);
      }
      newUserForm.resetFields();
      setIsModalVisible(false);
    });
  };

  const viewUserDetails = (user: IUser) => {
    setIsModalVisible(true);
    setSelectedUser(user);

    // Set the form values
    newUserForm.setFieldsValue({
      name: user.name,
      username: user.username,
      password: '',
      address: user.address,
      email: user.email,
      birthday: user.birthday ? dayjs(user.birthday) : null,
      phone: user.phone,
    });
  };

  // Configure pagination
  const pageSize = 5;
  const totalUsers = usersData?.length;

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  // Calculate the start and end index for the current page
  const startIndex = (currentPage - 1) * pageSize;
  const endIndex = startIndex + pageSize;

  const filteredData = searchKeyword
    ? usersData?.filter(
        user =>
          user.name.toLowerCase().includes(searchKeyword.toLowerCase()) ||
          user.username.toLowerCase().includes(searchKeyword.toLowerCase()),
      )
    : usersData;

  const currentPageData = filteredData?.slice(startIndex, endIndex);

  return (
    <div className="organization">
      <div className="organization__search">
        <Typography.Title level={2}>Tìm kiếm nhân viên</Typography.Title>
        <Search
          placeholder="Nhập vào tên hoặc tên đăng nhập"
          allowClear
          enterButton="Search"
          size="large"
          onSearch={onSearch}
        />
      </div>
      <Card
        className="organization__list"
        loading={organizationLoading}
        title={
          <Space className="organization__list__title">
            <Typography.Title level={3}>Danh sách nhân viên</Typography.Title>
            <Typography.Title level={3}>Tổng số: {totalUsers}</Typography.Title>
            <Typography.Title level={3}>Hiển thị: {currentPageData?.length}</Typography.Title>
            <Button
              type="primary"
              size="large"
              icon={<PlusCircleOutlined />}
              className="organization__list_titleBtn"
              onClick={showModal}
            />
          </Space>
        }
      >
        <Modal
          title={selectedUser ? 'Xem thông tin nhân viên' : 'Thêm nhân viên'}
          open={isModalVisible}
          onCancel={handleCancel}
          footer={[
            <Button key="cancel" onClick={handleCancel}>
              Hủy
            </Button>,
            selectedUser ? (
              <Button key="edit" type="primary" onClick={handleUpdateUser}>
                Câp nhật
              </Button>
            ) : (
              <Button key="add" type="primary" onClick={handleAddUser}>
                Thêm
              </Button>
            ),
          ]}
        >
          <Form form={newUserForm} layout="vertical">
            <Form.Item
              name="name"
              label="Tên nhân viên"
              rules={[{ required: true, message: 'Vui lòng nhập tên nhân viên' }]}
            >
              <Input placeholder="Tên nhân viên" />
            </Form.Item>
            <Form.Item
              name="username"
              label="Tên đăng nhập"
              rules={[{ required: true, message: 'Vui lòng nhập tên đăng nhập' }]}
            >
              <Input placeholder="Tên đăng nhập" />
            </Form.Item>
            <Form.Item label="Mật khẩu" name="password" rules={[{ required: true, message: 'Vui lòng nhập mật khẩu' }]}>
              <Input.Password type="password" placeholder="Mật khẩu" />
            </Form.Item>

            <Form.Item
              name="confirmPassword"
              label="Xác nhận mật khẩu"
              dependencies={['password']}
              rules={[
                { required: true, message: 'Vui lòng xác nhận lại mật khẩu' },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue('password') === value) {
                      return Promise.resolve();
                    }
                    return Promise.reject(new Error('Mật khẩu không khớp'));
                  },
                }),
              ]}
            >
              <Input.Password type="password" placeholder="Xác nhận mật khẩu" />
            </Form.Item>
            <Form.Item
              name="birthday"
              label="Ngày sinh"
              rules={[{ required: true, message: 'Vui lòng chọn ngày sinh' }]}
            >
              <DatePicker placeholder="Ngày sinh" />
            </Form.Item>
            <Form.Item name="address" label="Địa chỉ" rules={[{ required: true, message: 'Vui lòng nhập địa chỉ' }]}>
              <Input placeholder="Địa chỉ" />
            </Form.Item>
            <Form.Item name="email" label="Email" rules={[{ required: true, message: 'Vui lòng nhập email' }]}>
              <Input placeholder="Email" />
            </Form.Item>
            <Form.Item
              name="phone"
              label="Số điện thoại"
              rules={[{ required: true, message: 'Vui lòng nhập số điện thoại' }]}
            >
              <Input placeholder="Số điện thoại" />
            </Form.Item>
          </Form>
        </Modal>
        <Table
          dataSource={currentPageData}
          columns={columns}
          bordered={true}
          pagination={false}
          rowKey={record => record.id}
        />
        <Pagination
          current={currentPage}
          pageSize={pageSize}
          total={filteredData?.length}
          onChange={handlePageChange}
          style={{ marginTop: 16, textAlign: 'right' }}
        />
      </Card>
    </div>
  );
};

export default inject(Stores.OrganizationStore)(Organization);
