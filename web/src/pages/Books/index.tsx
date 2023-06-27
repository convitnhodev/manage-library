import {
  Button,
  Card,
  DatePicker,
  Form,
  Input,
  InputNumber,
  Modal,
  Pagination,
  Popconfirm,
  Select,
  Space,
  Table,
  Typography,
} from 'antd';
import React, { useEffect, useState } from 'react';
import '@/assets/scss/pages/books.scss';
import { DeleteOutlined, EditOutlined, PlusCircleOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import BookStore, { IBook } from '@/store/bookStore';
import { inject } from 'mobx-react';
import Stores from '@/store';
import RuleStore from '@/store/ruleStore';

const { Search } = Input;

interface IBooksProps {
  bookStore?: BookStore;
  ruleStore?: RuleStore;
}

const Books: React.FC = ({ bookStore, ruleStore }: IBooksProps) => {
  const [booksData, setBooksData] = useState<IBook[]>(); // booksDataInit is defined below
  const [currentPage, setCurrentPage] = useState(1);
  const [searchKeyword, setSearchKeyword] = useState('');
  const [newBookForm] = Form.useForm();
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [selectedBook, setSelectedBook] = useState<IBook | null>(null); // The book object that is being viewed or edited
  const [booksLoading, setBooksLoading] = useState(true);

  const getAllBooks = async () => {
    try {
      await bookStore?.getAll();
    } catch (error) {
      console.log(error);
    } finally {
      setBooksLoading(false);
    }
  };

  useEffect(() => {
    bookStore?.booksData.length ? setBooksLoading(false) : getAllBooks();
  }, [bookStore]);

  useEffect(() => {
    setBooksData(bookStore?.booksData);
  }, [bookStore?.booksData]);

  const columns = [
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
    {
      title: 'Tổng sách',
      dataIndex: 'numberOfCopies',
      key: 'numberOfCopies',
    },
    {
      title: 'Tổng sách cho mượn',
      dataIndex: 'numberOfBorrowedCopies',
      key: 'numberOfBorrowedCopies',
    },
    {
      title: 'Actions',
      dataIndex: 'id',
      key: 'actions',
      render: (id: number) => {
        const record = booksData?.find(book => book.id === id); // Find the corresponding book object
        return record ? (
          <Space size="small">
            <Button type="link" onClick={() => viewBookDetails(record)}>
              <EditOutlined />
            </Button>
            <Popconfirm
              title="Are you sure to delete this book?"
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
    newBookForm.resetFields();
    setSelectedBook(null);
    setIsModalVisible(true);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
  };

  const onSearch = (value: string) => {
    setSearchKeyword(value.trim());
    setCurrentPage(1); // Reset current page to 1 when performing a new search
  };

  const handleDelete = async (id: number) => {
    const bookDeleted = await bookStore?.deleteBook(id);
    const updatedBooksData = booksData?.filter(book => book.id !== bookDeleted?.id);
    setBooksData(updatedBooksData);
  };

  const handleAddBook = () => {
    newBookForm.validateFields().then(async values => {
      const newBook = {
        id: booksData?.length ? booksData.length + 1 : 1,
        name: values.name,
        category: values.category,
        author: values.author,
        numberOfCopies: values.numberOfCopies,
        publicCationYear: values.publicationYear?.year(),
        publisher: values.publisher,
        importDate: values.importDate?.toDate(),
      };
      const new_book = await bookStore?.createNewBook(newBook);
      if (new_book) {
        setBooksData(booksData ? [...booksData, new_book] : [new_book]);
      }

      newBookForm.resetFields();
      setIsModalVisible(false);
    });
  };

  const handleUpdateBook = () => {
    if (!selectedBook) return;
    newBookForm.validateFields().then(async values => {
      const updatedBook = {
        id: selectedBook.id,
        name: values.name,
        category: values.category,
        author: values.author,
        numberOfCopies: values.numberOfCopies,
        publicCationYear: values.publicationYear?.year(),
        publisher: values.publisher,
        importDate: values.importDate?.toDate(),
      };
      let updatedBooksData;
      const bookUpdated = await bookStore?.updateBook(updatedBook);
      if (booksData && bookUpdated) {
        console.log(bookUpdated);
        updatedBooksData = booksData.map(book => {
          if (book.id === bookUpdated.id) {
            return bookUpdated;
          }
          return book;
        });
        setBooksData(updatedBooksData);
      }
      newBookForm.resetFields();
      setIsModalVisible(false);
    });
  };

  const viewBookDetails = (book: IBook) => {
    setIsModalVisible(true);
    setSelectedBook(book);

    // Set the form values
    newBookForm.setFieldsValue({
      name: book.name,
      category: book.category,
      author: book.author,
      publicationYear: book.publicCationYear ? dayjs(`${book.publicCationYear}`) : null,
      publisher: book.publisher,
      importDate: book.importDate ? dayjs(book.importDate) : null,
      numberOfCopies: book.numberOfCopies,
    });
  };

  // Configure pagination
  const pageSize = 5;
  const totalBooks = booksData?.length;

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  // Calculate the start and end index for the current page
  const startIndex = (currentPage - 1) * pageSize;
  const endIndex = startIndex + pageSize;

  // Filter the booksData based on the search keyword
  const filteredData = searchKeyword
    ? booksData?.filter(
        book =>
          book.name.toLowerCase().includes(searchKeyword.toLowerCase()) ||
          book.category.toLowerCase().includes(searchKeyword.toLowerCase()),
      )
    : booksData;

  // Slice the data source to display only the books for the current page
  const currentPageData = filteredData?.slice(startIndex, endIndex);

  return (
    <div className="books">
      <div className="books__search">
        <Typography.Title level={2}>Tìm kiếm sách</Typography.Title>
        <Search placeholder="Nhập vào tên sách" allowClear enterButton="Search" size="large" onSearch={onSearch} />
      </div>
      <Card
        className="books__list"
        loading={booksLoading}
        title={
          <Space className="books__list__title">
            <Typography.Title level={3}>Danh sách sách</Typography.Title>
            <Typography.Title level={3}>Tổng số: {totalBooks}</Typography.Title>
            <Typography.Title level={3}>Hiển thị: {currentPageData?.length}</Typography.Title>
            <Button
              type="primary"
              size="large"
              icon={<PlusCircleOutlined />}
              className="book__list_titleBtn"
              onClick={showModal}
            />
          </Space>
        }
      >
        <Modal
          title={selectedBook ? 'Chi tiết sách' : 'Thêm sách'}
          open={isModalVisible}
          onCancel={handleCancel}
          footer={[
            <Button key="cancel" onClick={handleCancel}>
              Hủy
            </Button>,
            selectedBook ? (
              <Button key="edit" type="primary" onClick={handleUpdateBook}>
                Câp nhật
              </Button>
            ) : (
              <Button key="add" type="primary" onClick={handleAddBook}>
                Thêm
              </Button>
            ),
          ]}
        >
          <Form form={newBookForm} layout="vertical">
            <Form.Item name="name" label="Tên sách" rules={[{ required: true, message: 'Vui lòng nhập tên sách' }]}>
              <Input placeholder="Tên sách" />
            </Form.Item>
            <Form.Item
              name="category"
              label="Thể loại"
              rules={[{ required: true, message: 'Vui lòng nhập thể loại sách' }]}
            >
              <Select placeholder="Thể loại" allowClear>
                {ruleStore?.ruleData?.categoryBooks?.map((cat: string) => (
                  <Select.Option key={cat} value={cat}>
                    {cat}
                  </Select.Option>
                ))}
              </Select>
            </Form.Item>
            <Form.Item
              name="author"
              label="Tác giả"
              rules={[{ required: true, message: 'Vui lòng nhập tác giả sách' }]}
            >
              <Input placeholder="Tác giả" />
            </Form.Item>
            <Form.Item
              name="publicationYear"
              label="Năm xuất bản"
              rules={[{ required: true, message: 'Vui lòng chọn năm xuất bản' }]}
            >
              <DatePicker picker="year" placeholder="Năm xuất bản" />
            </Form.Item>
            <Form.Item
              name="publisher"
              label="Nhà xuất bản"
              rules={[{ required: true, message: 'Vui lòng nhập nhà xuất bản' }]}
            >
              <Input placeholder="Tác giả" />
            </Form.Item>
            <Form.Item
              name="importDate"
              label="Ngày nhập sách"
              rules={[{ required: true, message: 'Vui lòng chọn ngày nhập sách' }]}
            >
              <DatePicker placeholder="Ngày nhập sách" />
            </Form.Item>
            <Form.Item
              name="numberOfCopies"
              label="Số lượng sách"
              rules={[{ required: true, message: 'Vui lòng nhập số lượng sách' }]}
            >
              <InputNumber placeholder="Số lượng sách" min={1} />
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

export default inject(Stores.BookStore, Stores.RuleStore)(Books);
