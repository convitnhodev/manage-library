import { useEffect, useState } from 'react';
import { Button, Card, Form, InputNumber, Modal, Select, Table, Typography } from 'antd';
import '@/assets/scss/pages/home.scss';
import { inject } from 'mobx-react';
import Stores from '@/store';
import RuleStore from '@/store/ruleStore';

interface IRuleProps {
  ruleStore?: RuleStore;
}

const Rule = ({ ruleStore }: IRuleProps) => {
  const [loading, setLoading] = useState(true);
  const [dataSourceRule, setDataSourceRule] = useState<any>();
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [updateRuleForm] = Form.useForm();

  const getRuleData = async () => {
    try {
      await ruleStore?.getAll();
      setLoading(false);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    ruleStore?.hasRuleData() ? setLoading(false) : getRuleData();
  }, [ruleStore]);

  useEffect(() => {
    setDataSourceRule([
      {
        key: '1',
        minMemberAge: ruleStore?.ruleData.minMemberAge,
        maxMemberAge: ruleStore?.ruleData.maxMemberAge,
        periodValidCard: ruleStore?.ruleData.periodValidCard,
        categoryBooks: ruleStore?.ruleData.categoryBooks ? ruleStore?.ruleData.categoryBooks.join(', ') : '',
        publicationYearGap: ruleStore?.ruleData.publicationYearGap,
        maxBookCanBorrow: ruleStore?.ruleData.maxBookCanBorrow,
        maxDayCanBorrow: ruleStore?.ruleData.maxDayCanBorrow,
      },
    ]);
  }, [ruleStore?.ruleData]);

  const columnsRule = [
    {
      title: 'Tuổi độc giả tối thiểu',
      dataIndex: 'minMemberAge',
      key: 'minMemberAge',
      align: 'center' as const,
    },
    {
      title: 'Tuổi độc giả tối đa',
      dataIndex: 'maxMemberAge',
      key: 'maxMemberAge',
      align: 'center' as const,
    },
    {
      title: 'Thời hạn thẻ độc giả',
      dataIndex: 'periodValidCard',
      key: 'periodValidCard',
      align: 'center' as const,
    },
    {
      title: 'Các thể loại sách',
      dataIndex: 'categoryBooks',
      key: 'categoryBooks',
      align: 'center' as const,
    },
    {
      title: 'Khoảng cách năm xuất bản',
      dataIndex: 'publicationYearGap',
      key: 'publicationYearGap',
      align: 'center' as const,
    },
    {
      title: 'Số lượng sách mượn tối đa',
      dataIndex: 'maxBookCanBorrow',
      key: 'maxBookCanBorrow',
      align: 'center' as const,
    },
    {
      title: 'Số ngày mượn tối đa',
      dataIndex: 'maxDayCanBorrow',
      key: 'maxDayCanBorrow',
      align: 'center' as const,
    },
  ];

  const viewToUpdateRule = () => {
    setIsModalVisible(true);
    console.log(dataSourceRule);

    updateRuleForm.setFieldsValue({
      minMemberAge: dataSourceRule[0].minMemberAge,
      maxMemberAge: dataSourceRule[0].maxMemberAge,
      periodValidCard: dataSourceRule[0].periodValidCard,
      categoryBooks: dataSourceRule[0].categoryBooks.split(', '),
      publicationYearGap: dataSourceRule[0].publicationYearGap,
      maxBookCanBorrow: dataSourceRule[0].maxBookCanBorrow,
      maxDayCanBorrow: dataSourceRule[0].maxDayCanBorrow,
    });
  };

  return (
    <>
      <Typography.Title level={2}>Quy định thư viện</Typography.Title>
      <Button type="primary" onClick={viewToUpdateRule}>
        Cập nhật quy định
      </Button>
      <Modal
        title="Basic Modal"
        open={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        footer={[
          <Button key="back" onClick={() => setIsModalVisible(false)}>
            Hủy
          </Button>,
          <Button
            key="submit"
            type="primary"
            onClick={() => {
              updateRuleForm.validateFields().then(values => {
                updateRuleForm.resetFields();
                setIsModalVisible(false);
                console.log(values);
              });
            }}
          >
            Cập nhật
          </Button>,
        ]}
      >
        <Form form={updateRuleForm}>
          <Form.Item
            name="minMemberAge"
            label="Tuổi độc giả tối thiểu"
            rules={[{ required: true, message: 'Vui lòng nhập tuổi tối thiểu' }]}
          >
            <InputNumber min={1} placeholder="Tuổi độc giả tối thiểu" style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item
            name="maxMemberAge"
            label="Tuổi độc giả tối đa"
            rules={[
              { required: true, message: 'Vui lòng nhập tuổi tối đa' },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  const minValue = getFieldValue('minMemberAge');
                  if (!value || value > minValue) {
                    return Promise.resolve();
                  }
                  return Promise.reject(new Error('Tuổi tối đa phải lớn hơn tuổi tối thiểu'));
                },
              }),
            ]}
          >
            <InputNumber min={1} max={100} placeholder="Tuổi độc giả tối đa" style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item
            name="periodValidCard"
            label="Thời hạn thẻ độc giả (số tháng)"
            rules={[{ required: true, message: 'Vui lòng nhập thời hạn thẻ độc giả' }]}
          >
            <InputNumber min={1} placeholder="Thời hạn thẻ độc giả" style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item
            name="categoryBooks"
            label="Các thể loại sách nhập"
            rules={[{ required: true, message: 'Vui lòng chọn các thể loại sách nhập' }]}
          >
            <Select
              options={[
                { value: 'A', label: 'A' },
                { value: 'B', label: 'B' },
                { value: 'C', label: 'C' },
                { value: 'D', label: 'D' },
                { value: 'E', label: 'E' },
                { value: 'F', label: 'F' },
              ]}
              mode="multiple"
              placeholder="Các thể loại sách nhập"
            />
          </Form.Item>
          <Form.Item
            name="publicationYearGap"
            label="Khoảng cách năm xuất bản (số năm)"
            rules={[{ required: true, message: 'Vui lòng nhập khoảng cách năm xuất bản' }]}
          >
            <InputNumber min={0} placeholder="Khoảng cách năm xuất bản" style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item
            name="maxBookCanBorrow"
            label="Số lượng sách mượn tối đa"
            rules={[{ required: true, message: 'Vui lòng nhập số lượng sách mượn tối đa' }]}
          >
            <InputNumber min={1} placeholder="Số lượng sách mượn tối đa" style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item
            name="maxDayCanBorrow"
            label="Số ngày mượn tối đa"
            rules={[{ required: true, message: 'Vui lòng nhập số ngày mượn tối đa' }]}
          >
            <InputNumber min={1} placeholder="Số ngày mượn tối đa" style={{ width: '100%' }} />
          </Form.Item>
        </Form>
      </Modal>
      <Card loading={loading} style={{ marginTop: 20 }}>
        <Table loading={loading} columns={columnsRule} dataSource={dataSourceRule} pagination={false} />
      </Card>
    </>
  );
};

export default inject(Stores.RuleStore)(Rule);
