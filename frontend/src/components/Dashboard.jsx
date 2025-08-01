import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
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

        if (!jobsRes.ok || !candidatesRes.ok || !applicationsRes.ok) {
          throw new Error('Failed to fetch data from API');
        }

        const [jobsData, candidatesData, applicationsData] = await Promise.all([
          jobsRes.json(),
          candidatesRes.json(),
          applicationsRes.json(),
        ]);

        // Calculate average matching score
        const matchScores = applicationsData
          .filter(app => typeof app.matching_score === 'number')
          .map(app => app.matching_score);

        const avgScore = matchScores.length
          ? matchScores.reduce((sum, score) => sum + score, 0) / matchScores.length
          : 0;

        setStats({
          totalJobs: jobsData.length,
          totalCandidates: candidatesData.length,
          totalApplications: applicationsData.length,
          avgMatchScore: avgScore,
        });
      } catch (err) {
        console.error('Error fetching data:', err);
        setError('Unable to load data. Please try again later.');
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
      <div className="flex items-center justify-center min-h-screen text-red-600 font-semibold">
        {error}
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

          {/* Add other tab contents here as needed */}
        </Tabs>
      </div>
    </div>
  );
};

export default Dashboard;

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
