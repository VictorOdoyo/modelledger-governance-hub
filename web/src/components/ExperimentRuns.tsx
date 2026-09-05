import type { ExperimentRun, RegisteredModel } from '../types';

import { percent } from '../lib/format';

interface Props {
  runs: ExperimentRun[];
  selectedModel: RegisteredModel;
}

export function ExperimentRuns({ runs, selectedModel }: Props) {
  const matching = runs.filter((run) => run.modelId === selectedModel.id);
  return (
    <section className="panel">
      <h2>Experiment runs</h2>
      <p>Recent MLflow-linked run state for the selected registered model.</p>
      <div className="run-list">
        {matching.map((run) => (
          <article className="run-row" key={run.id}>
            <span className={`pill run-${run.status}`}>{run.status}</span>
            <strong>{run.id}</strong>
            <span>{run.owner}</span>
            <span>{percent(run.metricDelta)}</span>
          </article>
        ))}
      </div>
    </section>
  );
}
