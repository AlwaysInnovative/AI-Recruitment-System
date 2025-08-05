import React, { useState } from 'react';
import { Form, Input, Button, message, InputNumber, Select } from 'antd';
import { createJob } from '../../api/jobs';
import { JobCreate } from '../../types';

const { TextArea } = Input;
const { Option } = Select;

const JobForm: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const onFinish = async (values: JobCreate) => {
    try {
      setLoading(true);
      await createJob(values);
      message.success('Job posted successfully!');
      form.resetFields();
    } catch (error) {
      message.error('Failed to create job posting');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={onFinish}
      initialValues={{ status: 'open' }}
    >
      <Form.Item
        name="title"
        label="Job Title"
        rules={[{ required: true, message: 'Please input job title!' }]}
      >
        <Input placeholder="Senior Software Engineer" />
      </Form.Item>

      <Form.Item
        name="description"
        label="Job Description"
        rules={[{ required: true, message: 'Please input job description!' }]}
      >
        <TextArea rows={4} />
      </Form.Item>

      <Form.Item
        name="requirements"
        label="Requirements"
        rules={[{ required: true, message: 'Please input job requirements!' }]}
      >
        <TextArea rows={4} />
      </Form.Item>

      <Form.Item
        name="location"
        label="Location"
        rules={[{ required: true, message: 'Please input job location!' }]}
      >
        <Input placeholder="Remote, New York, etc." />
      </Form.Item>

      <Form.Item label="Salary Range">
        <Input.Group compact>
          <Form.Item
            name={['salary_range', 'min']}
            noStyle
            rules={[{ required: true, message: 'Min salary required' }]}
          >
            <InputNumber
              style={{ width: '45%' }}
              placeholder="Minimum"
              min={0}
              formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
            />
          </Form.Item>
          <Form.Item
            name={['salary_range', 'max']}
            noStyle
            rules={[{ required: true, message: 'Max salary required' }]}
          >
            <InputNumber
              style={{ width: '45%', marginLeft: '10%' }}
              placeholder="Maximum"
              min={0}
              formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
            />
          </Form.Item>
        </Input.Group>
      </Form.Item>

      <Form.Item
        name="status"
        label="Status"
        rules={[{ required: true }]}
      >
        <Select>
          <Option value="open">Open</Option>
          <Option value="closed">Closed</Option>
        </Select>
      </Form.Item>

      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading}>
          Post Job
        </Button>
      </Form.Item>
    </Form>
  );
};

export default JobForm;
