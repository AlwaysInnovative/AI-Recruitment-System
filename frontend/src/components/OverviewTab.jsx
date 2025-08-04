import React, { useState, useEffect } from 'react';
import { Card, Statistic, Table, Tag, Space, Spin, Row, Col } from 'antd';
import { 
  DollarOutlined, 
  UserOutlined, 
  FileDoneOutlined, 
  AuditOutlined,
  RiseOutlined,
  FallOutlined
} from '@ant-design/icons';
import { Pie, Bar } from 'react-chartjs-2';
import api from '../services/api';
import Chart from 'chart.js/auto';

const OverviewTab = () => {
  const [stats, setStats] = useState(null);
  const [activity, setActivity] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, activityRes] = await Promise.all([
          api.get('/overview/stats'),
          api.get('/overview/activity')
        ]);
        setStats(statsRes.data);
        setActivity(activityRes.data.activities);
      } catch (error) {
        console.error('Error fetching overview data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <Spin size="large" className="loading-spinner" />;

  // Application Status Chart Data
  const appStatusData = {
    labels: Object.keys(stats.applications.by_status),
    datasets: [{
      data: Object.values(stats.applications.by_status),
      backgroundColor: [
        '#1890ff', // applied
        '#13c2c2', // reviewed
        '#722ed1', // interviewed
        '#52c41a', // hired
        '#f5222d'  // rejected
      ],
      borderWidth: 1
    }]
  };

  // Hiring Trends Chart Data
  const hiringTrendsData = {
    labels: ['This Week', 'This Month', 'All Time'],
    datasets: [{
      label: 'Hires',
      data: [
        stats.applications.hires.week,
        stats.applications.hires.month,
        stats.applications.by_status.hired
      ],
      backgroundColor: '#52c41a'
    }]
  };

  // Activity Table Columns
  const activityColumns = [
    {
      title: 'Type',
      dataIndex: 'type',
      key: 'type',
      render: type => (
        <Tag color={type === 'application' ? 'geekblue' : 'green'}>
          {type.toUpperCase()}
        </Tag>
      )
    },
    {
      title: 'Details',
      key: 'details',
      render: (_, record) => (
        <Space direction="vertical" size="small">
          {record.type === 'application' ? (
            <>
              <strong>{record.candidate}</strong>
              <span>For: {record.job}</span>
              <Tag color={
                record.status === 'hired' ? 'green' : 
                record.status === 'rejected' ? 'red' : 'blue'
              }>
                {record.status.toUpperCase()}
              </Tag>
            </>
          ) : (
            <>
              <strong>Commission: {record.agency}</strong>
              <span>Amount: ${record.amount.toFixed(2)}</span>
              <Tag color={record.status === 'paid' ? 'green' : 'orange'}>
                {record.status.toUpperCase()}
              </Tag>
            </>
          )}
        </Space>
      )
    },
    {
      title: 'Date',
      dataIndex: 'time',
      key: 'time',
      render: time => new Date(time).toLocaleString()
    }
  ];

  return (
    <div className="overview-tab">
      {/* Summary Statistics Row */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Open Jobs"
              value={stats.jobs.active}
              prefix={<AuditOutlined />}
              suffix={`/ ${stats.jobs.total}`}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Active Candidates"
              value={stats.candidates.active}
              prefix={<UserOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="New Applications"
              value={stats.applications.by_status.applied}
              prefix={<FileDoneOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Pending Commissions"
              value={stats.financials.pending_commissions}
              prefix={<DollarOutlined />}
              valueStyle={{ color: '#cf1322' }}
            />
          </Card>
        </Col>
      </Row>

      {/* Charts Row */}
      <Row gutter={24} style={{ marginBottom: 24 }}>
        <Col span={12}>
          <Card title="Application Status">
            <Pie 
              data={appStatusData}
              options={{ responsive: true }}
            />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="Hiring Trends">
            <Bar 
              data={hiringTrendsData}
              options={{ responsive: true }}
            />
          </Card>
        </Col>
      </Row>

      {/* Recent Activity */}
      <Card title="Recent Activity">
        <Table
          columns={activityColumns}
          dataSource={activity}
          rowKey="id"
          pagination={{ pageSize: 5 }}
        />
      </Card>
    </div>
  );
};

export default OverviewTab;
