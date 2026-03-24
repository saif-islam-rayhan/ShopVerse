import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate, useLocation } from 'react-router-dom';
import '../styles/dashboard.css';

export const DashboardPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [showSuccess, setShowSuccess] = useState(false);

  useEffect(() => {
    if (location.state?.showSuccess) {
      setShowSuccess(true);
      const timer = setTimeout(() => setShowSuccess(false), 4000);
      return () => clearTimeout(timer);
    }
  }, [location.state]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="dashboard-container">
      {showSuccess && (
        <div className="success-banner">
          <div className="success-banner-content">
            <span className="success-icon">✓</span>
            <div>
              <h3>Login Successful!</h3>
              <p>Welcome back to ShopVerse, {user?.username}!</p>
            </div>
            <button 
              className="success-banner-close" 
              onClick={() => setShowSuccess(false)}
            >
              ✕
            </button>
          </div>
        </div>
      )}
      <div className="dashboard-header">
        <h1>Welcome, {user?.username}!</h1>
        <div className="header-actions">
          <button className="btn btn-primary" onClick={() => navigate('/profile')}>
            View Profile
          </button>
          <button className="btn btn-secondary" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="user-card">
          <h2>Your Account</h2>
          <div className="user-info">
            <div className="info-row">
              <label>Email:</label>
              <span>{user?.email}</span>
            </div>
            <div className="info-row">
              <label>Username:</label>
              <span>{user?.username}</span>
            </div>
            <div className="info-row">
              <label>Auth Provider:</label>
              <span className="provider-badge">{user?.auth_provider}</span>
            </div>
            <div className="info-row">
              <label>Member Since:</label>
              <span>{new Date(user?.created_at).toLocaleDateString()}</span>
            </div>
          </div>
        </div>

        <div className="coming-soon">
          <h3>More features coming soon!</h3>
          <p>Check back for shopping, orders, and more.</p>
        </div>
      </div>
    </div>
  );
};
