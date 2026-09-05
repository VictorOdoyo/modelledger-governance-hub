import type { Approval, Deployment, DriftReport, GateState, ModelVersion, RegisteredModel } from '../types';

export function latestVersions(models: RegisteredModel[], versions: ModelVersion[]) {
  return models.map((model) => ({
    model,
    version: versions.find((version) => version.modelId === model.id),
  }));
}

export function modelsNeedingAttention(
  models: RegisteredModel[],
  versions: ModelVersion[],
  approvals: Approval[],
  driftReports: DriftReport[],
) {
  return latestVersions(models, versions).filter(({ version }) => {
    if (!version) return true;
    const pending = approvals.some((approval) => approval.versionId === version.id && approval.state === 'requested');
    const drift = driftReports.some(
      (report) => report.versionId === version.id && ['breach', 'critical'].includes(report.severity),
    );
    return version.gateState !== 'passed' || pending || drift;
  });
}

export function gateLabel(state: GateState) {
  return {
    not_run: 'Not run',
    passed: 'Passed',
    warning: 'Warning',
    failed: 'Failed',
  }[state];
}

export function countProductionDeployments(deployments: Deployment[]) {
  return deployments.filter((deployment) => deployment.stage === 'production' && !deployment.rolledBack).length;
}

export function policyCompletion(version: ModelVersion) {
  const expected = ['auc', 'latency_ms', 'data_quality', 'bias_gap'];
  const present = expected.filter((metric) => typeof version.metrics[metric] === 'number').length;
  return Math.round((present / expected.length) * 100);
}
