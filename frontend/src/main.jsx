import React, { StrictMode, useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css'; // Tailwind + custom styles
import App from './App.jsx';

// Helper to update <html> class for dark mode
const updateHtmlClass = (enabled) => {
  const html = document.documentElement;
  if (enabled) {
    html.classList.add('dark');
  } else {
    html.classList.remove('dark');
  }
};

const Root = () => {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const prefersDark = mediaQuery.matches;
    setIsDark(prefersDark);
    updateHtmlClass(prefersDark);

    const handler = (e) => {
      setIsDark(e.matches);
      updateHtmlClass(e.matches);
    };

    // Use modern event listeners, fallback for Safari
    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', handler);
    } else if (mediaQuery.addListener) {
      mediaQuery.addListener(handler);
    }

    return () => {
      if (mediaQuery.removeEventListener) {
        mediaQuery.removeEventListener('change', handler);
      } else if (mediaQuery.removeListener) {
        mediaQuery.removeListener(handler);
      }
    };
  }, []);

  const toggleDarkMode = () => {
    const newDark = !isDark;
    setIsDark(newDark);
    updateHtmlClass(newDark);
  };

  return (
    <StrictMode>
      <App isDark={isDark} toggleDarkMode={toggleDarkMode} />
    </StrictMode>
  );
};

// Render app
const container = document.getElementById('root');
if (container) {
  createRoot(container).render(<Root />);
} else {
  console.error('❌ Root element not found!');
}
