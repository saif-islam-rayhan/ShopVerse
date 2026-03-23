import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useGoogleLogin } from '@react-oauth/google';
import { loginUser, googleLogin } from '../services/authService';
import { useAuth } from '../context/AuthContext';
import '../styles/auth.css';

export const LoginPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { storeAuth } = useAuth();

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

    setLoading(true);
    try {
      const authResponse = await loginUser(formData.email, formData.password);
      storeAuth(authResponse);
      navigate('/dashboard'); // Redirect to dashboard after successful login
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Google login handler
  const googleLoginHandler = useGoogleLogin({
    onSuccess: async (credentialResponse) => {
      try {
        setLoading(true);
        const authResponse = await googleLogin(credentialResponse.access_token);
        storeAuth(authResponse);
        navigate('/dashboard');
      } catch (err) {
        setError('Google login failed. Please try again.');
      } finally {
        setLoading(false);
      }
    },
    onError: () => {
      setError('Google login failed');
    },
  });

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>Welcome Back</h1>
        <p className="auth-subtitle">Sign in to your ShopVerse account</p>

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

        <div className="divider">Or</div>

        <button
          type="button"
          className="btn btn-google"
          onClick={() => googleLoginHandler()}
          disabled={loading}
        >
          <span className="google-icon">G</span>
          Sign in with Google
        </button>

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
