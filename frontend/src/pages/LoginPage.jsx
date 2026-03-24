import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { GoogleLogin } from '@react-oauth/google';
import { loginUser, googleLogin } from '../services/authService';
import { useAuth } from '../context/AuthContext';
import '../styles/auth.css';

export const LoginPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { storeAuth } = useAuth();
  
  // FIXED: Hardcoded Client ID to match App.jsx
  const hasGoogleConfig = true;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.email || !formData.password) {
      setError('Email and password are required');
      return;
    }
    
    console.log('Attempting login to backend...');

    setLoading(true);
    try {
      const authResponse = await loginUser(formData.email, formData.password);
      storeAuth(authResponse);
      setSuccess(`✓ Welcome back, ${authResponse.user?.email}! Login successful!`);
      setError('');
      // Redirect to dashboard after 1.5 seconds
      setTimeout(() => {
        navigate('/dashboard', { state: { showSuccess: true } });
      }, 1500);
    } catch (err) {
      console.error('Login Error Details:', err);
      const errorMsg = err.response?.data?.detail || `Login failed: ${err.message}`;
      setError(errorMsg);
      setSuccess('');
    } finally {
      setLoading(false);
    }
  };

  // Google login handler - using standard GoogleLogin component for ID Token
  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      console.log("1. Google Credential Received:", credentialResponse);
      
      if (!credentialResponse.credential) {
        throw new Error("No credential received from Google");
      }

      setLoading(true);
      setError('');
      
      // Pass the credential (ID token) to backend instead of access_token
      console.log("2. Sending token to backend for database save...");
      const authResponse = await googleLogin(credentialResponse.credential);
      console.log("3. Backend Success Response:", authResponse);
      storeAuth(authResponse);
      
      // Show success message and redirect to dashboard/home
      setSuccess(`✓ Welcome, ${authResponse.user?.email}! Successfully signed in with Google!`);
      setTimeout(() => {
        navigate('/dashboard', { replace: true, state: { showSuccess: true } });
      }, 1000);
    } catch (err) {
      console.error("Full Login Error:", err);
      let errorMsg = 'Google login failed. Please try again.';
      
      // Check for backend error message
      if (err.response) {
        // Backend returned an error (400, 401, 500)
        console.error("Backend Error Data:", err.response.data);
        errorMsg = err.response.data?.detail || `Server Error: ${err.response.status}`;
      } else if (err.request) {
        // Network error (Backend not reachable)
        errorMsg = "Network Error: Cannot connect to backend server. Is it running?";
      } else {
        errorMsg = err.message || "Unknown error occurred";
      }
      
      setError(errorMsg);
      // Show alert so user definitely sees the specific error
      alert(`Login Failed: ${errorMsg}`);
      setLoading(false);
    }
  };

  const handleGoogleError = () => {
    console.error("Google Popup Closed or Failed to Load");
    setError('Failed to sign in with Google. Please check your connection.');
    alert("Google Popup Failed. Check console for details.");
    setLoading(false);
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>Welcome Back</h1>
        <p className="auth-subtitle">Sign in to your ShopVerse account</p>

        {success && <div className="success-message">{success}</div>}
        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="your@email.com"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="••••••••"
              required
            />
            <a href="/forgot-password" className="forgot-password">
              Forgot password?
            </a>
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Signing In...' : 'Sign In'}
          </button>
        </form>

        {hasGoogleConfig && (
          <>
            <div className="divider">Or</div>

            <div className="google-login-wrapper" style={{ display: 'flex', justifyContent: 'center' }}>
              <GoogleLogin
                onSuccess={handleGoogleSuccess}
                onError={handleGoogleError}
                theme="filled_blue"
                shape="pill"
                text="signin_with"
              />
            </div>
          </>
        )}

        <div className="auth-footer">
          <p>
            Don't have an account?{' '}
            <a href="/register">Create one here</a>
          </p>
        </div>
      </div>
    </div>
  );
};
