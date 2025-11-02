import { useState } from 'react';
import PageHeader from '../shared/PageHeader';
import { useToast } from '../contexts/ToastContext';
import LoadingSpinner, { LoadingButton } from '../components/LoadingSpinner';
import { generateContract, GenerateContractPayload } from '../api/client';

const contractTypes = [
  'NDA',
  'Employment',
  'Service',
  'Consultant',
  'Lease',
  'Partnership',
  'Vendor',
];

type ContractResult = {
  contract_id: number;
  html?: string;
  pdf_url?: string;
  docx_url?: string;
  summary?: {
    contract_type?: string;
    parties?: string[];
    key_terms?: Record<string, unknown>;
  };
  markdown?: string;
};

const defaultForm = {
  contractType: '',
  parties: '',
  summary: '',
  jurisdiction: 'IN',
  language: 'en',
};

export default function CreateContractPage() {
  const [form, setForm] = useState(defaultForm);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ContractResult | null>(null);
  const { success, error: showError } = useToast();

  const handleChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    const parties = form.parties
      .split(',')
      .map((party) => party.trim())
      .filter(Boolean);

    const payload: GenerateContractPayload = {
      contract_type: form.contractType,
      parties,
      terms: {
        summary: form.summary,
      },
      jurisdiction: form.jurisdiction,
      language: form.language,
    };

    try {
      const data = await generateContract(payload);
      setResult(data);
      success('Contract generated successfully!');
    } catch (err: any) {
      const message = err?.response?.data?.error || err?.message || 'Failed to generate contract.';
      setError(message);
      showError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page animate-fade-in">
      <PageHeader
        title="Create Contract"
        subtitle="Generate legally-structured contracts from natural language prompts or structured form inputs."
      />

      <div className="two-column">
        <form className="card" onSubmit={handleSubmit}>
          <h3>⚖️ Contract Details</h3>
          <label className="input-group">
            <span>Contract Type</span>
            <select
              name="contractType"
              required
              value={form.contractType}
              onChange={handleChange}
            >
              <option value="">Select type...</option>
              {contractTypes.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </label>

          <label className="input-group">
            <span>Parties (comma separated)</span>
            <input
              name="parties"
              type="text"
              placeholder="Party A, Party B"
              required
              value={form.parties}
              onChange={handleChange}
            />
          </label>

          <label className="input-group">
            <span>Natural Language Summary</span>
            <textarea
              name="summary"
              rows={4}
              placeholder="e.g. Employment contract for SWE at 8 LPA with NDA & IP clauses."
              value={form.summary}
              onChange={handleChange}
            />
          </label>

          <div className="grid grid-2">
            <label className="input-group">
              <span>Jurisdiction</span>
              <select name="jurisdiction" value={form.jurisdiction} onChange={handleChange}>
                <option value="IN">India</option>
                <option value="US">United States</option>
                <option value="UK">United Kingdom</option>
              </select>
            </label>

            <label className="input-group">
              <span>Language</span>
              <select name="language" value={form.language} onChange={handleChange}>
                <option value="en">English</option>
                <option value="hi">हिंदी</option>
              </select>
            </label>
          </div>

          <LoadingButton loading={loading} className="primary-button">
            Generate Contract
          </LoadingButton>

          {error && <div className="notice notice-error">{error}</div>}
        </form>

        <aside className="card preview">
          <h3>Preview</h3>
          <div className="preview-body">
            {loading && <p>Generating contract…</p>}
            {!loading && !result && <p>Select options and generate to preview contract.</p>}
            {!loading && result?.html && (
              <div
                className="contract-preview"
                dangerouslySetInnerHTML={{ __html: result.html }}
              />
            )}
            {!loading && !result?.html && result?.markdown && <pre>{result.markdown}</pre>}
          </div>

          {result && (
            <div className="preview-actions">
              {result.pdf_url && (
                <a className="link-button" href={result.pdf_url} target="_blank" rel="noopener noreferrer">
                  Download PDF
                </a>
              )}
              {result.docx_url && (
                <a className="link-button" href={result.docx_url} target="_blank" rel="noopener noreferrer">
                  Download DOCX
                </a>
              )}
            </div>
          )}

          {result?.summary && (
            <div className="summary-block">
              <h4>Summary</h4>
              <ul>
                {result.summary.parties && (
                  <li>
                    <strong>Parties:</strong> {result.summary.parties.join(', ')}
                  </li>
                )}
                {result.summary.key_terms &&
                  Object.entries(result.summary.key_terms).map(([key, value]) => (
                    <li key={key}>
                      <strong>{key}:</strong> {String(value)}
                    </li>
                  ))}
              </ul>
            </div>
          )}
        </aside>
      </div>
    </div>
  );
}

