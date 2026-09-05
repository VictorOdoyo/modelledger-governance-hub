import type { Deployment, ModelVersion } from '../types';

interface Props {
  deployments: Deployment[];
  version: ModelVersion;
}

export function RollbackPlanner({ deployments, version }: Props) {
  const active = deployments.find((deployment) => deployment.versionId === version.id && !deployment.rolledBack);
  return (
    <section className="panel">
      <h2>Rollback planner</h2>
      <p>Controlled rollback target for active deployment records.</p>
      {active ? (
        <article className="rollback-card">
          <strong>{active.environment}</strong>
          <span>{active.changeTicket}</span>
          <small>Fallback: previous approved version in the same environment.</small>
        </article>
      ) : (
        <div className="empty-state">No active deployment selected.</div>
      )}
    </section>
  );
}
