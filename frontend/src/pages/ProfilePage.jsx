import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { getProfile, updateProfile } from '../services/authService';
import '../styles/profile.css';

export const ProfilePage = () => {
  const { user, logout } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [profile, setProfile] = useState({
    email: '',
    username: '',
    full_name: '',
    address: '',
    profile_picture: '',
    created_at: '',
  });

  // Load profile on mount
  useEffect(() => {
    const loadProfile = async () => {
      try {
        setLoading(true);
        const data = await getProfile();
        setProfile({
          email: data.email,
          username: data.username,
          full_name: data.full_name || '',
          address: data.address || '',
          profile_picture: data.profile_picture || '',
          created_at: new Date(data.created_at).toLocaleDateString(),
        });
        setError('');
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to load profile');
      } finally {
        setLoading(false);
      }
    };

    loadProfile();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setProfile((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSaveProfile = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      setError('');
      setSuccess('');

      // Validate inputs
      if (profile.full_name && profile.full_name.trim().length === 0) {
        setError('Full name cannot be empty');
        setLoading(false);
        return;
      }

      const updateData = {
        full_name: profile.full_name || null,
        address: profile.address || null,
        profile_picture: profile.profile_picture || null,
      };

      const data = await updateProfile(updateData);

      setProfile({
        ...profile,
        full_name: data.full_name || '',
        address: data.address || '',
        profile_picture: data.profile_picture || '',
      });

      setSuccess('Profile updated successfully!');
      setIsEditing(false);

      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    setIsEditing(false);
    setError('');
  };

  if (loading && !isEditing) {
    return <div className="profile-container"><div className="loading">Loading profile...</div></div>;
  }

  return (
    <div className="profile-container">
      <div className="profile-header">
        <h1>User Profile</h1>
        <button className="logout-btn" onClick={logout}>
          Logout
        </button>
      </div>

      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      <div className="profile-card">
        {/* Profile Picture Section */}
        <div className="profile-picture-section">
          {profile.profile_picture ? (
            <img
              src={profile.profile_picture}
              alt="Profile"
              className="profile-picture"
            />
          ) : (
            <div className="profile-picture-placeholder">
              <span className="placeholder-text">
                {profile.username?.charAt(0).toUpperCase()}
              </span>
            </div>
          )}
        </div>

        {/* Profile Information */}
        {!isEditing ? (
          <div className="profile-info">
            <div className="info-group">
              <label>Email</label>
              <p>{profile.email}</p>
            </div>

            <div className="info-group">
              <label>Username</label>
              <p>{profile.username}</p>
            </div>

            <div className="info-group">
              <label>Full Name</label>
              <p>{profile.full_name || 'Not set'}</p>
            </div>

            <div className="info-group">
              <label>Address</label>
              <p>{profile.address || 'Not set'}</p>
            </div>

            <div className="info-group">
              <label>Member Since</label>
              <p>{profile.created_at}</p>
            </div>

            <button
              className="edit-btn"
              onClick={() => setIsEditing(true)}
            >
              Edit Profile
            </button>
          </div>
        ) : (
          <form className="profile-form" onSubmit={handleSaveProfile}>
            <div className="form-group">
              <label htmlFor="full_name">Full Name</label>
              <input
                type="text"
                id="full_name"
                name="full_name"
                value={profile.full_name}
                onChange={handleInputChange}
                placeholder="Enter your full name"
                maxLength="100"
              />
            </div>

            <div className="form-group">
              <label htmlFor="address">Address</label>
              <textarea
                id="address"
                name="address"
                value={profile.address}
                onChange={handleInputChange}
                placeholder="Enter your address"
                rows="3"
                maxLength="500"
              />
            </div>

            <div className="form-group">
              <label htmlFor="profile_picture">Profile Picture URL</label>
              <input
                type="url"
                id="profile_picture"
                name="profile_picture"
                value={profile.profile_picture}
                onChange={handleInputChange}
                placeholder="https://example.com/image.jpg"
                maxLength="1000"
              />
            </div>

            {profile.profile_picture && (
              <div className="preview-section">
                <p className="preview-label">Preview:</p>
                <img
                  src={profile.profile_picture}
                  alt="Preview"
                  className="preview-image"
                />
              </div>
            )}

            <div className="form-actions">
              <button
                type="submit"
                className="save-btn"
                disabled={loading}
              >
                {loading ? 'Saving...' : 'Save Changes'}
              </button>
              <button
                type="button"
                className="cancel-btn"
                onClick={handleCancel}
              >
                Cancel
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

export default ProfilePage;
