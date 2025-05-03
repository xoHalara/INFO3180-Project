/*
  reports.js - API service for Jam-Date report-related endpoints
  Provides functions for creating and fetching reports.
*/

import api from './api'

/**
 * Create a new report.
 * @param {Object} data - Report data containing reported_user_id and reason
 */
export const createReport = (data) => api.post('/reports/', data)

/**
 * Fetch all reports with optional sorting.
 * @param {Object} params - Query parameters for sorting (sort_by and order)
 */
export const fetchReports = (params = {}) => api.get('/reports/', { params }) 