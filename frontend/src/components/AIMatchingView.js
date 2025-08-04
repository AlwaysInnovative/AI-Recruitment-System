// src/components/AIMatchingView.js
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { API } from '../services/api';

const AIMatchingView = () => {
  const { applicationId } = useParams();
  const [matchingData, setMatchingData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMatchingData = async () => {
      try {
        const data = await API.get(`/match/${applicationId}`);
        setMatchingData(data);
      } catch (error) {
        console.error('Error fetching matching data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchMatchingData();
  }, [applicationId]);

  return (
    <div className="matching-container">
      {loading ? (
        <p>Loading matching analysis...</p>
      ) : (
        <div>
          <h2>AI Matching Analysis</h2>
          <div className="score-display">
            <h3>Match Score: {matchingData.score}%</h3>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${matchingData.score}%` }}
              ></div>
            </div>
          </div>
          <div className="breakdown">
            <h3>Key Matching Factors:</h3>
            <ul>
              {matchingData.breakdown.map((factor, index) => (
                <li key={index}>
                  <strong>{factor.category}:</strong> {factor.matchLevel} ({factor.score}%)
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default AIMatchingView;
