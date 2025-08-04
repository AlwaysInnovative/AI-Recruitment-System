// src/services/cache.js
const cache = new Map();

export const cachedFetch = async (url, options) => {
  const cacheKey = `${url}-${JSON.stringify(options)}`;
  
  if (cache.has(cacheKey)) {
    return cache.get(cacheKey);
  }

  const response = await fetch(url, options);
  const data = await response.json();
  
  // Cache for 5 minutes
  cache.set(cacheKey, data);
  setTimeout(() => cache.delete(cacheKey), 300000);

  return data;
};

// Update your api.js to use cachedFetch for GET requests
