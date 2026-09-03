# GKE Cluster Setup: Remediation Reference

Consult this when a script fails, not before. The dispatch scripts assume the state below, which
was verified live on 2026-09-03.

## What exists

| Thing | Value |
|---|---|
| Project | `claude-mcp-457317` |
| Cluster | `envision-compute`, region `us-central1`, GKE Standard, STABLE channel, Workload Identity on |
| kubeconfig context | `gke_claude-mcp-457317_us-central1_envision-compute` (the default in `config.cluster`) |
| Namespace | `gke-dispatch` (only on this cluster; `envision-delta-gke` and `envision-cockpit-uswest1` do not have it) |
| KSA to GSA | `gke-dispatch-worker` bound to `gke-dispatch-sa@claude-mcp-457317.iam.gserviceaccount.com` (`roles/storage.objectAdmin`, Secret Manager access) |
| Bucket | `gs://gke-dispatch-claude-mcp-457317` (`waves/` prefix; 30-day lifecycle) |
| Job TTL | `ttlSecondsAfterFinished: 3600`; finished Jobs vanish from `kubectl` after an hour. GCS is the record. |

Node pools on `envision-compute`:

| Pool | Machine | Spot | GPU | Max nodes | Labels / taints |
|---|---|---|---|---|---|
| `default-pool` | e2-standard-4 | no | none | 3 | untainted; first fit for generic Indexed Job tasks (`light`/`standard`); executor tasks never land here (spot pin) |
| `l4-inference-pool` | g2-standard-8 | yes | 1x L4 | 5 | `gpu-type=nvidia-l4`, taint `nvidia.com/gpu` |
| `l4-dual-gpu-pool` | g2-standard-24 | yes | 2x L4 | 2 | `gpu-type=nvidia-l4-dual`, taint `nvidia.com/gpu` |
| `h100-spot-pool` | a3-highgpu-1g | yes | 1x H100 80GB | 3 | taint `nvidia.com/gpu`; spot quota 3 in us-central1 |
| `l4-ondemand-pool` | g2-standard-8 | no | 1x L4 | 1 | not selected by the spot pin |

Executor Jobs carry `nodeSelector: cloud.google.com/gke-spot: "true"` plus a preference for
`nvidia-l4-dual`, then `nvidia-l4`. Every spot pool is a GPU pool, so a CPU-only `standard`
executor task boots an L4 spot node. GPU pools idle at zero most of the time: budget 2 to 5
minutes of scale-up before the first executor pod runs. To let executor tasks use `default-pool`
instead, drop the `nodeSelector` block in `job_templates.build_executor_job` (a deliberate
change, not a fix). Generic Indexed Job tasks are not pinned: they take `default-pool` when the
request fits (`light`, `standard`) and tolerate the spot/GPU taints otherwise (`heavy`, `gpu`,
`gpu_high`), so their start-up is usually an image pull, 1 to 2 minutes.

## Error: `namespaces "gke-dispatch" not found`

You are on another cluster's context (the usual current-context is `envision-delta-gke`). The
scripts pin the context from `config.cluster`; if you ran `kubectl` by hand, add
`--context gke_claude-mcp-457317_us-central1_envision-compute`. If the context is missing from
kubeconfig:

```bash
gcloud container clusters get-credentials envision-compute \
  --region us-central1 --project claude-mcp-457317
```

## Error: pod stuck `Pending` (`didn't match Pod's node affinity/selector`, `Insufficient nvidia.com/gpu`)

Normal for the first few minutes: the autoscaler is adding a spot node. Check:

```bash
kubectl --context gke_claude-mcp-457317_us-central1_envision-compute \
  get pods -n gke-dispatch -o wide
kubectl --context gke_claude-mcp-457317_us-central1_envision-compute \
  get events -n gke-dispatch --sort-by=.lastTimestamp | tail -20
```

If it stays pending past roughly 10 minutes: spot capacity or quota. Modern GPU quotas are
invisible to `gcloud compute regions describe`; use the quotas API:

