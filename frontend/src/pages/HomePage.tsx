import { useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './HomePage.css';

export default function HomePage() {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  if (isAuthenticated) {
    return null;
  }

  return (
    <div className="homepage">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-badge">
            <span>⚖️ AI-Powered Legal Assistant</span>
          </div>
          <h1 className="hero-title">
            Transform Your Legal Workflow with
            <span className="gradient-text"> LawBot 360</span>
          </h1>
          <p className="hero-description">
            Generate contracts, verify documents, and understand legal concepts instantly. 
            Powered by advanced AI to make legal processes faster, smarter, and more accessible.
          </p>
          <div className="hero-actions">
            <Link to="/chat" className="btn-hero-primary">
              Start Chatting
            </Link>
            <Link to="/register" className="btn-hero-secondary">
              Get Started Free
            </Link>
            <Link to="/login" className="btn-hero-secondary">
              Sign In
            </Link>
          </div>
          <div className="hero-stats">
            <div className="stat-item">
              <div className="stat-number">1000+</div>
              <div className="stat-label">Contracts Generated</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">500+</div>
              <div className="stat-label">Documents Verified</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">99%</div>
              <div className="stat-label">Accuracy Rate</div>
            </div>
          </div>
        </div>
        <div className="hero-visual">
          <div className="hero-card hero-card-1">
            <div className="card-icon">📄</div>
            <div className="card-text">Contract Generated</div>
          </div>
          <div className="hero-card hero-card-2">
            <div className="card-icon">✓</div>
            <div className="card-text">Verified & Compliant</div>
          </div>
          <div className="hero-card hero-card-3">
            <div className="card-icon">⚡</div>
            <div className="card-text">AI-Powered</div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="section-header">
          <h2 className="section-title">Powerful Features for Legal Professionals</h2>
          <p className="section-subtitle">
            Everything you need to streamline your legal workflow in one platform
          </p>
        </div>

        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">📝</div>
            <h3 className="feature-title">Smart Contract Generation</h3>
            <p className="feature-description">
              Generate legally-structured contracts from natural language prompts. 
              Choose from templates for NDAs, Employment agreements, Service contracts, and more.
            </p>
            <div className="feature-badge">AI-Powered</div>
          </div>

          <div className="feature-card">
            <div className="feature-icon">✓</div>
            <h3 className="feature-title">Document Verification</h3>
            <p className="feature-description">
              Upload your contract to check for missing clauses, risk factors, and compliance issues. 
              Get actionable suggestions for improvements.
            </p>
            <div className="feature-badge">Risk Analysis</div>
          </div>

          <div className="feature-card">
            <div className="feature-icon">📚</div>
            <h3 className="feature-title">Legal Explanation</h3>
            <p className="feature-description">
              Understand legal clauses and concepts in plain language. 
              Get explanations with references to relevant sections and acts.
            </p>
            <div className="feature-badge">Knowledge Base</div>
          </div>

          <div className="feature-card">
            <div className="feature-icon">📋</div>
            <h3 className="feature-title">Template Library</h3>
            <p className="feature-description">
              Access a comprehensive library of legal templates. 
              Customize and use pre-approved contract templates for faster drafting.
            </p>
            <div className="feature-badge">Pre-Approved</div>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🔒</div>
            <h3 className="feature-title">Secure & Compliant</h3>
            <p className="feature-description">
              Your documents are encrypted and stored securely. 
              Full compliance with data protection regulations and audit trails.
            </p>
            <div className="feature-badge">Enterprise Grade</div>
          </div>

          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <h3 className="feature-title">Instant Results</h3>
            <p className="feature-description">
              Get contract generation and verification results in seconds. 
              No more waiting hours or days for legal document processing.
            </p>
            <div className="feature-badge">Lightning Fast</div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="cta-content">
          <h2 className="cta-title">Ready to Transform Your Legal Workflow?</h2>
          <p className="cta-description">
            Join thousands of legal professionals who trust LawBot 360 for their contract management needs.
          </p>
          <Link to="/chat" className="btn-cta">
            Start Chatting Now
          </Link>
        </div>
      </section>
    </div>
  );
}

