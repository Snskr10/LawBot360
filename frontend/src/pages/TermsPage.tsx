import './TermsPage.css';

export default function TermsPage() {
  return (
    <div className="terms-page">
      <div className="terms-container">
        <h1>Terms and Conditions</h1>
        
        <section className="terms-section">
          <h2>1. Privacy Policy</h2>
          <p>
            LawBot 360 is committed to protecting your privacy. We collect and use your information only 
            to provide and improve our services. We do not sell your personal information to third parties.
          </p>
          <p>
            <strong>Information We Collect:</strong> We collect information you provide when you register, 
            use our services, or contact us. This includes your name, email address, and usage data.
          </p>
          <p>
            <strong>How We Use Your Information:</strong> We use your information to provide legal assistance, 
            improve our services, send updates, and ensure security.
          </p>
          <p>
            <strong>Data Security:</strong> We implement appropriate security measures to protect your 
            personal information against unauthorized access, alteration, disclosure, or destruction.
          </p>
        </section>

        <section className="terms-section">
          <h2>2. Terms of Service</h2>
          <p>
            By using LawBot 360, you agree to these Terms and Conditions. If you do not agree, 
            please do not use our services.
          </p>
          <p>
            <strong>Service Description:</strong> LawBot 360 provides AI-powered legal information and 
            document generation tools. Our services are educational aids and do not constitute legal advice.
          </p>
          <p>
            <strong>User Responsibilities:</strong> You are responsible for maintaining the confidentiality 
            of your account and for all activities that occur under your account.
          </p>
          <p>
            <strong>Prohibited Uses:</strong> You may not use our services for any illegal purpose or to 
            violate any laws. You may not attempt to gain unauthorized access to our systems.
          </p>
        </section>

        <section className="terms-section">
          <h2>3. Cancellation and Refund Policy</h2>
          <p>
            <strong>Free Services:</strong> LawBot 360 offers free access to basic features. There are 
            no charges for free services, and no refunds are applicable.
          </p>
          <p>
            <strong>Paid Services:</strong> If you purchase any paid services, you may cancel your 
            subscription at any time. Refunds will be processed according to the following:
          </p>
          <ul>
            <li>Refund requests within 7 days of purchase will be fully refunded</li>
            <li>Refund requests after 7 days will be considered on a case-by-case basis</li>
            <li>Refunds may take 5-10 business days to process</li>
          </ul>
          <p>
            <strong>Cancellation:</strong> To cancel your subscription, please contact us through 
            the Contact Us page or email us directly.
          </p>
        </section>

        <section className="terms-section">
          <h2>4. Disclaimer</h2>
          <p>
            LawBot 360 provides educational information and document generation tools. Our AI-powered 
            responses are based on available legal data but should not be considered as legal advice. 
            Always consult with a qualified lawyer for specific legal matters.
          </p>
          <p>
            We are not responsible for any decisions made based on information provided by LawBot 360. 
            Users are solely responsible for verifying the accuracy and applicability of any information 
            provided through our services.
          </p>
        </section>

        <section className="terms-section">
          <h2>5. Contact Information</h2>
          <p>
            If you have any questions about these Terms and Conditions, please contact us:
          </p>
          <p>
            <strong>Email:</strong> support@lawbot360.com<br />
            <strong>Phone:</strong> +91-XXXXXXXXXX<br />
            <strong>Address:</strong> New Delhi, India
          </p>
        </section>

        <section className="terms-section">
          <p className="terms-updated">
            <strong>Last Updated:</strong> {new Date().toLocaleDateString()}
          </p>
        </section>
      </div>
    </div>
  );
}

