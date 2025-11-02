import './AboutPage.css';

export default function AboutPage() {
  return (
    <div className="about-page">
      <div className="about-container">
        <h1>About Us</h1>
        <div className="about-content">
          <section className="about-section">
            <h2>LawBot 360</h2>
            <p>
              LawBot 360 is an AI-powered legal assistant designed to help individuals and businesses 
              understand Indian laws, generate contracts, verify documents, and get answers to legal questions.
            </p>
          </section>

          <section className="about-section">
            <h2>Our Partnership</h2>
            <p>
              LawBot 360 has been designed with help from <strong>Giri & Co.</strong>, a 40 year old law firm 
              based in New Delhi, India, specialising in all sorts of civil and criminal matters. This partnership 
              ensures that our AI responses are grounded in real legal expertise and practice.
            </p>
          </section>

          <section className="about-section">
            <h2>Technology</h2>
            <p>
              We leverage advanced AI and machine learning technologies to provide accurate legal information. 
              Our system uses vector databases and retrieval-augmented generation (RAG) to ensure responses are 
              based on authentic legal sources.
            </p>
          </section>

          <section className="about-section">
            <h2>Disclaimer</h2>
            <p>
              LawBot 360 provides educational information and is not a substitute for professional legal advice. 
              Always consult a qualified lawyer for specific legal matters and final document review.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}

