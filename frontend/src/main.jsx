import React, { StrictMode, useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';  // Your Tailwind + custom CSS here
import App from './App.jsx';

const Root = () => {
  const [isDark, setIsDark] = useState(false);

  // On mount: detect system preference & set dark mode class
  useEffect(() => {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    setIsDark(prefersDark);
    updateHtmlClass(prefersDark);

    // Listen for changes to system preference and update accordingly
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handler = (e) => {
      setIsDark(e.matches);
      updateHtmlClass(e.matches);
    };
    mediaQuery.addEventListener('change', handler);

    return () => mediaQuery.removeEventListener('change', handler);
  }, []);

  // Update the <html> class to toggle dark mode
  const updateHtmlClass = (enabled) => {
    const html = document.documentElement;
    if (enabled) {
      html.classList.add('dark');
    } else {
      html.classList.remove('dark');
    }
  };

  // Optional: Toggle dark mode manually (could be passed down via context or props)
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

createRoot(document.getElementById('root')).render(<Root />);
