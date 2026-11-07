import { apiRequest } from './client';

export const fetchCourses = async (searchQuery = '') => {
  const query = searchQuery ? `?search=${encodeURIComponent(searchQuery)}` : '';
  return await apiRequest(`/api/courses/${query}`, { method: 'GET' });
};