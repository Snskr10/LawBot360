import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Sidebar.css';

const sidebarItems = [
  { to: '/login', label: 'Log In / Sign Up', icon: '→' },
  { to: '/chat', label: 'Chat', icon: '💬' },
  { to: '/dashboard', label: 'Dashboard', icon: '📊' },
  { to: '/create', label: 'Create Contract', icon: '📝' },
  { to: '/verify', label: 'Verify Document', icon: '✓' },
  { to: '/explain', label: 'Explain Law', icon: '📚' },
  { to: '/settings', label: 'Settings', icon: '⚙️' },
  { to: '/mission', label: 'Our Mission', icon: '✈️' },
  { to: '/about', label: 'About Us', icon: 'ℹ️' },
  { to: '/contact', label: 'Contact Us', icon: '👤' },
  { to: '/terms', label: 'Terms and Conditions', icon: '📄' },
];

export default function Sidebar() {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <aside className="sidebar">
      <Link to="/" className="sidebar-logo">
        <div className="logo-icon">🧠⚙️</div>
        <span className="logo-text"><span className="logo-text-green">Law</span>Bot 360</span>
      </Link>
      
      <nav className="sidebar-nav">
        {sidebarItems.map((item) => {
          // Don't show login link if already authenticated
          if (item.to === '/login' && isAuthenticated) {
            return null;
          }
          
          // Don't show dashboard/settings if not authenticated
          if ((item.to === '/dashboard' || item.to === '/create' || item.to === '/verify' || 
               item.to === '/explain' || item.to === '/settings') && !isAuthenticated) {
            return null;
          }
          
          return (
            <Link
              key={item.to}
              to={item.to}
              className="sidebar-nav-item"
            >
              <span className="sidebar-nav-icon">{item.icon}</span>
              <span className="sidebar-nav-label">{item.label}</span>
            </Link>
          );
        })}
        
        {isAuthenticated && (
          <button
            onClick={handleLogout}
            className="sidebar-nav-item sidebar-logout-btn"
          >
            <span className="sidebar-nav-icon">🚪</span>
            <span className="sidebar-nav-label">Logout</span>
          </button>
        )}
      </nav>
    </aside>
  );
}

