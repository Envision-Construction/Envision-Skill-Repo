#!/usr/bin/env python3
"""Shared GCS utilities and constants for gke-dispatch scripts."""

import json
import subprocess
import tempfile
from pathlib import Path


# Profiles map to envision-compute node pools (verified 2026-09-03):
#   generic tasks (Indexed Job): default-pool (on-demand e2-standard-4) first; heavy (8 CPU) only
#     fits a tolerated spot GPU node (g2-standard-24), so it waits for scale-up
#   executor tasks: pinned to spot (preferred: l4-dual-gpu-pool, then l4-inference-pool)
#   gpu                  -> nvidia-l4 required (l4-inference-pool / l4-dual-gpu-pool, spot)
#   gpu_high             -> nvidia-h100-80gb required (h100-spot-pool, spot quota 3 in us-central1)
# There is no A100 pool on envision-compute; an A100 profile would never schedule.
RESOURCE_PROFILES = {
    "light": {"cpu": "500m", "memory": "512Mi", "cpu_limit": "1", "memory_limit": "1Gi"},
    "standard": {"cpu": "2", "memory": "4Gi", "cpu_limit": "4", "memory_limit": "8Gi"},
    "heavy": {"cpu": "8", "memory": "16Gi", "cpu_limit": "16", "memory_limit": "32Gi"},
    "gpu": {
        "cpu": "4", "memory": "16Gi", "cpu_limit": "8", "memory_limit": "32Gi",
        "gpu": "1", "accelerator": "nvidia-l4",
    },
    "gpu_high": {
        "cpu": "8", "memory": "64Gi", "cpu_limit": "16", "memory_limit": "128Gi",
        "gpu": "1", "accelerator": "nvidia-h100-80gb",
    },
}

DEFAULT_CONFIG = {
    "mode": "auto",
    "parallelism_cap": None,
    "bucket": "gs://gke-dispatch-claude-mcp-457317",
    "namespace": "gke-dispatch",
    # The gke-dispatch namespace, worker SA, and Workload Identity binding exist ONLY on
    # envision-compute. This is the kubeconfig context name gcloud generates for it.
    "cluster": "gke_claude-mcp-457317_us-central1_envision-compute",
    "node_pool": None,
    "service_account": "gke-dispatch-worker",
}


def run(cmd: list[str], check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check, capture_output=capture, text=True)


def gcs_exists(path: str) -> bool:
    return run(["gsutil", "ls", path], check=False).returncode == 0


def gcs_read_json(path: str) -> dict | None:
    result = run(["gsutil", "cat", path], check=False)
    if result.returncode != 0:
        return None
    return json.loads(result.stdout)


def gcs_write_json(path: str, data: dict) -> None:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(data, f, indent=2)
        tmp = f.name
    run(["gsutil", "cp", tmp, path])
    Path(tmp).unlink()


def gcs_list(prefix: str) -> list[str]:
    result = run(["gsutil", "ls", prefix], check=False)
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
