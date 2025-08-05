export interface SalaryRange {
  min: number;
  max: number;
}

export type JobStatus = 'draft' | 'open' | 'closed';

export interface JobCreate {
  title: string;
  description: string;
  requirements: string;
  location: string;
  salary_range?: SalaryRange;
  status?: JobStatus;
}

export interface Job extends JobCreate {
  id: number;
  hiring_manager_id: number;
  created_at: string;
  updated_at: string;
}
