import type { Approval, ModelVersion } from '../types';

interface Props {
  approvals: Approval[];
  version: ModelVersion;
}

export function ApprovalQueue({ approvals, version }: Props) {
  const matching = approvals.filter((approval) => approval.versionId === version.id);
  return (
    <section className="panel" id="approvals">
      <h2>Approval queue</h2>
      <p>Independent review packages for release governance.</p>
      {matching.length === 0 ? (
        <div className="empty-state">No approvals requested for this version.</div>
      ) : (
        matching.map((approval) => (
          <article className="queue-item" key={approval.id}>
            <span className={`pill approval-${approval.state}`}>{approval.state}</span>
            <strong>{approval.requestedBy}</strong>
            <p>{approval.reason}</p>
            {approval.decidedBy ? <small>Decided by {approval.decidedBy}</small> : null}
          </article>
        ))
      )}
    </section>
  );
}
