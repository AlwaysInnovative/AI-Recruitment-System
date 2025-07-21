import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { 
  Users, 
  Briefcase, 
  FileText, 
  TrendingUp, 
  Mail, 
  MessageSquare,
  Star,
  Clock,
  CheckCircle,
  XCircle,
  Search,
  Plus,
  Eye,
  Send
} from 'lucide-react';
import './Dashboard.css';

const API_BASE = 'https://0vhlizckd7jk.manussite.space/api';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalJobs: 0,
    totalCandidates: 0,
    totalApplications: 0,
    avgMatchScore: 0
  });
  
  const [jobs, setJobs] = useState([]);
  const [candidates, setCandidates] = useState([]);
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  // Fetch data from API
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      
      // Fetch jobs
      const jobsResponse = await fetch(`${API_BASE}/jobs`);
      const jobsData = await jobsResponse.json();
      setJobs(jobsData);
      
      // Fetch candidates
      const candidatesResponse = await fetch(`${API_BASE}/candidates`);
      const candidatesData = await candidatesResponse.json();
      setCandidates(candidatesData);
      
      // Fetch applications
      const applicationsResponse = await fetch(`${API_BASE}/applications`);
      const applicationsData = await applicationsResponse.json();
      setApplications(applicationsData);
      
      // Calculate stats
      const matchScores = applicationsData
        .filter(app => app.matching_score)
        .map(app => app.matching_score);
      const avgScore = matchScores.length > 0 
        ? matchScores.reduce((a, b) => a + b, 0) / matchScores.length 
        : 0;
      
      setStats({
        totalJobs: jobsData.length,
        totalCandidates: candidatesData.length,
        totalApplications: applicationsData.length,
        avgMatchScore: avgScore
      });
      
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      'applied': 'bg-blue-100 text-blue-800',
      'reviewed': 'bg-yellow-100 text-yellow-800',
      'interviewed': 'bg-purple-100 text-purple-800',
      'offered': 'bg-green-100 text-green-800',
      'hired': 'bg-green-200 text-green-900',
      'rejected': 'bg-red-100 text-red-800',
      'open': 'bg-green-100 text-green-800',
      'closed': 'bg-gray-100 text-gray-800',
      'filled': 'bg-blue-100 text-blue-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getMatchScoreColor = (score) => {
    if (score >= 0.8) return 'text-green-600 font-semibold';
    if (score >= 0.6) return 'text-yellow-600 font-semibold';
    return 'text-red-600 font-semibold';
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

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
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

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            {/* Stats Cards */}
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

            {/* Recent Activity */}
            <div className="grid gap-6 md:grid-cols-2">
              <Card>
                <CardHeader>
                  <CardTitle>Recent Applications</CardTitle>
                  <CardDescription>Latest candidate applications</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {applications.slice(0, 5).map((app) => (
                      <div key={app.id} className="flex items-center justify-between p-3 border rounded-lg">
                        <div>
                          <p className="font-medium">
                            {app.candidate?.first_name} {app.candidate?.last_name}
                          </p>
                          <p className="text-sm text-muted-foreground">{app.job?.title}</p>
                        </div>
                        <div className="text-right">
                          {app.matching_score && (
                            <p className={`text-sm ${getMatchScoreColor(app.matching_score)}`}>
                              {(app.matching_score * 100).toFixed(0)}% match
                            </p>
                          )}
                          <Badge className={getStatusColor(app.status)}>
                            {app.status}
                          </Badge>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Top Jobs</CardTitle>
                  <CardDescription>Most popular job postings</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {jobs.slice(0, 5).map((job) => {
                      const jobApplications = applications.filter(app => app.job_id === job.id);
                      return (
                        <div key={job.id} className="flex items-center justify-between p-3 border rounded-lg">
                          <div>
                            <p className="font-medium">{job.title}</p>
                            <p className="text-sm text-muted-foreground">{job.location}</p>
                          </div>
                          <div className="text-right">
                            <p className="text-sm font-medium">{jobApplications.length} applications</p>
                            <Badge className={getStatusColor(job.status)}>
                              {job.status}
                            </Badge>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Jobs Tab */}
          <TabsContent value="jobs" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Job Postings</CardTitle>
                <CardDescription>Manage your job postings and requirements</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {jobs.map((job) => {
                    const jobApplications = applications.filter(app => app.job_id === job.id);
                    const avgScore = jobApplications.length > 0 
                      ? jobApplications.reduce((sum, app) => sum + (app.matching_score || 0), 0) / jobApplications.length
                      : 0;
                    
                    return (
                      <Card key={job.id} className="hover:shadow-md transition-shadow">
                        <CardContent className="p-6">
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <h3 className="text-lg font-semibold">{job.title}</h3>
                              <p className="text-muted-foreground mb-2">{job.location}</p>
                              <p className="text-sm mb-4">{job.description}</p>
                              <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                                <span>{jobApplications.length} applications</span>
                                {avgScore > 0 && (
                                  <span>Avg match: {(avgScore * 100).toFixed(0)}%</span>
                                )}
                                <span>Salary: {job.salary_range || 'Not specified'}</span>
                              </div>
                            </div>
                            <div className="flex items-center space-x-2">
                              <Badge className={getStatusColor(job.status)}>
                                {job.status}
                              </Badge>
                              <Button variant="outline" size="sm">
                                <Eye className="h-4 w-4 mr-1" />
                                View
                              </Button>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Candidates Tab */}
          <TabsContent value="candidates" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Candidate Pool</CardTitle>
                <CardDescription>Browse and manage candidate profiles</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {candidates.map((candidate) => {
                    const candidateApplications = applications.filter(app => app.candidate_id === candidate.id);
                    
                    return (
                      <Card key={candidate.id} className="hover:shadow-md transition-shadow">
                        <CardContent className="p-6">
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <h3 className="text-lg font-semibold">
                                {candidate.first_name} {candidate.last_name}
                              </h3>
                              <p className="text-muted-foreground mb-2">{candidate.email}</p>
                              <div className="flex items-center space-x-4 text-sm text-muted-foreground mb-3">
                                <span>{candidate.total_experience_years || 0} years experience</span>
                                <span>{candidate.phone || 'No phone'}</span>
                                <span>{candidateApplications.length} applications</span>
                              </div>
                              {candidate.skills && candidate.skills.length > 0 && (
                                <div className="flex flex-wrap gap-1">
                                  {candidate.skills.slice(0, 5).map((skill, index) => (
                                    <Badge key={index} variant="secondary" className="text-xs">
                                      {skill}
                                    </Badge>
                                  ))}
                                  {candidate.skills.length > 5 && (
                                    <Badge variant="outline" className="text-xs">
                                      +{candidate.skills.length - 5} more
                                    </Badge>
                                  )}
                                </div>
                              )}
                            </div>
                            <div className="flex items-center space-x-2">
                              <Button variant="outline" size="sm">
                                <Eye className="h-4 w-4 mr-1" />
                                Profile
                              </Button>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Applications Tab */}
          <TabsContent value="applications" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Applications</CardTitle>
                <CardDescription>Review and manage job applications</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {applications.map((app) => (
                    <Card key={app.id} className="hover:shadow-md transition-shadow">
                      <CardContent className="p-6">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center space-x-3 mb-2">
                              <h3 className="text-lg font-semibold">
                                {app.candidate?.first_name} {app.candidate?.last_name}
                              </h3>
                              <Badge className={getStatusColor(app.status)}>
                                {app.status}
                              </Badge>
                            </div>
                            <p className="text-muted-foreground mb-2">
                              Applied for: <span className="font-medium">{app.job?.title}</span>
                            </p>
                            <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                              <span>Applied: {new Date(app.application_date).toLocaleDateString()}</span>
                              {app.matching_score && (
                                <span className={getMatchScoreColor(app.matching_score)}>
                                  AI Match: {(app.matching_score * 100).toFixed(0)}%
                                </span>
                              )}
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            {app.matching_score && (
                              <div className="text-right mr-4">
                                <div className={`text-2xl font-bold ${getMatchScoreColor(app.matching_score)}`}>
                                  {(app.matching_score * 100).toFixed(0)}%
                                </div>
                                <div className="text-xs text-muted-foreground">Match Score</div>
                              </div>
                            )}
                            <Button variant="outline" size="sm">
                              <Eye className="h-4 w-4 mr-1" />
                              Review
                            </Button>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Communications Tab */}
          <TabsContent value="communications" className="space-y-6">
            <div className="grid gap-6 md:grid-cols-2">
              <Card>
                <CardHeader>
                  <CardTitle>Email Templates</CardTitle>
                  <CardDescription>Manage automated email communications</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between p-3 border rounded-lg">
                      <div>
                        <p className="font-medium">Application Acknowledgment</p>
                        <p className="text-sm text-muted-foreground">Sent when application is received</p>
                      </div>
                      <Button variant="outline" size="sm">
                        <Mail className="h-4 w-4 mr-1" />
                        Edit
                      </Button>
                    </div>
                    <div className="flex items-center justify-between p-3 border rounded-lg">
                      <div>
                        <p className="font-medium">Information Request</p>
                        <p className="text-sm text-muted-foreground">Request additional candidate details</p>
                      </div>
                      <Button variant="outline" size="sm">
                        <Mail className="h-4 w-4 mr-1" />
                        Edit
                      </Button>
                    </div>
                    <div className="flex items-center justify-between p-3 border rounded-lg">
                      <div>
                        <p className="font-medium">Interview Invitation</p>
                        <p className="text-sm text-muted-foreground">Schedule candidate interviews</p>
                      </div>
                      <Button variant="outline" size="sm">
                        <Mail className="h-4 w-4 mr-1" />
                        Edit
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Communication Stats</CardTitle>
                  <CardDescription>Email and SMS delivery metrics</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Emails Sent Today</span>
                      <span className="font-semibold">24</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">SMS Sent Today</span>
                      <span className="font-semibold">12</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Delivery Rate</span>
                      <span className="font-semibold text-green-600">98.5%</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Response Rate</span>
                      <span className="font-semibold text-blue-600">67.2%</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default Dashboard;

