import { createContext, useContext, useState, useEffect } from 'react';
import { getCurrentUser, logout as logoutService } from '../services/authService';

// Create Auth Context
const AuthContext = createContext(null);

/**
 * Auth Provider Component
 * Provides authentication state and methods to all child components
 */
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('access_token') || null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(!!token);

  // Check if user is authenticated on component mount
  useEffect(() => {
    const checkAuth = async () => {
      if (token) {
        try {
          setIsLoading(true);
          const userData = await getCurrentUser();
          setUser(userData);
          setIsAuthenticated(true);
        } catch (err) {
          setError(err.message);
          setToken(null);
          setIsAuthenticated(false);
          localStorage.removeItem('access_token');
        } finally {
          setIsLoading(false);
        }
      }
    };

    checkAuth();
  }, [token]);

  /**
   * Store authentication response and update state
   */
  const storeAuth = (authResponse) => {
    const { user, token } = authResponse;
    localStorage.setItem('access_token', token.access_token);
    localStorage.setItem('user', JSON.stringify(user));
    setToken(token.access_token);
    setUser(user);
    setIsAuthenticated(true);
    setError(null);
  };

  /**
   * Logout user
   */
  const logout = () => {
    logoutService();
    setUser(null);
    setToken(null);
    setIsAuthenticated(false);
    setError(null);
  };

  const contextValue = {
    user,
    token,
    isLoading,
    error,
    isAuthenticated,
    storeAuth,
    logout,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

/**
 * Custom hook to use Auth Context
 */
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
