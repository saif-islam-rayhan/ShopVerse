import apiClient from './apiClient';

/**
 * Register a new user
 * @param {string} email - User email
 * @param {string} password - User password
 * @param {string} username - User username
 * @returns {Promise} Auth response with user and token
 */
export const registerUser = async (email, password, username) => {
  const response = await apiClient.post('/auth/register', {
    email,
    password,
    username,
  });
  return response.data;
};

/**
 * Login user with email and password
 * @param {string} email - User email
 * @param {string} password - User password
 * @returns {Promise} Auth response with user and token
 */
export const loginUser = async (email, password) => {
  const response = await apiClient.post('/auth/login', {
    email,
    password,
  });
  return response.data;
};

/**
 * Google OAuth login
 * @param {string} token - Google ID token
 * @returns {Promise} Auth response with user and token
 */
export const googleLogin = async (token) => {
  const response = await apiClient.post('/auth/google', {
    token,
  });
  return response.data;
};

/**
 * Get current user information
 * @returns {Promise} User data
 */
export const getCurrentUser = async () => {
  const response = await apiClient.get('/auth/me');
  return response.data;
};

/**
 * Logout user (client-side)
 */
export const logout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('user');
};

/**
 * Get user profile
 * @returns {Promise} User profile data
 */
export const getProfile = async () => {
  const response = await apiClient.get('/auth/profile');
  return response.data;
};

/**
 * Update user profile
 * @param {Object} profileData - Profile data to update
 * @param {string} profileData.full_name - User full name
 * @param {string} profileData.address - User address
 * @param {string} profileData.profile_picture - Profile picture URL
 * @returns {Promise} Updated profile data
 */
export const updateProfile = async (profileData) => {
  const response = await apiClient.put('/auth/profile', profileData);
  return response.data;
};
