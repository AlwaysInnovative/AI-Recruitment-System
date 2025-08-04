// src/components/ErrorBoundary.jsx
import { useState } from 'react';

const ErrorBoundary = ({ children }) => {
  const [hasError, setHasError] = useState(false);

  const handleRetry = () => {
    setHasError(false);
    window.location.reload();
  };

  return (
    <>
      {hasError ? (
        <div className="error-fallback">
          <h3>Something went wrong</h3>
          <p>We're having trouble loading this content.</p>
          <button onClick={handleRetry}>Retry</button>
        </div>
      ) : (
        children
      )}
    </>
  );
};

// Usage in your app:
<ErrorBoundary>
  <CandidateDashboard />
</ErrorBoundary>
