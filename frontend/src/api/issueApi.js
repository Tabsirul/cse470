import { apiRequest } from './client';

export const reportIssue = async (token, issueData) => {
    return await apiRequest('/api/issues/report', {
        method: 'POST',
        token,
        body: issueData
    });
};

export const getMyReports = async (token) => {
    return await apiRequest('/api/issues/my-reports', { token });
};