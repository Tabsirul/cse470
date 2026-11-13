import { apiRequest } from './client';

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export const uploadMaterial = async (token, formData) => {
  const response = await fetch(`${API_URL}/api/materials/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: formData, 
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.detail || "Upload failed");
  }
  return response.json();
};

export const getMaterials = async (token, course = '') => {
  const query = course ? `?course=${encodeURIComponent(course)}` : '';
  return await apiRequest(`/api/materials/${query}`, { token });
};