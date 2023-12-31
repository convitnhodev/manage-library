import { DeleteOutlined, FundViewOutlined } from '@ant-design/icons';
import { Card, Space, Typography, Button, Modal, Table, Pagination, Popconfirm, DatePicker, Form, Select } from 'antd';
import { useEffect, useState } from 'react';
import '@/assets/scss/pages/loanSlips.scss';
import BookStore, { IBook } from '@/store/bookStore';
import LoanSlipStore, { ILoanSlip } from '@/store/loanSlipStore';
import { inject } from 'mobx-react';
import Stores from '@/store';
import dayjs from 'dayjs';
import MemberStore, { IMember } from '@/store/memberStore';
import { set } from 'lodash';

interface ILoanSlipsProps {
  loanSlipStore: LoanSlipStore;
  bookStore: BookStore;
  memberStore?: MemberStore;
}

const LoanSlips = ({ loanSlipStore, bookStore, memberStore }: ILoanSlipsProps) => {
  const [loanSlipsData, setLoanSlipsData] = useState<ILoanSlip[]>([]); // booksDataInit is defined below
  const [currentPage, setCurrentPage] = useState(1);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [isModalCreateLoanSlipVisible, setIsModalCreateLoanSlipVisible] = useState(false);
  const [selectedLoanSlips, setSelectedLoanSlips] = useState<ILoanSlip | null>(null);
  const [loading, setLoading] = useState(true);
  const [newLoanSlipForm] = Form.useForm();
  const [searchKeyword, setSearchKeyword] = useState('');
  const [searchMemberKeyword, setSearchMemberKeyword] = useState('');

  const getLoanSlipsData = async () => {
    try {
      await loanSlipStore?.getAll();
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getLoanSlipsData();
    if (!bookStore?.booksData.length) {
      bookStore?.getAll();
    }
    if (!memberStore?.memberData.length) {
      memberStore?.getAll();
    }
  }, []);

  useEffect(() => {
    setLoanSlipsData(loanSlipStore?.loanSlips);
  }, [loanSlipStore?.loanSlips]);

  const columns = [
    {
      title: 'STT',
      dataIndex: 'id',
      key: 'id',
    },
    {
      title: 'Tên độc giả',
      dataIndex: 'borrowerId',
      key: 'borrowerId',
      render: (borrowerId: number) => {
        const member = memberStore?.memberData.find(member => member.id === borrowerId);
        return member?.name;
      },
    },
    {
      title: 'Số sách mượn',
      dataIndex: 'books',
      key: 'books',
      render: (books: number[]) => {
        return books?.length;
      },
    },
    {
      title: 'Actions',
      dataIndex: 'id',
      key: 'actions',
      render: (id: number) => {
        const record = loanSlipsData.find(loanSlip => loanSlip.id === id);
        return record ? (
          <Space size="small">
            <Button type="link" onClick={() => viewLoanSlipDetail(record)}>
              <FundViewOutlined />
            </Button>
            <Popconfirm
              title="Are you sure to delete this loan slip?"
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

  const viewLoanSlipDetail = (loanSlip: ILoanSlip) => {
    setSelectedLoanSlips(loanSlip);
    setIsModalVisible(true);
  };

  const handleDelete = async (id: number) => {
    const result = await loanSlipStore.deleteLoanSlip(id);
    const newData = loanSlipsData.filter(loanSlip => loanSlip.id !== result.id);
    setLoanSlipsData(newData);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
  };

  // Configure pagination
  const pageSize = 5;
  const totalBooks = loanSlipsData.length;

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  // Calculate the start and end index for the current page
  const startIndex = (currentPage - 1) * pageSize;
  const endIndex = startIndex + pageSize;

  // Slice the data source to display only the books for the current page
  const currentPageData = loanSlipsData.slice(startIndex, endIndex);

  return (
    <>
      <Typography.Title level={2}>Quản lý phiếu mượn</Typography.Title>
      <Button type="primary" onClick={() => setIsModalCreateLoanSlipVisible(true)}>
        Lập phiếu mượn
      </Button>
      <Modal
        title="Basic Modal"
        open={isModalCreateLoanSlipVisible}
        onCancel={() => setIsModalCreateLoanSlipVisible(false)}
        footer={[
          <Button key="back" onClick={() => setIsModalCreateLoanSlipVisible(false)}>
            Hủy
          </Button>,
          <Button
            key="submit"
            type="primary"
            onClick={() => {
              newLoanSlipForm.validateFields().then(async values => {
                const result = await loanSlipStore.createLoanSlip(values);
                if (result === 433) {
                  alert('Không thể tạo phiếu mượn do độc giả đã mượn sách quá số lượng cho phép');
                }
                newLoanSlipForm.resetFields();
                setIsModalCreateLoanSlipVisible(false);
                console.log(values);
              });
            }}
          >
            Lập phiếu mượn
          </Button>,
        ]}
      >
        <Form form={newLoanSlipForm} layout="vertical">
          <Form.Item
            name="id_card"
            label="Mã độc giả"
            rules={[{ required: true, message: 'Vui lòng chọn mã độc giả' }]}
          >
            <Select
              placeholder="Mã độc giả"
              allowClear
              showSearch
              onSearch={setSearchMemberKeyword} // Update the search keyword when input changes
            >
              {memberStore?.memberData
                .filter(
                  (member: IMember) =>
                    (searchMemberKeyword
                      ? member.name.toLowerCase().includes(searchMemberKeyword.toLowerCase()) ||
                        member.id === Number(searchMemberKeyword)
                      : true) &&
                    (loanSlipsData ? !loanSlipsData.find(loanSlip => loanSlip.borrowerId === member.id) : true),
                )
                .map((member: IMember) => (
                  <Select.Option key={member.id} value={member.id}>
                    {`${member.id} - ${member.name}`}
                  </Select.Option>
                ))}
            </Select>
          </Form.Item>
          <Form.Item
            name="created_at"
            label="Ngày lập phiếu"
            rules={[{ required: true, message: 'Vui lòng chọn ngày lập phiếu' }]}
          >
            <DatePicker placeholder="Ngày lập phiếu" />
          </Form.Item>
          <Form.Item
            name="ids_books"
            label="Sách mượn"
            rules={[{ required: true, message: 'Vui lòng nhập sách mượn' }]}
          >
            <Select
              mode="multiple"
              placeholder="Sách mượn"
              allowClear
              onSearch={setSearchKeyword} // Update the search keyword when input changes
            >
              {bookStore.booksData
                .filter(
                  (book: IBook) =>
                    (book.numberOfBorrowedCopies ? book.numberOfBorrowedCopies < book.numberOfCopies : true) &&
                    book.name.toLowerCase().includes(searchKeyword.toLowerCase()),
                )
                .map((book: IBook) => (
                  <Select.Option key={book.id} value={book.id}>
                    {`${book.id} - ${book.name}`}
                  </Select.Option>
                ))}
            </Select>
          </Form.Item>
        </Form>
      </Modal>
      <Card
        className="loanSlips"
        loading={loading}
        title={
          <Space className="loanSlips__title">
            <Typography.Title level={3}>Danh sách phiếu mượn</Typography.Title>
            <Typography.Title level={3}>Tổng số: {totalBooks}</Typography.Title>
            <Typography.Title level={3}>Hiển thị: {currentPageData.length}</Typography.Title>
          </Space>
        }
      >
        <Modal open={isModalVisible} onCancel={handleCancel} onOk={handleCancel}>
          <Typography.Title level={2}>Phiếu mượn sách</Typography.Title>
          <Typography.Title level={3}>Mã độc giả: {selectedLoanSlips?.borrowerId}</Typography.Title>
          <Typography.Title level={3}>
            Ngày mượn: {dayjs(selectedLoanSlips?.borrowDate).format('DD/MM/YYYY')}
          </Typography.Title>
          <Table
            dataSource={bookStore.booksData.filter(book => selectedLoanSlips?.books.includes(book.id))}
            columns={[
              {
                title: 'STT',
                dataIndex: 'id',
                key: 'id',
              },
              {
                title: 'Tên sách',
                dataIndex: 'name',
                key: 'name',
              },
              {
                title: 'Thể loại',
                dataIndex: 'category',
                key: 'category',
              },
              {
                title: 'Tác giả',
                dataIndex: 'author',
                key: 'author',
              },
            ]}
            bordered={true}
            pagination={false}
            rowKey={record => record.id}
          />
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
          total={loanSlipsData.length}
          onChange={handlePageChange}
          style={{ marginTop: 16, textAlign: 'right' }}
        />
      </Card>
    </>
  );
};

export default inject(Stores.LoanSlipStore, Stores.BookStore, Stores.MemberStore)(LoanSlips);
