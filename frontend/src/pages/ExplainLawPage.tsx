import { useState } from 'react';
import PageHeader from '../shared/PageHeader';
import { explainClause } from '../api/client';

type ExplanationResult = {
  explanation: string;
  refs?: string[];
};

export default function ExplainLawPage() {
  const [text, setText] = useState('');
  const [jurisdiction, setJurisdiction] = useState('IN');
  const [language, setLanguage] = useState('en');
  const [detail, setDetail] = useState('summary');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ExplanationResult | null>(null);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await explainClause({
        text,
        jurisdiction,
        language,
      });

      setResult({ explanation: data.explanation, refs: data.refs });
    } catch (err: any) {
      const message = err?.response?.data?.error || err?.message || 'Failed to fetch explanation.';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <PageHeader
        title="Explain Law"
        subtitle="Request clause-level explanations grounded in authenticated legal sources."
      />

      <form className="card stack" onSubmit={handleSubmit}>
        <label className="input-group">
          <span>Clause or Text</span>
          <textarea
            rows={5}
            placeholder="Paste a clause or question, e.g. 'Explain Section 10 of the Contract Act'."
            required
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
        </label>

        <div className="grid grid-3">
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
          <label className="input-group">
            <span>Output Detail</span>
            <select value={detail} onChange={(e) => setDetail(e.target.value)}>
              <option value="summary">Summary</option>
              <option value="detailed">Detailed</option>
            </select>
          </label>
        </div>

        <button type="submit" className="primary-button align-start" disabled={loading}>
          {loading ? 'Generating…' : 'Explain Clause'}
        </button>

        {error && <div className="notice notice-error">{error}</div>}
      </form>

      {loading && <section className="card">Generating explanation…</section>}

      {!loading && result && (
        <section className="card stack">
          <div>
            <h3>Explanation</h3>
            <p>{result.explanation}</p>
            {detail === 'detailed' && (
              <div className="hint">
                Detailed narrative requested — additional depth will surface as the backend enriches responses.
              </div>
            )}
          </div>
          {result.refs && result.refs.length > 0 && (
            <div>
              <h4>References</h4>
              <ul>
                {result.refs.map((ref) => (
                  <li key={ref}>{ref}</li>
                ))}
              </ul>
            </div>
          )}
        </section>
      )}
    </div>
  );
}

