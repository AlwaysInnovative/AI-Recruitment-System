import { useState, useEffect } from 'react';
import apiClient from '../api/apiClient';

export default function useApi(endpoint, initialData = []) {
  const [data, setData] = useState(initialData);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await apiClient.get(endpoint);
        setData(response.data);
      } catch (err) {
        setError(err.message || 'Failed to fetch data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [endpoint]);

  return { data, loading, error, refetch: () => {
    setLoading(true);
    setError(null);
    useEffect(() => fetchData(), [endpoint]);
  } };
}
