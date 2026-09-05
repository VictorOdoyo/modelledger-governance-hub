export type RiskTier = 'low' | 'medium' | 'high' | 'critical';
export type GateState = 'not_run' | 'passed' | 'warning' | 'failed';
export type ApprovalState = 'requested' | 'approved' | 'rejected';
export type DeploymentStage = 'candidate' | 'staging' | 'production' | 'rolled_back';
export type DriftSeverity = 'none' | 'watch' | 'breach' | 'critical';

export interface RegisteredModel {
  id: string;
  name: string;
  owner: string;
  businessDomain: string;
  riskTier: RiskTier;
  tags: string[];
}

export interface ModelVersion {
  id: string;
  modelId: string;
  semanticVersion: string;
  sourceRunId: string;
  artifactUri: string;
  trainingDataset: string;
  stage: DeploymentStage;
  gateState: GateState;
  metrics: Record<string, number>;
  featureSignature: string[];
}

export interface Approval {
  id: string;
  versionId: string;
  state: ApprovalState;
  requestedBy: string;
  decidedBy?: string;
  reason: string;
}

export interface DriftReport {
  id: string;
  versionId: string;
  severity: DriftSeverity;
  baselineWindow: string;
  observedWindow: string;
  metrics: Record<string, number>;
}

export interface Deployment {
  id: string;
  versionId: string;
  stage: DeploymentStage;
  environment: string;
  changeTicket: string;
  createdBy: string;
  rolledBack: boolean;
}

export interface ExperimentRun {
  id: string;
  modelId: string;
  owner: string;
  status: 'queued' | 'running' | 'complete' | 'failed';
  metricDelta: number;
}
