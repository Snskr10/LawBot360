import './MissionPage.css';

export default function MissionPage() {
  return (
    <div className="mission-page">
      <div className="mission-container">
        <h1>Our Mission</h1>
        <div className="mission-content">
          <p className="mission-intro">
            At LawBot 360, our mission is to make legal information accessible, understandable, and actionable 
            for everyone. We believe that understanding your legal rights should not be complicated or expensive.
          </p>

          <section className="mission-section">
            <h2>Our Vision</h2>
            <p>
              To democratize legal knowledge and empower individuals and businesses with AI-powered legal 
              assistance that is accurate, reliable, and easy to use.
            </p>
          </section>

          <section className="mission-section">
            <h2>What We Do</h2>
            <ul>
              <li>Provide AI-powered legal question answering for Indian Laws</li>
              <li>Generate legally-structured contracts using natural language</li>
              <li>Verify documents for compliance and risk assessment</li>
              <li>Explain legal concepts in plain, understandable language</li>
            </ul>
          </section>

          <section className="mission-section">
            <h2>Our Commitment</h2>
            <p>
              We are committed to providing accurate, helpful legal information while always reminding users 
              that our services are educational aids and not substitutes for professional legal advice.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}

