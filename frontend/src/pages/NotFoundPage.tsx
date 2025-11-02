import { Link } from 'react-router-dom';
import PageHeader from '../shared/PageHeader';

export default function NotFoundPage() {
  return (
    <div className="page">
      <PageHeader title="Page Not Found" subtitle="The page you are looking for does not exist." />
      <section className="card">
        <p>
          Return to the <Link to="/dashboard">dashboard</Link> or choose another section from the navigation above.
        </p>
      </section>
    </div>
  );
}

