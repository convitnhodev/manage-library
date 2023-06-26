import { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Card, Pagination, Table, Typography } from 'antd';
import '@/assets/scss/pages/home.scss';
import { BookOutlined, UndoOutlined, UserAddOutlined, UserOutlined } from '@ant-design/icons';
import { inject } from 'mobx-react';
import Stores from '@/store';
import ReportStore, { IChartData, IReportData } from '@/store/reportStore';
import LoanSlipStore, { IBooksLoan } from '@/store/loanSlipStore';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface IHomeProps {
  reportStore?: ReportStore;
  loanSlipStore: LoanSlipStore;
}

const Home = ({ reportStore, loanSlipStore }: IHomeProps) => {
  const [dataReport, setDataReport] = useState<IReportData>();
  const [dataChart, setDataChart] = useState<IChartData>();
  const [booksLoanData, setBooksLoanData] = useState<IBooksLoan[]>([]);
  const [loading, setLoading] = useState(true);

  const getDataReport = async () => {
    try {
      await reportStore?.getData();
    } catch (error) {
      console.log(error);
    }
  };

  const getBooksLoanData = async () => {
    try {
      await loanSlipStore?.getBooksLoan();
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getDataReport();
    getBooksLoanData();
  }, []);

  useEffect(() => {
    setDataReport(reportStore?.dataReport);
    setDataChart(reportStore?.dataChart);
    setBooksLoanData(loanSlipStore?.booksLoan);
  }, [reportStore?.dataReport, reportStore?.dataChart]);

  const dataSourceReport = [
    {
      key: '1',
      visitors: {
        icon: <UserOutlined />,
        value: dataReport?.visitors,
      },
      borrowed: {
        icon: <BookOutlined />,
        value: dataReport?.borrowed,
      },
      returned: {
        icon: <UndoOutlined />,
        value: dataReport?.returned,
      },
      newMembers: {
        icon: <UserAddOutlined />,
        value: dataReport?.newMembers,
      },
    },
  ];

  const columnsReport = [
    {
      title: 'Đọc giả đến thư viện',
      dataIndex: 'visitors',
      key: 'visitors',
      align: 'center' as const,
      render: (visitors: { icon: JSX.Element; value: number }) => (
        <>
          {visitors.icon}
          <span>{visitors.value}</span>
        </>
      ),
    },
    {
      title: 'Sách được mượn',
      dataIndex: 'borrowed',
      key: 'borrowed',
      align: 'center' as const,
      render: (borrowed: { icon: JSX.Element; value: number }) => (
        <>
          {borrowed.icon}
          <span>{borrowed.value}</span>
        </>
      ),
    },
    {
      title: 'Sách đã trả',
      dataIndex: 'returned',
      key: 'returned',
      align: 'center' as const,
      render: (returned: { icon: JSX.Element; value: number }) => (
        <>
          {returned.icon}
          <span>{returned.value}</span>
        </>
      ),
    },
    {
      title: 'Đọc giả mới',
      dataIndex: 'newMembers',
      key: 'newMembers',
      align: 'center' as const,
      render: (newMembers: { icon: JSX.Element; value: number }) => (
        <>
          {newMembers.icon}
          <span>{newMembers.value}</span>
        </>
      ),
    },
  ];

  const labelsChart = ['Tuần 1', 'Tuần 2', 'Tuần 3', 'Tuần 4'];
  const valueChart = {
    labels: labelsChart,
    datasets: [
      {
        label: 'Số lượng đọc giả đến thư viện',
        backgroundColor: 'rgb(75, 192, 192)',
        data: dataChart?.visitors,
        stack: 'Stack 0',
      },
      {
        label: 'Số lượng đọc giả mượn sách',
        backgroundColor: 'rgb(53, 162, 235)',
        data: dataChart?.borrowers,
        stack: 'Stack 1',
      },
    ],
  };

  const options = {
    plugins: {
      title: {
        display: true,
        text: 'Biểu đồ thống kê',
      },
    },
    responsive: true,
    interaction: {
      mode: 'index' as const,
      intersect: false,
    },
    scales: {
      x: {
        stacked: true,
      },
      y: {
        stacked: true,
      },
    },
  };

  // Define the columns of the table
  const columns = [
    {
      title: 'STT',
      dataIndex: 'id',
      key: 'id',
    },
    {
      title: 'Tên sách',
      dataIndex: 'bookTitle',
      key: 'bookTitle',
    },
    {
      title: 'Người mượn',
      dataIndex: 'borrower',
      key: 'borrower',
    },
    {
      title: 'Ngày trả',
      dataIndex: 'returnDate',
      key: 'returnDate',
    },
  ];

  const [currentPage, setCurrentPage] = useState(1);

  // Configure pagination
  const pageSize = 5;
  const totalBooks = booksLoanData.length;

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  // Calculate the start and end index for the current page
  const startIndex = (currentPage - 1) * pageSize;
  const endIndex = startIndex + pageSize;

  // Slice the data source to display only the books for the current page
  const currentPageData = booksLoanData.slice(startIndex, endIndex);

  return (
    <div>
      <Card
        loading={loading}
        title={
          <Table dataSource={dataSourceReport} columns={columnsReport} pagination={false} className="tableReport" />
        }
      >
        <Bar data={valueChart} options={options} />
      </Card>
      <Card className="booksLoan" title={<Typography.Title level={2}>Sách đang được mượn</Typography.Title>}>
        <Table dataSource={currentPageData} columns={columns} rowKey={record => record.id} pagination={false} />
        <Pagination
          current={currentPage}
          pageSize={pageSize}
          total={totalBooks}
          onChange={handlePageChange}
          style={{ marginTop: 16, textAlign: 'right' }}
        />
      </Card>
    </div>
  );
};

export default inject(Stores.ReportStore, Stores.LoanSlipStore)(Home);
