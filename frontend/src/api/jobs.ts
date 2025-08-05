import { client } from './client';
import { Job, JobCreate } from '../types';

export const fetchJobs = async (): Promise<Job[]> => {
  const response = await client.get('/jobs');
  return response.data;
};

export const fetchMyJobs = async (status?: string): Promise<Job[]> => {
  const params = status ? { status } : {};
  const response = await client.get('/jobs/my-jobs', { params });
  return response.data;
};

export const createJob = async (jobData: JobCreate): Promise<Job> => {
  const response = await client.post('/jobs', jobData);
  return response.data;
};

export const updateJobStatus = async (jobId: number, status: string): Promise<Job> => {
  const response = await client.patch(`/jobs/${jobId}/status`, { status });
  return response.data;
};
