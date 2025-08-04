// src/components/CandidateDashboard.jsx
import { useEffect, useState } from 'react';
import { api } from '../services/api';
import { setupSocket } from '../services/socket';

const CandidateDashboard = () => {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    status: '',
    position: '',
    dateRange: '30d'
  });

  useEffect(() => {
    const fetchCandidates = async () => {
      try {
        setLoading(true);
        const data = await api.getCandidates(filters);
        setCandidates(data);
      } catch (error) {
        console.error('Error fetching candidates:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCandidates();

    // Setup WebSocket for real-time updates
    const socket = setupSocket((newCandidate) => {
      setCandidates(prev => [newCandidate, ...prev]);
    });

    return () => {
      socket.close();
    };
  }, [filters]);

  const handleStatusChange = async (candidateId, newStatus) => {
    try {
      await api.updateCandidate(candidateId, { status: newStatus });
      setCandidates(prev => prev.map(c => 
        c._id === candidateId ? { ...c, status: newStatus } : c
      ));
    } catch (error) {
      console.error('Error updating candidate:', error);
    }
  };

  return (
    <div className="dashboard">
      <FilterPanel filters={filters} onFilterChange={setFilters} />
      
      {loading ? (
        <div className="loading-spinner">Loading candidates...</div>
      ) : (
        <CandidateList 
          candidates={candidates} 
          onStatusChange={handleStatusChange} 
        />
      )}
    </div>
  );
};
