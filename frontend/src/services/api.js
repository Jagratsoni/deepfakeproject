import axios from 'axios';

// Set the base URL for the API
const API_URL = 'http://localhost:8000/api';

// Create an axios instance
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Upload a file for deepfake analysis
 * @param {File} file - The file to upload
 * @returns {Promise} - The analysis result
 */
export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  // Change Content-Type header for file uploads
  const config = {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  };
  
  try {
    const response = await apiClient.post('/detect', formData, config);
    return response.data;
  } catch (error) {
    console.error('Error uploading file:', error);
    throw error;
  }
};

/**
 * Get statistics about the model's performance
 * @returns {Promise} - The statistics data
 */
export const getStats = async () => {
  try {
    const response = await apiClient.get('/stats');
    return response.data;
  } catch (error) {
    console.error('Error fetching stats:', error);
    throw error;
  }
};

export default apiClient; 