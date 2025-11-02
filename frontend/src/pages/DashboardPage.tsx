import { useCallback, useEffect, useState } from 'react';
import PageHeader from '../shared/PageHeader';
import LoadingSpinner from '../components/LoadingSpinner';
import { fetchDashboardMetrics } from '../api/client';

type MetricResponse = {
  counts: { contracts?: number; verifications?: number };
  risk_histogram: Array<{ range: string; count: number }>;
  top_missing_clauses: string[];
  compliance_scores: Array<{ month: string; avg_risk_score: number }>;
};

export default function DashboardPage() {
  const [metrics, setMetrics] = useState<MetricResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadMetrics = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await fetchDashboardMetrics();
      setMetrics(data);
    } catch (err: any) {
      const message = err?.response?.data?.error || err?.message || 'Failed to load metrics.';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadMetrics();
  }, [loadMetrics]);

  const counts = metrics?.counts || {};
  const riskHistogram = metrics?.risk_histogram ?? [];
  const topClauses = metrics?.top_missing_clauses ?? [];
  const complianceScores = metrics?.compliance_scores ?? [];

  return (
    <div className="page animate-fade-in">
      <div className="dashboard-welcome">
        <h2>Welcome back! 👋</h2>
        <p>Here's what's happening with your legal documents today.</p>
      </div>

      <PageHeader
        title="Dashboard"
        subtitle="Track contract activity, verification risk and compliance trends."
        actions={
          <button className="link-button" onClick={loadMetrics} disabled={loading}>
            🔄 Refresh
          </button>
        }
      />

      {error && <div className="notice notice-error">{error}</div>}
      {loading && <LoadingSpinner message="Loading metrics..." />}

      {!loading && metrics && (
        <>
          <section className="card-grid">
            <div className="stat-card stat-primary">
              <div className="stat-card-header">
                <h3 className="stat-card-title">Total Contracts</h3>
                <span className="stat-card-icon">📄</span>
              </div>
              <div className="stat-card-value">{counts.contracts ?? 0}</div>
              <p className="metric-caption">Contracts generated</p>
            </div>
            
            <div className="stat-card stat-success">
              <div className="stat-card-header">
                <h3 className="stat-card-title">Verifications</h3>
                <span className="stat-card-icon">✓</span>
              </div>
              <div className="stat-card-value">{counts.verifications ?? 0}</div>
              <p className="metric-caption">Documents analyzed</p>
            </div>
            
          </section>

          <section className="card-grid">
            <div className="card">
              <h3>Risk Distribution</h3>
              <ul className="histogram">
                {riskHistogram.map((bucket) => (
                  <li key={bucket.range} className="histogram-item">
                    <span className="histogram-label">{bucket.range}</span>
                    <div className="histogram-bar-container">
                      <div 
                        className="histogram-bar" 
                        style={{ 
                          width: `${riskHistogram.length > 0 && Math.max(...riskHistogram.map(b => b.count)) > 0 
                            ? (bucket.count / Math.max(...riskHistogram.map(b => b.count))) * 100 
                            : 0}%` 
                        }}
                      ></div>
                    </div>
                    <span className="histogram-value">{bucket.count}</span>
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="card">
              <h3>Compliance Scores</h3>
              <ul className="histogram">
                {complianceScores.map((score) => (
                  <li key={score.month} className="histogram-item">
                    <span className="histogram-label">{score.month}</span>
                    <div className="histogram-bar-container">
                      <div 
                        className="histogram-bar" 
                        style={{ width: `${score.avg_risk_score}%` }}
                      ></div>
                    </div>
                    <span className="histogram-value">{score.avg_risk_score.toFixed(1)}</span>
                  </li>
                ))}
              </ul>
            </div>
          </section>
        </>
      )}
    </div>
  );
}

