// src/components/FilterPanel.jsx
const FilterPanel = ({ filters, onFilterChange }) => {
  const [positions, setPositions] = useState([]);

  useEffect(() => {
    const fetchPositions = async () => {
      const jobs = await api.getJobs();
      setPositions(jobs.map(job => job.title));
    };
    fetchPositions();
  }, []);

  return (
    <div className="filter-panel">
      <select
        value={filters.status}
        onChange={(e) => onFilterChange({ ...filters, status: e.target.value })}
      >
        <option value="">All Statuses</option>
        <option value="new">New</option>
        <option value="reviewed">Reviewed</option>
        <option value="interview">Interview</option>
        <option value="hired">Hired</option>
        <option value="rejected">Rejected</option>
      </select>

      <select
        value={filters.position}
        onChange={(e) => onFilterChange({ ...filters, position: e.target.value })}
      >
        <option value="">All Positions</option>
        {positions.map(position => (
          <option key={position} value={position}>{position}</option>
        ))}
      </select>

      <select
        value={filters.dateRange}
        onChange={(e) => onFilterChange({ ...filters, dateRange: e.target.value })}
      >
        <option value="7d">Last 7 days</option>
        <option value="30d">Last 30 days</option>
        <option value="90d">Last 90 days</option>
        <option value="all">All time</option>
      </select>
    </div>
  );
};
