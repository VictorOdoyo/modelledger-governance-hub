import { describe, expect, it } from 'vitest';

import { approvals, deployments, driftReports, models, versions } from '../data/seed';
import { countProductionDeployments, modelsNeedingAttention, policyCompletion } from './selectors';

describe('governance selectors', () => {
  it('counts only active production deployments', () => {
    expect(countProductionDeployments(deployments)).toBe(1);
  });

  it('finds models with failed gates, pending approval, or drift breach', () => {
    const names = modelsNeedingAttention(models, versions, approvals, driftReports).map(({ model }) => model.name);
    expect(names).toEqual(['Revenue Forecast', 'Support Deflection']);
  });

  it('measures policy metric completeness', () => {
    expect(policyCompletion(versions[0])).toBe(100);
  });
});