```bash
gcq us-central1 claude-mcp-457317 gpu      # global/scripts/gcq.sh
```

`gpu_high` needs H100 spot quota (3 as of 2026-09-03). There is no A100 pool; a task that
requires one never schedules.

## Error: executor pod fails in `fetch-secrets`

Workload Identity binding or Secret Manager access. Verify:

```bash
kubectl --context gke_claude-mcp-457317_us-central1_envision-compute \
  get sa gke-dispatch-worker -n gke-dispatch -o jsonpath='{.metadata.annotations}'
gcloud iam service-accounts get-iam-policy \
  gke-dispatch-sa@claude-mcp-457317.iam.gserviceaccount.com --project claude-mcp-457317
gcloud secrets list --project claude-mcp-457317 --filter='name~gsd'
```

Expected annotation: `iam.gke.io/gcp-service-account=gke-dispatch-sa@claude-mcp-457317.iam.gserviceaccount.com`.
Expected secrets: `gsd-claude-oauth-token`, `gsd-github-app-private-key`.

Recreate the binding only if it is genuinely missing:

```bash
kubectl --context gke_claude-mcp-457317_us-central1_envision-compute \
  create serviceaccount gke-dispatch-worker -n gke-dispatch
gcloud iam service-accounts add-iam-policy-binding \
  gke-dispatch-sa@claude-mcp-457317.iam.gserviceaccount.com \
  --role="roles/iam.workloadIdentityUser" \
  --member="serviceAccount:claude-mcp-457317.svc.id.goog[gke-dispatch/gke-dispatch-worker]"
kubectl --context gke_claude-mcp-457317_us-central1_envision-compute \
  annotate serviceaccount gke-dispatch-worker -n gke-dispatch \
  iam.gke.io/gcp-service-account=gke-dispatch-sa@claude-mcp-457317.iam.gserviceaccount.com
```

## Error: `kubectl get jobs` shows nothing for a wave I dispatched

Jobs are garbage-collected one hour after finishing. Read the wave from GCS instead:

```bash
gcloud storage cat gs://gke-dispatch-claude-mcp-457317/waves/<wave_id>/manifest.json
gcloud storage ls -r gs://gke-dispatch-claude-mcp-457317/waves/<wave_id>/outputs/
```

## Error: task pod exits 1 with `FATAL: no task command resolved`

The init container could not map `JOB_COMPLETION_INDEX` to a task. Regenerate the manifest with
`normalize_wave.py`; hand-edited manifests with missing `index` fields or duplicate ids cause this.

## Error: GCS bucket does not exist / permission denied from pod

The bucket exists today. If it is ever recreated:

```bash
gcloud storage buckets create gs://gke-dispatch-claude-mcp-457317 \
  --project claude-mcp-457317 --location us-central1
gcloud storage buckets update gs://gke-dispatch-claude-mcp-457317 \
  --lifecycle-file=<(echo '{"rule":[{"action":{"type":"Delete"},"condition":{"age":30}}]}')
gcloud projects add-iam-policy-binding claude-mcp-457317 \
  --member="serviceAccount:gke-dispatch-sa@claude-mcp-457317.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"
```

## Optional: resource quota on the namespace

Only if you want to cap what gke-dispatch can consume:

```bash
kubectl --context gke_claude-mcp-457317_us-central1_envision-compute apply -f - <<'EOF'
apiVersion: v1
kind: ResourceQuota
metadata:
  name: gke-dispatch-quota
  namespace: gke-dispatch
spec:
  hard:
    requests.cpu: "64"
    requests.memory: 128Gi
    count/jobs.batch: "100"
EOF
```

## Not implemented: pod pool

`config.mode: pod-pool` was designed (pre-warmed Deployment + HPA on a Pub/Sub queue) and never
built. `dispatch.py` prints a notice and uses the Indexed Job path. Do not deploy a runner pool
expecting the scripts to use it.
