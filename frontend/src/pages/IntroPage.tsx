import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './IntroPage.css';

export default function IntroPage() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="intro-page">
      <div className="intro-content">
        <div className="intro-container">
          <div className="intro-logo">
            <div className="intro-logo-icon">🧠⚙️</div>
            <h1 className="intro-title">
              <span className="intro-title-green">Law</span>Bot 360
            </h1>
          </div>

          <div className="intro-welcome">
            <h2 className="intro-subtitle">Welcome to LawBot 360</h2>
            <p className="intro-description">
              Your AI-powered legal assistant for Indian Laws. Get instant answers to your legal queries,
              understand your rights, and get guidance on legal matters - all powered by advanced AI technology.
            </p>
            <p className="intro-disclaimer">
              <strong>Important:</strong> LawBot 360 provides educational information and is not a substitute for 
              professional legal advice. Please consult a qualified lawyer for specific legal matters.
            </p>
          </div>

          <div className="intro-features">
            <h3 className="intro-features-title">What You Can Do:</h3>
            <div className="intro-features-grid">
              <div className="intro-feature-item">
                <span className="feature-icon">💬</span>
                <div>
                  <h4>Chat with AI</h4>
                  <p>Ask legal questions and get instant answers</p>
                </div>
              </div>
              <div className="intro-feature-item">
                <span className="feature-icon">📝</span>
                <div>
                  <h4>Create Contracts</h4>
                  <p>Generate legally-structured contracts</p>
                </div>
              </div>
              <div className="intro-feature-item">
                <span className="feature-icon">✓</span>
                <div>
                  <h4>Verify Documents</h4>
                  <p>Check contracts for compliance issues</p>
                </div>
              </div>
              <div className="intro-feature-item">
                <span className="feature-icon">📚</span>
                <div>
                  <h4>Explain Laws</h4>
                  <p>Understand legal concepts easily</p>
                </div>
              </div>
            </div>
          </div>

          <div className="intro-actions">
            {!isAuthenticated ? (
              <>
                <Link to="/chat" className="intro-btn intro-btn-primary">
                  Start Chatting
                </Link>
                <Link to="/register" className="intro-btn intro-btn-secondary">
                  Create Account
                </Link>
                <Link to="/login" className="intro-btn intro-btn-secondary">
                  Sign In
                </Link>
              </>
            ) : (
              <>
                <Link to="/chat" className="intro-btn intro-btn-primary">
                  Start Chatting
                </Link>
                <Link to="/dashboard" className="intro-btn intro-btn-secondary">
                  Go to Dashboard
                </Link>
              </>
            )}
          </div>

          <div className="intro-footer">
            <p>
              LawBot 360 has been designed with help from <strong>Giri & Co.</strong>, a 40 year old law firm 
              based in New Delhi, India, specialising in all sorts of civil and criminal matters.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

