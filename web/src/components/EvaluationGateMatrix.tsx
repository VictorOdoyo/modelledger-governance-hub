import type { ModelVersion } from '../types';

import { policyCompletion } from '../lib/selectors';

interface Props {
  version: ModelVersion;
}

export function EvaluationGateMatrix({ version }: Props) {
  const rules = [
    ['AUC', version.metrics.auc, '>= 0.82'],
    ['Latency', version.metrics.latency_ms, '<= 650 ms'],
    ['Data quality', version.metrics.data_quality, '>= 0.94'],
    ['Bias gap', version.metrics.bias_gap, '<= 0.12'],
  ];
  return (
    <section className="panel" id="gates">
      <h2>Evaluation gates</h2>
      <p>{policyCompletion(version)}% of required governance metrics are present.</p>
      <div className="gate-list">
        {rules.map(([label, value, threshold]) => (
          <div className="gate-row" key={label}>
            <span>{label}</span>
            <strong>{typeof value === 'number' ? value : 'missing'}</strong>
            <small>{threshold}</small>
          </div>
        ))}
      </div>
    </section>
  );
}
