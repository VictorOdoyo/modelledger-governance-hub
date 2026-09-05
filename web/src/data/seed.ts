import type { Approval, Deployment, DriftReport, ExperimentRun, ModelVersion, RegisteredModel } from '../types';

export const models: RegisteredModel[] = [
  {
    id: 'mdl-claims',
    name: 'Claims Triage',
    owner: 'risk-platform',
    businessDomain: 'insurance',
    riskTier: 'high',
    tags: ['claims', 'routing', 'regulated'],
  },
  {
    id: 'mdl-revenue',
    name: 'Revenue Forecast',
    owner: 'finance-ml',
    businessDomain: 'finance',
    riskTier: 'medium',
    tags: ['forecasting', 'quarterly'],
  },
  {
    id: 'mdl-support',
    name: 'Support Deflection',
    owner: 'customer-ai',
    businessDomain: 'support',
    riskTier: 'low',
    tags: ['nlp', 'routing'],
  },
];

export const versions: ModelVersion[] = [
  {
    id: 'ver-claims-140',
    modelId: 'mdl-claims',
    semanticVersion: '1.4.0',
    sourceRunId: 'run-claims-q3-882',
    artifactUri: 's3://model-artifacts/claims/1.4.0/model.pkl',
    trainingDataset: 'claims-2026-q3',
    stage: 'production',
    gateState: 'passed',
    metrics: { auc: 0.91, latency_ms: 236, data_quality: 0.99, bias_gap: 0.04 },
    featureSignature: ['age_band', 'claim_type', 'region', 'prior_claim_count'],
  },
  {
    id: 'ver-revenue-210',
    modelId: 'mdl-revenue',
    semanticVersion: '2.1.0',
    sourceRunId: 'run-revenue-q3-221',
    artifactUri: 's3://model-artifacts/revenue/2.1.0/model.pkl',
    trainingDataset: 'finance-2026-q3',
    stage: 'staging',
    gateState: 'warning',
    metrics: { auc: 0.83, latency_ms: 642, data_quality: 0.96, bias_gap: 0.11 },
    featureSignature: ['region', 'segment', 'pipeline_age', 'seasonality'],
  },
  {
    id: 'ver-support-080',
    modelId: 'mdl-support',
    semanticVersion: '0.8.0',
    sourceRunId: 'run-support-beta-019',
    artifactUri: 's3://model-artifacts/support/0.8.0/model.pkl',
    trainingDataset: 'tickets-2026-aug',
    stage: 'candidate',
    gateState: 'failed',
    metrics: { auc: 0.72, latency_ms: 310, data_quality: 0.86, bias_gap: 0.09 },
    featureSignature: ['intent', 'language', 'account_tier'],
  },
];

export const approvals: Approval[] = [
  {
    id: 'apr-claims-prod',
    versionId: 'ver-claims-140',
    state: 'approved',
    requestedBy: 'Mina',
    decidedBy: 'Owen',
    reason: 'Critical claims routing package with validated bias and latency controls.',
  },
  {
    id: 'apr-revenue-stage',
    versionId: 'ver-revenue-210',
    state: 'requested',
    requestedBy: 'Ravi',
    reason: 'Forecast refresh for quarterly planning requires finance approval.',
  },
];

export const driftReports: DriftReport[] = [
  {
    id: 'drift-claims-week-34',
    versionId: 'ver-claims-140',
    severity: 'watch',
    baselineWindow: '2026-W31',
    observedWindow: '2026-W34',
    metrics: { population_stability_index: 0.13, accuracy_drop: 0.02, volume_shift: 0.18 },
  },
  {
    id: 'drift-revenue-week-34',
    versionId: 'ver-revenue-210',
    severity: 'breach',
    baselineWindow: '2026-W30',
    observedWindow: '2026-W34',
    metrics: { population_stability_index: 0.28, accuracy_drop: 0.05, volume_shift: 0.41 },
  },
];

export const deployments: Deployment[] = [
  {
    id: 'dep-claims-prod',
    versionId: 'ver-claims-140',
    stage: 'production',
    environment: 'prod-us',
    changeTicket: 'CHG-4821',
    createdBy: 'Owen',
    rolledBack: false,
  },
  {
    id: 'dep-revenue-stage',
    versionId: 'ver-revenue-210',
    stage: 'staging',
    environment: 'stage-eu',
    changeTicket: 'CHG-4890',
    createdBy: 'Ravi',
    rolledBack: false,
  },
];

export const experimentRuns: ExperimentRun[] = [
  { id: 'run-claims-q3-882', modelId: 'mdl-claims', owner: 'Mina', status: 'complete', metricDelta: 0.027 },
  { id: 'run-revenue-q3-221', modelId: 'mdl-revenue', owner: 'Ravi', status: 'running', metricDelta: -0.012 },
  { id: 'run-support-beta-019', modelId: 'mdl-support', owner: 'Kira', status: 'failed', metricDelta: -0.093 },
];
