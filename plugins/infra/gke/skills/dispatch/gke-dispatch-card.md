## Description: <br>
Run 2+ independent tasks in parallel on GKE cluster envision-compute (claude-mcp-457317) as Kubernetes Jobs: generic container commands or Claude Code plan executions in the claude-executor image, with results in GCS and idempotent replay keyed by wave id. Covers single waves, GSD planning-dir execution, and multi-phase roadmaps with checkpoint resume. <br>

This skill is ready for commercial/non-commercial use. <br>

## Third-Party Community Consideration
This skill is not owned or developed by NVIDIA. This skill has been developed and built to a third-party's requirements for this application and use case; see link to Non-NVIDIA [Envision Construction Agent Card](https://github.com/Envision-Construction/Envision-Skill-Repo). <br>

### License/Terms of Use: <br>
UNLICENSED (Prometheus Ventures / Envision Construction internal). <br>

## Use Case: <br>
Engineers and orchestration agents moving parallel work units (shell tasks in containers, or Claude Code plan executions) off the workstation onto the envision-compute GKE cluster, with every result recorded in GCS and safe re-runs. <br>

### Deployment Geography for Use: <br>
Global (cluster and bucket are in us-central1). <br>

## Requirements / Dependencies: <br>
**Requires API Key or External Credential:** [Yes] <br>
**Credential Type(s):** [OAuth Token, Cloud Credentials] <br>

Credentials never appear in manifests or images: executor pods fetch the Claude OAuth token and the GitHub App private key from Secret Manager through Workload Identity at start. Operator needs gcloud auth for project claude-mcp-457317 and the envision-compute kubeconfig context. Do not include secrets in prompts/logs/output; use least-privilege credentials; rotate keys as appropriate. <br>

## Known Risks and Mitigations: <br>
Risk: Executor tasks run Claude Code with permissions bypassed inside the pod and push branches to GitHub. <br>
Mitigation: Pods run as a non-root user in an isolated Job; pushes go only to `gke-dispatch/<wave>/<task>` branches, never `main`; spend is capped per task by `max_budget_usd`. <br>
Risk: The published executor image (Docker Hub, 2026-05-08) lags the entrypoint in this repo. <br>
Mitigation: `references/executor-image.md` documents the staleness, the rebuild, and a smoke test; dispatch executor waves only after rebuilding. <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment; 99 unit tests cover manifest validation, Job YAML generation, dry-run isolation, and roadmap parsing. <br>

## Reference(s): <br>
- [manifest-schema.md](references/manifest-schema.md) <br>
- [multi-phase-milestone.md](references/multi-phase-milestone.md) <br>
- [executor-image.md](references/executor-image.md) <br>
- [cluster-setup.md](references/cluster-setup.md) <br>
- [envision-mcp-integration.md](references/envision-mcp-integration.md) <br>

## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks, JSON wave manifests, Kubernetes Job YAML] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results persisted to gs://gke-dispatch-claude-mcp-457317/waves/<wave_id>/] <br>

## Skill Version(s): <br>
1.1.0 (gke plugin version; upgraded 2026-09-03; git SHA assigned at commit) <br>
