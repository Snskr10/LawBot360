import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useToast } from '../contexts/ToastContext';
import { getCurrentUser, User } from '../api/client';
import PageHeader from '../shared/PageHeader';
import LoadingSpinner from '../components/LoadingSpinner';
import './SettingsPage.css';

export default function SettingsPage() {
  const { user, logout } = useAuth();
  const { success, error: showError } = useToast();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [userData, setUserData] = useState<User | null>(user);
  const [editing, setEditing] = useState(false);
  const [profileImage, setProfileImage] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    name: user?.name || '',
    email: user?.email || '',
  });

  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        showError('Image size should be less than 5MB');
        return;
      }
      const reader = new FileReader();
      reader.onloadend = () => {
        setProfileImage(reader.result as string);
        success('Profile picture updated!');
      };
      reader.readAsDataURL(file);
    }
  };

  const handleEdit = () => {
    setEditing(true);
  };

  const handleSave = async () => {
    setLoading(true);
    try {
      // TODO: Implement update user API endpoint
      // await updateUser(formData);
      success('Profile updated successfully!');
      setEditing(false);
      // Refresh user data
      const updated = await getCurrentUser();
      setUserData(updated);
    } catch (err: any) {
      showError(err.response?.data?.error || 'Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    setFormData({
      name: user?.name || '',
      email: user?.email || '',
    });
    setEditing(false);
  };

  const handleLogout = () => {
    logout();
    success('Logged out successfully');
    navigate('/login');
  };

  if (loading && !userData) {
    return <LoadingSpinner message="Loading profile..." fullScreen />;
  }

  return (
    <div className="page">
      <PageHeader title="Settings" subtitle="Manage your account settings and preferences" />

      <div className="settings-content">
        <section className="card">
          <h3>Profile Information</h3>
          
          {/* Circular Profile Picture Uploader */}
          <div className="profile-picture-section">
            <div className="profile-picture-container">
              <label htmlFor="profile-upload" className="profile-upload-label">
                <div className="profile-picture-wrapper">
                  {profileImage ? (
                    <img src={profileImage} alt="Profile" className="profile-picture" />
                  ) : (
                    <div className="profile-picture-placeholder">
                      <span className="profile-initials">
                        {userData?.name?.charAt(0).toUpperCase() || 'U'}
                      </span>
                    </div>
                  )}
                  <div className="profile-overlay">
                    <span className="camera-icon">📷</span>
                    <span className="upload-text">Change Photo</span>
                  </div>
                </div>
              </label>
              <input
                id="profile-upload"
                type="file"
                accept="image/*"
                onChange={handleImageChange}
                className="profile-upload-input"
              />
            </div>
            <p className="profile-picture-hint">Click the circle to upload a new profile picture</p>
          </div>

          {editing ? (
            <div className="profile-form">
              <div className="form-group">
                <label>Full Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  disabled={loading}
                />
              </div>
              <div className="form-group">
                <label>Email</label>
                <input
                  type="email"
                  value={formData.email}
                  disabled
                  className="disabled"
                />
                <small>Email cannot be changed</small>
              </div>
              <div className="form-actions">
                <button
                  className="btn-primary"
                  onClick={handleSave}
                  disabled={loading}
                >
                  {loading ? 'Saving...' : 'Save Changes'}
                </button>
                <button
                  className="btn-secondary"
                  onClick={handleCancel}
                  disabled={loading}
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <div className="profile-info">
              <div className="info-row">
                <label>Name:</label>
                <span>{userData?.name || 'N/A'}</span>
              </div>
              <div className="info-row">
                <label>Email:</label>
                <span>{userData?.email || 'N/A'}</span>
              </div>
              <div className="info-row">
                <label>Role:</label>
                <span className="role-badge">{userData?.role || 'user'}</span>
              </div>
              <button className="btn-primary" onClick={handleEdit}>
                Edit Profile
              </button>
            </div>
          )}
        </section>

        <section className="card">
          <h3>Change Password</h3>
          <div className="password-form">
            <div className="form-group">
              <label>Current Password</label>
              <input type="password" placeholder="Enter current password" />
            </div>
            <div className="form-group">
              <label>New Password</label>
              <input type="password" placeholder="Enter new password" minLength={6} />
            </div>
            <div className="form-group">
              <label>Confirm New Password</label>
              <input type="password" placeholder="Confirm new password" minLength={6} />
            </div>
            <button className="btn-primary" disabled>
              Change Password
            </button>
            <small className="text-muted">Password change feature coming soon</small>
          </div>
        </section>

        <section className="card">
          <h3>Preferences</h3>
          <div className="preferences">
            <div className="preference-item">
              <label>
                <input type="checkbox" defaultChecked />
                Email notifications for contract updates
              </label>
            </div>
            <div className="preference-item">
              <label>
                <input type="checkbox" />
                Weekly summary reports
              </label>
            </div>
            <div className="preference-item">
              <label>
                <input type="checkbox" defaultChecked />
                Risk alerts for high-risk contracts
              </label>
            </div>
          </div>
        </section>

        <section className="card danger-zone">
          <h3>Danger Zone</h3>
          <p className="warning-text">Irreversible actions</p>
          <button className="btn-danger" onClick={handleLogout}>
            Logout
          </button>
          <button className="btn-danger" disabled>
            Delete Account
          </button>
          <small className="text-muted">Account deletion coming soon</small>
        </section>
      </div>
    </div>
  );
}
