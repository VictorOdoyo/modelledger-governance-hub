import type { DriftReport, ModelVersion } from '../types';

interface Props {
  reports: DriftReport[];
  version: ModelVersion;
}

export function DriftDashboard({ reports, version }: Props) {
  const matching = reports.filter((report) => report.versionId === version.id);
  return (
    <section className="panel" id="drift">
      <h2>Drift dashboard</h2>
      <p>Population stability, accuracy movement, and volume shift.</p>
      {matching.length === 0 ? (
        <div className="empty-state">No drift reports for this version.</div>
      ) : (
        matching.map((report) => (
          <article className="drift-card" key={report.id}>
            <span className={`pill drift-${report.severity}`}>{report.severity}</span>
            <strong>{report.baselineWindow} to {report.observedWindow}</strong>
            <div className="metric-grid">
              {Object.entries(report.metrics).map(([name, value]) => (
                <span key={name}>{name}: {value}</span>
              ))}
            </div>
          </article>
        ))
      )}
    </section>
  );
}
