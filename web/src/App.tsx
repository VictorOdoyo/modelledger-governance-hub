import { AlertTriangle, BarChart3, DatabaseZap, GitBranch, ShieldCheck } from 'lucide-react';
import { useMemo, useState } from 'react';

import { ApprovalQueue } from './components/ApprovalQueue';
import { ArtifactPanel } from './components/ArtifactPanel';
import { DeploymentTimeline } from './components/DeploymentTimeline';
import { DriftDashboard } from './components/DriftDashboard';
import { EvaluationGateMatrix } from './components/EvaluationGateMatrix';
import { ExperimentRuns } from './components/ExperimentRuns';
import { MetricCard } from './components/MetricCard';
import { ModelRegistry } from './components/ModelRegistry';
import { RollbackPlanner } from './components/RollbackPlanner';
import { approvals, deployments, driftReports, experimentRuns, models, versions } from './data/seed';
import { countProductionDeployments, modelsNeedingAttention } from './lib/selectors';

export function App() {
  const [selectedModelId, setSelectedModelId] = useState(models[0].id);
  const selectedModel = models.find((model) => model.id === selectedModelId) ?? models[0];
  const selectedVersion = versions.find((version) => version.modelId === selectedModel.id) ?? versions[0];
  const attention = useMemo(
    () => modelsNeedingAttention(models, versions, approvals, driftReports),
    [],
  );

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand-mark">ML</div>
        <div>
          <strong>ModelLedger</strong>
          <span>Governance hub</span>
        </div>
        <nav>
          <a href="#registry">Registry</a>
          <a href="#gates">Evaluation</a>
          <a href="#approvals">Approvals</a>
          <a href="#deployments">Deployments</a>
          <a href="#drift">Drift</a>
        </nav>
      </aside>
      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">Model governance workspace</p>
            <h1>ModelLedger Governance Hub</h1>
          </div>
          <button type="button">
            <ShieldCheck size={18} />
            Request approval
          </button>
        </header>
        <section className="metrics">
          <MetricCard icon={DatabaseZap} label="Registered models" value={models.length.toString()} detail="Owned model records" />
          <MetricCard icon={GitBranch} label="Versions" value={versions.length.toString()} detail="Governed release packages" />
          <MetricCard icon={AlertTriangle} label="Needs attention" value={attention.length.toString()} detail="Drift, gates, or approvals" />
          <MetricCard icon={BarChart3} label="Production" value={countProductionDeployments(deployments).toString()} detail="Active deployments" />
        </section>
        <ModelRegistry
          models={models}
          versions={versions}
          selectedModelId={selectedModelId}
          onSelect={setSelectedModelId}
        />
        <section className="grid-two">
          <EvaluationGateMatrix version={selectedVersion} />
          <ApprovalQueue approvals={approvals} version={selectedVersion} />
          <DeploymentTimeline deployments={deployments} version={selectedVersion} />
          <DriftDashboard reports={driftReports} version={selectedVersion} />
          <ArtifactPanel version={selectedVersion} />
          <RollbackPlanner deployments={deployments} version={selectedVersion} />
        </section>
        <ExperimentRuns runs={experimentRuns} selectedModel={selectedModel} />
      </section>
    </main>
  );
}
