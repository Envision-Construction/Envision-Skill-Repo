#!/usr/bin/env python3
"""Tests for job_templates.py: YAML generation for K8s Jobs."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import yaml
import base64
import json

import pytest
from job_templates import (
    build_executor_jobs_yaml,
    build_indexed_job_yaml,
    build_job_yaml,
    validate_wave_shape,
    _job_name,
    _resources,
)


def _manifest(tasks, image="alpine:latest", **config_overrides):
    config = {
        "bucket": "gs://test-bucket",
        "namespace": "test-ns",
        "service_account": "test-sa",
        "parallelism_cap": None,
    }
    config.update(config_overrides)
    return {
        "wave_id": "test-wave-1",
        "tasks": [
            {
                "id": t["id"],
                "cmd": t.get("cmd", "echo hi"),
                "image": t.get("image", image),
                "status": t.get("status", "pending"),
                "resource_profile": t.get("resource_profile", "standard"),
                "timeout_seconds": t.get("timeout_seconds", 600),
                "retries": t.get("retries", 2),
                "inputs": t.get("inputs", {}),
            }
            for t in tasks
        ],
        "config": config,
    }


class TestJobName:
    def test_basic(self):
        assert _job_name("wave-1") == "gke-dispatch-wave-1"

    def test_underscores_replaced(self):
        assert _job_name("my_wave") == "gke-dispatch-my-wave"

    def test_truncated_to_63(self):
        name = _job_name("a" * 100)
        assert len(name) <= 63

    def test_with_suffix(self):
        name = _job_name("wave-1", "task-0")
        assert name == "gke-dispatch-wave-1-task-0"


class TestResources:
    def test_known_profiles(self):
        for profile in ("light", "standard", "heavy", "gpu"):
            r = _resources(profile)
            assert "cpu" in r
            assert "memory" in r

    def test_unknown_falls_back_to_standard(self):
        assert _resources("nonexistent") == _resources("standard")

    def test_gpu_has_gpu_key(self):
        r = _resources("gpu")
        assert "gpu" in r

    def test_gpu_pins_l4_not_any_spot_gpu(self):
        # Without an accelerator constraint a gpu task could land on the H100 spot pool.
        assert _resources("gpu")["accelerator"] == "nvidia-l4"
        assert _resources("gpu_high")["accelerator"] == "nvidia-h100-80gb"

    def test_no_a100_profile(self):
        # envision-compute has no A100 pool; a profile for it would never schedule.
        assert _resources("gpu_a100") == _resources("standard")


class TestBuildIndexedJobYaml:
    def test_empty_when_no_pending(self):
        m = _manifest([{"id": "t1", "status": "completed"}])
        assert build_indexed_job_yaml(m) == ""

    def test_generates_valid_yaml(self):
        m = _manifest([{"id": "t1"}, {"id": "t2"}])
        result = build_indexed_job_yaml(m)
        doc = yaml.safe_load(result)
        assert doc["kind"] == "Job"
        assert doc["spec"]["completionMode"] == "Indexed"
        assert doc["spec"]["completions"] == 2

    def test_namespace_from_config(self):
        m = _manifest([{"id": "t1"}], namespace="custom-ns")
        result = build_indexed_job_yaml(m)
        doc = yaml.safe_load(result)
        assert doc["metadata"]["namespace"] == "custom-ns"

    def test_resources_from_profile(self):
        m = _manifest([{"id": "t1", "resource_profile": "heavy"}])
        result = build_indexed_job_yaml(m)
        doc = yaml.safe_load(result)
        containers = doc["spec"]["template"]["spec"]["containers"]
        task_container = next(c for c in containers if c["name"] == "task")
        assert task_container["resources"]["requests"]["cpu"] == "8"
        assert task_container["resources"]["requests"]["memory"] == "16Gi"

    def test_has_log_shipper_sidecar(self):
        m = _manifest([{"id": "t1"}])
        result = build_indexed_job_yaml(m)
        doc = yaml.safe_load(result)
        containers = doc["spec"]["template"]["spec"]["containers"]
        names = [c["name"] for c in containers]
        assert "log-shipper" in names

    def test_has_idempotent_check_init(self):
        m = _manifest([{"id": "t1"}])
        result = build_indexed_job_yaml(m)
        doc = yaml.safe_load(result)
        inits = doc["spec"]["template"]["spec"]["initContainers"]
        assert inits[0]["name"] == "idempotent-check"

    def test_skips_completed_tasks(self):
        m = _manifest([
            {"id": "t1", "status": "completed"},
            {"id": "t2", "status": "pending"},
        ])
        result = build_indexed_job_yaml(m)
        doc = yaml.safe_load(result)
        assert doc["spec"]["completions"] == 1

    def _containers(self, doc):
        spec = doc["spec"]["template"]["spec"]
        by_name = {c["name"]: c for c in spec["containers"]}
        by_name.update({c["name"]: c for c in spec["initContainers"]})
        return by_name

    def test_task_container_needs_only_sh(self):
        # The 2026-08-18 pilot: postgres:17-alpine has no python3, so the old wrapper resolved
        # an empty command and reported a false "completed". Resolution now lives in the
        # cloud-sdk init container; the task container only reads /shared files.
        m = _manifest([{"id": "t1", "cmd": "echo hi", "image": "postgres:17-alpine"}])
        c = self._containers(yaml.safe_load(build_indexed_job_yaml(m)))
        assert "python3" not in c["task"]["args"][0]
        assert "python3" in c["idempotent-check"]["args"][0]
        assert "cat /shared/task_cmd" in c["task"]["args"][0]
        assert "FATAL: no task command resolved" in c["task"]["args"][0]

    def test_maps_survive_quotes_and_dollars(self):
        cmd = "echo 'it''s $HOME' && printf \"%s\" \"$(date)\""
        m = _manifest([{"id": "t-1", "cmd": cmd}, {"id": "t-2", "cmd": "true"}])
        c = self._containers(yaml.safe_load(build_indexed_job_yaml(m)))
        init = c["idempotent-check"]["args"][0]
        blobs = [line.split("'")[1] for line in init.splitlines() if line.strip().startswith("echo '")]
        assert len(blobs) == 2
        id_map = json.loads(base64.b64decode(blobs[0]))
        cmd_map = json.loads(base64.b64decode(blobs[1]))
        assert id_map == {"0": "t-1", "1": "t-2"}
        assert cmd_map["0"] == cmd

    def test_generic_tasks_not_pinned_to_spot_but_tolerate_it(self):
        # Generic tasks should take default-pool (on-demand) first; tolerations only open the
        # tainted spot/GPU pools for requests that do not fit there.
        m = _manifest([{"id": "t1", "resource_profile": "standard"}])
        spec = yaml.safe_load(build_indexed_job_yaml(m))["spec"]["template"]["spec"]
        assert "nodeSelector" not in spec
        assert "affinity" not in spec
        keys = {t["key"] for t in spec["tolerations"]}
        assert keys == {"cloud.google.com/gke-spot", "nvidia.com/gpu"}

    def test_gpu_indexed_task_requires_accelerator_and_tolerates_taint(self):
        # Without this a gpu-profile Indexed Job sat Pending forever: GPU pools are tainted.
        m = _manifest([{"id": "t1", "resource_profile": "gpu"}])
        spec = yaml.safe_load(build_indexed_job_yaml(m))["spec"]["template"]["spec"]
        terms = spec["affinity"]["nodeAffinity"]["requiredDuringSchedulingIgnoredDuringExecution"]["nodeSelectorTerms"]
        assert terms[0]["matchExpressions"][0]["values"] == ["nvidia-l4"]
        assert any(t["key"] == "nvidia.com/gpu" for t in spec["tolerations"])
        task = next(c for c in spec["containers"] if c["name"] == "task")
        assert task["resources"]["requests"]["nvidia.com/gpu"] == "1"

    def test_outputs_dir_is_on_shared_volume(self):
        # /outputs used to be container-private, so artifacts never reached GCS.
        m = _manifest([{"id": "t1"}])
        c = self._containers(yaml.safe_load(build_indexed_job_yaml(m)))
        for name in ("task", "log-shipper"):
            mounts = {v["mountPath"]: v for v in c[name]["volumeMounts"]}
            assert mounts["/outputs"]["name"] == "shared"
            assert mounts["/outputs"]["subPath"] == "outputs"


class TestBuildExecutorJobsYaml:
    def test_empty_when_no_pending(self):
        m = _manifest([{"id": "t1", "status": "completed", "image": "avireddy0/claude-executor:latest"}])
        assert build_executor_jobs_yaml(m) == ""

    def test_per_task_jobs(self):
        m = _manifest([
            {"id": "t1", "image": "avireddy0/claude-executor:latest"},
            {"id": "t2", "image": "avireddy0/claude-executor:latest"},
        ])
        result = build_executor_jobs_yaml(m)
        docs = list(yaml.safe_load_all(result))
        assert len(docs) == 2
        assert all(d["kind"] == "Job" for d in docs)

    def test_has_secrets_init(self):
        m = _manifest([{"id": "t1", "image": "avireddy0/claude-executor:latest"}])
        result = build_executor_jobs_yaml(m)
        doc = yaml.safe_load(result)
        inits = doc["spec"]["template"]["spec"]["initContainers"]
        assert inits[0]["name"] == "fetch-secrets"

    def test_env_vars_set(self):
        m = _manifest([{
            "id": "t1",
            "image": "avireddy0/claude-executor:latest",
            "inputs": {"repo_url": "https://github.com/test/repo.git", "plan_path": ".planning/PLAN.md"},
        }])
        result = build_executor_jobs_yaml(m)
        doc = yaml.safe_load(result)
        containers = doc["spec"]["template"]["spec"]["containers"]
        executor = next(c for c in containers if c["name"] == "executor")
        env_map = {e["name"]: e["value"] for e in executor["env"]}
        assert env_map["REPO_URL"] == "https://github.com/test/repo.git"
        assert env_map["PLAN_PATH"] == ".planning/PLAN.md"
        assert env_map["GITHUB_APP_ID"] == "3604031"
        assert env_map["MAX_BUDGET_USD"] == "5"
        assert "MAX_TURNS" not in env_map

    def test_budget_from_inputs(self):
        m = _manifest([{
            "id": "t1", "image": "avireddy0/claude-executor:latest",
            "inputs": {"max_budget_usd": "12"},
        }])
        doc = yaml.safe_load(build_executor_jobs_yaml(m))
        executor = next(c for c in doc["spec"]["template"]["spec"]["containers"] if c["name"] == "executor")
        env_map = {e["name"]: e["value"] for e in executor["env"]}
        assert env_map["MAX_BUDGET_USD"] == "12"

    def test_env_values_with_quotes_stay_valid_yaml(self):
        m = _manifest([{
            "id": "t1", "image": "avireddy0/claude-executor:latest",
            "cmd": 'echo "quoted" $VAR',
        }])
        doc = yaml.safe_load(build_executor_jobs_yaml(m))
        executor = next(c for c in doc["spec"]["template"]["spec"]["containers"] if c["name"] == "executor")
        env_map = {e["name"]: e["value"] for e in executor["env"]}
        assert env_map["TASK_CMD"] == 'echo "quoted" $VAR'

    def test_per_task_timeout_and_retries(self):
        # Previously every Job in the wave got max(timeout) and max(retries).
        m = _manifest([
            {"id": "short", "image": "avireddy0/claude-executor:latest", "timeout_seconds": 300, "retries": 0},
            {"id": "long", "image": "avireddy0/claude-executor:latest", "timeout_seconds": 3600, "retries": 3},
        ])
        docs = {d["metadata"]["labels"]["task-id"]: d for d in yaml.safe_load_all(build_executor_jobs_yaml(m))}
        assert docs["short"]["spec"]["activeDeadlineSeconds"] == 360
        assert docs["short"]["spec"]["backoffLimit"] == 0
        assert docs["long"]["spec"]["activeDeadlineSeconds"] == 3660
        assert docs["long"]["spec"]["backoffLimit"] == 3

    def test_dep_wait_uses_same_wave_branch(self):
        m = _manifest([
            {"id": "a", "image": "avireddy0/claude-executor:latest"},
            {"id": "b", "image": "avireddy0/claude-executor:latest", "depends_on": ["a"]},
        ])
        m["tasks"][1]["depends_on"] = ["a"]
        docs = {d["metadata"]["labels"]["task-id"]: d for d in yaml.safe_load_all(build_executor_jobs_yaml(m))}
        inits = [c["name"] for c in docs["b"]["spec"]["template"]["spec"]["initContainers"]]
        assert inits[0] == "wait-deps"
        assert "gke-dispatch/test-wave-1/$dep_id" in docs["b"]["spec"]["template"]["spec"]["initContainers"][0]["args"][0]


class TestValidateWaveShape:
    def test_mixed_executor_and_generic_rejected(self):
        with pytest.raises(ValueError, match="Mixed wave"):
            validate_wave_shape([
                {"id": "a", "image": "avireddy0/claude-executor:latest"},
                {"id": "b", "image": "alpine:latest"},
            ])

    def test_two_images_rejected(self):
        with pytest.raises(ValueError, match="one image"):
            validate_wave_shape([{"id": "a", "image": "alpine:3.20"}, {"id": "b", "image": "node:22"}])

    def test_two_profiles_rejected(self):
        with pytest.raises(ValueError, match="one resource_profile"):
            validate_wave_shape([
                {"id": "a", "image": "alpine", "resource_profile": "light"},
                {"id": "b", "image": "alpine", "resource_profile": "heavy"},
            ])

    def test_homogeneous_ok(self):
        validate_wave_shape([{"id": "a", "image": "alpine"}, {"id": "b", "image": "alpine"}])
        validate_wave_shape([
            {"id": "a", "image": "avireddy0/claude-executor:latest", "resource_profile": "light"},
            {"id": "b", "image": "avireddy0/claude-executor:latest", "resource_profile": "gpu"},
        ])

    def test_router_raises_on_mixed(self):
        m = _manifest([
            {"id": "a", "image": "avireddy0/claude-executor:latest"},
            {"id": "b", "image": "alpine:latest"},
        ])
        with pytest.raises(ValueError):
            build_job_yaml(m)


class TestBuildJobYamlRouter:
    def test_routes_to_executor(self):
        m = _manifest([{"id": "t1", "image": "avireddy0/claude-executor:latest"}])
        result = build_job_yaml(m)
        docs = list(yaml.safe_load_all(result))
        assert docs[0]["spec"]["template"]["spec"]["initContainers"][0]["name"] == "fetch-secrets"

    def test_routes_to_indexed(self):
        m = _manifest([{"id": "t1", "image": "alpine:latest"}])
        result = build_job_yaml(m)
        doc = yaml.safe_load(result)
        assert doc["spec"]["completionMode"] == "Indexed"

    def test_empty_when_all_done(self):
        m = _manifest([{"id": "t1", "status": "completed"}])
        assert build_job_yaml(m) == ""
