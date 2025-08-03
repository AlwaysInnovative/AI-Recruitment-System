import React, { useState, useEffect } from 'react';
import { 
  Card, 
  CardContent, 
  CardHeader, 
  CardTitle 
} from '../../components/ui/card';  // Changed to relative path
import { Button } from '../../components/ui/button';  // Changed to relative path
import { 
  Tabs, 
  TabsContent, 
  TabsList, 
  TabsTrigger 
} from '../../components/ui/tabs';  // Changed to relative path
import { 
  Search, 
  Plus, 
  Briefcase, 
  Users, 
  FileText, 
  TrendingUp 
} from 'lucide-react';
import './Dashboard.css';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'https://0vhlizckd7jk.manussite.space/api';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalJobs: 0,
    totalCandidates: 0,
    totalApplications: 0,
    avgMatchScore: 0,
  });

  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [jobsRes, candidatesRes, applicationsRes] = await Promise.all([
          fetch(`${API_BASE}/jobs`),
          fetch(`${API_BASE}/candidates`),
          fetch(`${API_BASE}/applications`)
        ]);

        // Enhanced error handling
        if (!jobsRes.ok) throw new Error('Failed to fetch jobs');
        if (!candidatesRes.ok) throw new Error('Failed to fetch candidates');
        if (!applicationsRes.ok) throw new Error('Failed to fetch applications');

        const [jobsData, candidatesData, applicationsData] = await Promise.all([
          jobsRes.json(),
          candidatesRes.json(),
          applicationsRes.json(),
        ]);

        // Calculate average matching score with additional validation
        const validScores = applicationsData
          .filter(app => typeof app.matching_score === 'number' && !isNaN(app.matching_score))
          .map(app => Math.min(Math.max(app.matching_score, 0), 1)); // Ensure score is between 0-1

        const avgScore = validScores.length > 0
          ? (validScores.reduce((sum, score) => sum + score, 0) / validScores.length)
          : 0;

        setStats({
          totalJobs: jobsData.length || 0,
          totalCandidates: candidatesData.length || 0,
          totalApplications: applicationsData.length || 0,
          avgMatchScore: avgScore,
        });
      } catch (err) {
        console.error('API Error:', err);
        setError(err.message || 'Unable to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="bg-red-50 p-6 rounded-lg max-w-md text-center">
          <h2 className="text-xl font-semibold text-red-600 mb-2">Loading Error</h2>
          <p className="text-red-700">{error}</p>
          <button 
            onClick={() => window.location.reload()}
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b bg-card">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-foreground">AI Recruitment Dashboard</h1>
            <p className="text-muted-foreground">Intelligent hiring made simple</p>
          </div>
          <div className="flex items-center space-x-4">
            <Button variant="outline" size="sm">
              <Search className="h-4 w-4 mr-2" />
              Search
            </Button>
            <Button size="sm">
              <Plus className="h-4 w-4 mr-2" />
              New Job
            </Button>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="jobs">Jobs</TabsTrigger>
            <TabsTrigger value="candidates">Candidates</TabsTrigger>
            <TabsTrigger value="applications">Applications</TabsTrigger>
            <TabsTrigger value="communications">Communications</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              <StatCard
                title="Total Jobs"
                value={stats.totalJobs}
                icon={Briefcase}
                description="Active job postings"
              />
              <StatCard
                title="Total Candidates"
                value={stats.totalCandidates}
                icon={Users}
                description="Registered candidates"
              />
              <StatCard
                title="Applications"
                value={stats.totalApplications}
                icon={FileText}
                description="Total applications received"
              />
              <StatCard
                title="Avg Match Score"
                value={`${(stats.avgMatchScore * 100).toFixed(1)}%`}
                icon={TrendingUp}
                description="AI matching accuracy"
              />
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

const StatCard = ({ title, value, icon: Icon, description }) => (
  <Card className="hover:shadow-lg transition-shadow duration-200">
    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
      <CardTitle className="text-sm font-medium">{title}</CardTitle>
      <Icon className="h-4 w-4 text-muted-foreground" />
    </CardHeader>
    <CardContent>
      <div className="text-2xl font-bold">{value}</div>
      <p className="text-xs text-muted-foreground">{description}</p>
    </CardContent>
  </Card>
);

export default Dashboard;
