import React, { useState } from 'react';
import { Form, Input, Button, message, InputNumber, Select, Card, Row, Col } from 'antd';
import { createJob } from '../../api/jobs';
import { JobCreate } from '../../types';
import RichTextEditor from './RichTextEditor';

const { TextArea } = Input;
const { Option } = Select;

interface JobFormProps {
  onSuccess?: () => void;
}

const JobForm: React.FC<JobFormProps> = ({ onSuccess }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [description, setDescription] = useState('');
  const [requirements, setRequirements] = useState('');

  const onFinish = async (values: JobCreate) => {
    try {
      setLoading(true);
      const completeValues = {
        ...values,
        description,
        requirements
      };
      await createJob(completeValues);
      message.success('Job posted successfully!');
      form.resetFields();
      setDescription('');
      setRequirements('');
      if (onSuccess) onSuccess();
    } catch (error) {
      message.error('Failed to create job posting');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card title="Create New Job Posting" bordered={false}>
      <Form
        form={form}
        layout="vertical"
        onFinish={onFinish}
        initialValues={{ status: 'open' }}
      >
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="title"
              label="Job Title"
              rules={[{ required: true, message: 'Please input job title!' }]}
            >
              <Input placeholder="e.g. Senior Software Engineer" />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="location"
              label="Location"
              rules={[{ required: true, message: 'Please input job location!' }]}
            >
              <Input placeholder="e.g. Remote, New York, etc." />
            </Form.Item>
          </Col>
        </Row>

        <Form.Item
          label="Job Description"
          required
        >
          <RichTextEditor 
            value={description}
            onChange={setDescription}
            placeholder="Enter detailed job description..."
          />
        </Form.Item>

        <Form.Item
          label="Requirements"
          required
        >
          <RichTextEditor
            value={requirements}
            onChange={setRequirements}
            placeholder="List all job requirements..."
          />
        </Form.Item>

        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              name={['salary_range', 'min']}
              label="Minimum Salary"
              rules={[{ required: true, message: 'Please input minimum salary' }]}
            >
              <InputNumber
                style={{ width: '100%' }}
                min={0}
                formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                parser={value => value?.replace(/\$\s?|(,*)/g, '') || ''}
              />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name={['salary_range', 'max']}
              label="Maximum Salary"
              rules={[{ required: true, message: 'Please input maximum salary' }]}
            >
              <InputNumber
                style={{ width: '100%' }}
                min={0}
                formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                parser={value => value?.replace(/\$\s?|(,*)/g, '') || ''}
              />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="status"
              label="Status"
              rules={[{ required: true }]}
            >
              <Select>
                <Option value="open">Open</Option>
                <Option value="closed">Closed</Option>
                <Option value="draft">Draft</Option>
              </Select>
            </Form.Item>
          </Col>
        </Row>

        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading} size="large">
            Publish Job
          </Button>
        </Form.Item>
      </Form>
    </Card>
  );
};

export default JobForm;
