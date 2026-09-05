# Governance Workflows

1. A scientist registers a model and one or more model versions.
2. Evaluation metrics are compared against a risk-tier policy.
3. A version with failed gates cannot enter approval.
4. A requester cannot approve their own release package.
5. Production deployment requires an approved review.
6. Drift reports can reopen governance review after production exposure.
7. Rollbacks preserve the original deployment record and mark the version as rolled back.

The default policies are intentionally transparent and deterministic so reviewers
can inspect decisions without a live model-serving system.
