import type { ModelVersion, RegisteredModel } from '../types';

interface Props {
  models: RegisteredModel[];
  versions: ModelVersion[];
  selectedModelId: string;
  onSelect(modelId: string): void;
}

export function ModelRegistry({ models, versions, selectedModelId, onSelect }: Props) {
  return (
    <section className="panel" id="registry">
      <div className="panel-heading">
        <div>
          <h2>Registry</h2>
          <p>Model ownership, risk tier, latest version, and gate state.</p>
        </div>
      </div>
      <div className="registry-table" role="table">
        <div className="registry-row registry-head" role="row">
          <span>Model</span>
          <span>Owner</span>
          <span>Risk</span>
          <span>Latest</span>
          <span>Gate</span>
        </div>
        {models.map((model) => {
          const version = versions.find((candidate) => candidate.modelId === model.id);
          return (
            <button
              className={`registry-row ${selectedModelId === model.id ? 'selected' : ''}`}
              key={model.id}
              onClick={() => onSelect(model.id)}
              type="button"
            >
              <span>
                <strong>{model.name}</strong>
                <small>{model.businessDomain}</small>
              </span>
              <span>{model.owner}</span>
              <span className={`pill risk-${model.riskTier}`}>{model.riskTier}</span>
              <span>{version?.semanticVersion ?? 'none'}</span>
              <span className={`pill gate-${version?.gateState ?? 'not_run'}`}>{version?.gateState ?? 'not run'}</span>
            </button>
          );
        })}
      </div>
    </section>
  );
}
