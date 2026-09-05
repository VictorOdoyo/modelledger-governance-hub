import type { Deployment, ModelVersion } from '../types';

interface Props {
  deployments: Deployment[];
  version: ModelVersion;
}

export function DeploymentTimeline({ deployments, version }: Props) {
  const matching = deployments.filter((deployment) => deployment.versionId === version.id);
  return (
    <section className="panel" id="deployments">
      <h2>Deployment timeline</h2>
      <p>Promotion records, environments, change tickets, and rollback state.</p>
      {matching.map((deployment) => (
        <article className="timeline-item" key={deployment.id}>
          <span className={`pill stage-${deployment.stage}`}>{deployment.stage}</span>
          <strong>{deployment.environment}</strong>
          <small>{deployment.changeTicket} by {deployment.createdBy}</small>
        </article>
      ))}
    </section>
  );
}
