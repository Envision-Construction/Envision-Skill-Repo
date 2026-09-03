# Which dispatch path? gke:dispatch vs Envision-MCP `dispatch_heavy_job` vs gsd-core

Three systems move work off the interactive session. They are not a fallback chain; each owns a
different shape of work. Pick by the table, then stop looking.

| You have | Use | Why |
|---|---|---|
| N independent shell commands or GSD plans, each in a container, results to GCS, resumable | **gke:dispatch** (this skill) | Wave manifest → Indexed Job / executor Jobs on `envision-compute`; idempotent replay by `wave_id` |
| A named Envision-MCP compute skill (`code_analysis`, `parallel_grep`, `test_runner`, `build_runner`, `dependency_audit`, `repo_indexing`, `document_search`, `bim_geometry_extraction`, `lidar_point_cloud`, `photo_progress_analysis`, `drawing_ocr`, `notebook_execution`) | **`dispatch_heavy_job(skill_id, input_data, …)`** via Envision-MCP | Calls the compute layer at `GatewayConfig.COMPUTE_LAYER_URL` (`gateway/compute/native_dispatch.py`), with graceful degradation to Vertex AI Search or a `suggest_local` hint. Timeout clamps to 10 s–10 min. Fixed catalog; no arbitrary images |
| A GSD phase to execute right now from this session | **gsd-core `execute-phase`** (`/gsd-execute-phase`) | In-process wave analysis from plan `wave:`/`depends_on`/`files_modified`, executors as subagents or the Workflow backend; commits land locally |
| A headless batch longer than ~5 h, a sweep, a red-team panel | Cloud Run jobs (placement doctrine) | 168 h task timeout, per-second billing |

Rules of thumb:

- `dispatch_heavy_job` does **not** read wave manifests and never touches
  `gs://gke-dispatch-claude-mcp-457317`. Its results come back inline through the MCP gateway.
- gke:dispatch does **not** know Envision-MCP skill ids. A task's `cmd` and `image` are the whole
  contract.
- gsd-core already ships the wave law (dependency waves, `files_modified` overlap → sequential
  stages, per-wave hooks). `run_roadmap.py --planning-dir` honors the same `wave:` frontmatter so
  a phase runs identically off-Mac; it does not re-derive a different DAG.

## Discovering `dispatch_heavy_job` from a session

```python
search("dispatch heavy job compute")          # envision-mcp gateway search
get_schema(tools=["dispatch_heavy_job"])
execute(code="""
result = await call_tool('dispatch_heavy_job', {
    'skill_id': 'test_runner',
    'input_data': {'repo_url': 'https://github.com/Envision-Construction/Envision-MCP.git',
                   'test_command': 'pytest tests/gateway -q', 'parallelism': 4},
    'timeout_ms': 600000,
})
""")
```

If `GKE_ENABLED` is false on the gateway, the call returns `status: degraded` or
`status: suggest_local` with alternatives. That is the gateway telling you the compute layer is
off, not a reason to hand-roll kubectl against it. For arbitrary containers, come back to this
skill.

## Related Cloud Run service

`gke-job-dispatcher` (`https://gke-job-dispatcher-5x7apc26sa-uc.a.run.app`, App Hub group
`envision-shared-services`) is Envision-MCP's dispatcher for its own notebook and compute jobs
(`gateway/webhooks/notebook_trigger.py`, `USE_GKE_NOTEBOOK_DISPATCH`). It is not part of
gke:dispatch and does not consume this skill's manifests.
