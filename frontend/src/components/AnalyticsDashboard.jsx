// src/components/AnalyticsDashboard.jsx
import { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { api } from '../services/api';

const AnalyticsDashboard = () => {
  const [stats, setStats] = useState(null);
  const [timeRange, setTimeRange] = useState('30d');

  useEffect(() => {
    const fetchStats = async () => {
      const data = await api.getDashboardStats({ range: timeRange });
      setStats(data);
    };
    fetchStats();
  }, [timeRange]);

  return (
    <div className="analytics-dashboard">
      <h2>Recruitment Analytics</h2>
      
      <div className="time-range-selector">
        <button onClick={() => setTimeRange('7d')} className={timeRange === '7d' ? 'active' : ''}>
          7 Days
        </button>
        <button onClick={() => setTimeRange('30d')} className={timeRange === '30d' ? 'active' : ''}>
          30 Days
        </button>
        <button onClick={() => setTimeRange('90d')} className={timeRange === '90d' ? 'active' : ''}>
          90 Days
        </button>
      </div>

      {stats && (
        <div className="charts">
          <div className="chart-container">
            <h3>Applications Over Time</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={stats.applicationsOverTime}>
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="count" stroke="#8884d8" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="stats-grid">
            <div className="stat-card">
              <h4>Total Candidates</h4>
              <p>{stats.totalCandidates}</p>
            </div>
            <div className="stat-card">
              <h4>Hiring Rate</h4>
              <p>{stats.hiringRate}%</p>
            </div>
            <div className="stat-card">
              <h4>Avg. Time to Hire</h4>
              <p>{stats.avgTimeToHire} days</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
