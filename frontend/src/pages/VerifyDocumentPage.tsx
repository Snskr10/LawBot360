import { useState } from 'react';
import PageHeader from '../shared/PageHeader';
import { verifyDocument } from '../api/client';

type VerificationFinding = {
  clause: string;
  issue: string;
  severity: string;
  suggestion?: string;
};

type VerificationResult = {
  report_id: number;
  risk_score: number;
  findings: VerificationFinding[];
  suggestions: string[];
  summary_pdf_url?: string;
};

export default function VerifyDocumentPage() {
  const [file, setFile] = useState<File | null>(null);
  const [jurisdiction, setJurisdiction] = useState('IN');
  const [language, setLanguage] = useState('en');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<VerificationResult | null>(null);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!file) {
      setError('Please select a contract file to verify.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('jurisdiction', jurisdiction);
    formData.append('language', language);

    try {
      const data = await verifyDocument(formData);
      setResult(data);
    } catch (err: any) {
      const message = err?.response?.data?.error || err?.message || 'Verification failed.';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0] ?? null;
    setFile(selectedFile);
  };

  const riskScore = result?.risk_score ?? null;

  return (
    <div className="page">
      <PageHeader
        title="Verify Document"
        subtitle="Upload a contract to check for missing clauses, risk indicators, and compliance gaps."
      />

      <div className="two-column">
        <form className="card" onSubmit={handleSubmit}>
          <h3>Upload Contract</h3>
          <label className="input-group">
            <span>Contract Document</span>
            <input type="file" accept=".pdf,.doc,.docx" required onChange={handleFileChange} />
          </label>

          <div className="grid grid-2">
            <label className="input-group">
              <span>Jurisdiction</span>
              <select value={jurisdiction} onChange={(e) => setJurisdiction(e.target.value)}>
                <option value="IN">India</option>
                <option value="US">United States</option>
                <option value="UK">United Kingdom</option>
              </select>
            </label>

            <label className="input-group">
              <span>Language</span>
              <select value={language} onChange={(e) => setLanguage(e.target.value)}>
                <option value="en">English</option>
                <option value="hi">हिंदी</option>
              </select>
            </label>
          </div>

          <button type="submit" className="primary-button" disabled={loading}>
            {loading ? 'Verifying…' : 'Run Verification'}
          </button>

          {error && <div className="notice notice-error">{error}</div>}
        </form>

        <aside className="card">
          <h3>Verification Results</h3>
          {loading && <p>Analyzing document…</p>}
          {!loading && !result && !error && <p>Results will appear here once a document is verified.</p>}
          {!loading && result && (
            <div className="verification-results">
              <div className="risk-bar">
                <span style={{ width: `${Math.min(result.risk_score, 100)}%` }} />
                <strong>{result.risk_score.toFixed(1)}</strong>
              </div>
              <p className="risk-score-text">Risk Score (0 = low risk, 100 = high risk)</p>

              {result.findings.length > 0 && (
                <div>
                  <h4>Findings</h4>
                  <ul>
                    {result.findings.map((finding, index) => (
                      <li key={index} className={`finding severity-${finding.severity}`}>
                        <strong>{finding.clause}:</strong> {finding.issue}
                        {finding.suggestion && <div className="hint">Suggested fix: {finding.suggestion}</div>}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {result.suggestions.length > 0 && (
                <div>
                  <h4>Suggestions</h4>
                  <ul>
                    {result.suggestions.map((suggestion, index) => (
                      <li key={index}>{suggestion}</li>
                    ))}
                  </ul>
                </div>
              )}

              {result.summary_pdf_url && (
                <a
                  className="link-button"
                  href={result.summary_pdf_url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Download Summary PDF
                </a>
              )}
            </div>
          )}
        </aside>
      </div>
    </div>
  );
}

