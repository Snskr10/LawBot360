import PageHeader from '../shared/PageHeader';

const placeholderTemplates = [
  { name: 'Mutual NDA', jurisdiction: 'IN', riskLevel: 'Medium' },
  { name: 'Employment Agreement', jurisdiction: 'IN', riskLevel: 'High' },
  { name: 'Service Agreement', jurisdiction: 'US', riskLevel: 'Medium' },
];

export default function TemplatesPage() {
  return (
    <div className="page">
      <PageHeader
        title="Clause Templates"
        subtitle="Manage reusable clause snippets with jurisdiction metadata and risk classification."
      />

      <section className="card">
        <table className="data-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Jurisdiction</th>
              <th>Risk Level</th>
            </tr>
          </thead>
          <tbody>
            {placeholderTemplates.map((template) => (
              <tr key={template.name}>
                <td>{template.name}</td>
                <td>{template.jurisdiction}</td>
                <td>{template.riskLevel}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}

