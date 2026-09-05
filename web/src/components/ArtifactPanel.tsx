import { FileArchive } from 'lucide-react';

import type { ModelVersion } from '../types';

interface Props {
  version: ModelVersion;
}

export function ArtifactPanel({ version }: Props) {
  return (
    <section className="panel">
      <h2>Artifacts</h2>
      <p>Model package, training dataset, and feature signature.</p>
      <article className="artifact-card">
        <FileArchive size={18} />
        <div>
          <strong>{version.artifactUri}</strong>
          <small>{version.trainingDataset}</small>
        </div>
      </article>
      <div className="tag-list">
        {version.featureSignature.map((feature) => (
          <span key={feature}>{feature}</span>
        ))}
      </div>
    </section>
  );
}
