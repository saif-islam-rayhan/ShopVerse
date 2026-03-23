import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import '../styles/dashboard.css';

export const DashboardPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Welcome, {user?.username}!</h1>
        <button className="btn btn-secondary" onClick={handleLogout}>
          Logout
        </button>
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
