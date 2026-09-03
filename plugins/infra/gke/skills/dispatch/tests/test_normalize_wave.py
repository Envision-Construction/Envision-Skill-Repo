#!/usr/bin/env python3
"""Tests for normalize_wave.py: validation, deduplication, cycle detection."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import pytest
from normalize_wave import check_dependency_cycles, normalize, validate_task


class TestValidateTask:
    def test_valid_task(self):
        task = {"id": "t1", "cmd": "echo hi", "image": "alpine:latest"}
        assert validate_task(task, 0) == []

    def test_missing_id(self):
        task = {"cmd": "echo hi", "image": "alpine:latest"}
        errors = validate_task(task, 0)
        assert any("missing 'id'" in e for e in errors)

    def test_missing_cmd(self):
        task = {"id": "t1", "image": "alpine:latest"}
        errors = validate_task(task, 0)
        assert any("missing 'cmd'" in e for e in errors)

    def test_missing_image(self):
        task = {"id": "t1", "cmd": "echo hi"}
        errors = validate_task(task, 0)
        assert any("missing 'image'" in e for e in errors)

    def test_invalid_resource_profile(self):
        task = {"id": "t1", "cmd": "echo hi", "image": "alpine", "resource_profile": "mega"}
        errors = validate_task(task, 0)
        assert any("invalid resource_profile" in e for e in errors)

    def test_valid_profiles(self):
        for profile in ("light", "standard", "heavy", "gpu"):
            task = {"id": "t1", "cmd": "echo", "image": "alpine", "resource_profile": profile}
            assert validate_task(task, 0) == []

    def test_negative_timeout(self):
        task = {"id": "t1", "cmd": "echo", "image": "alpine", "timeout_seconds": -1}
        errors = validate_task(task, 0)
        assert any("timeout_seconds" in e for e in errors)

    def test_negative_retries(self):
        task = {"id": "t1", "cmd": "echo", "image": "alpine", "retries": -1}
        errors = validate_task(task, 0)
        assert any("retries" in e for e in errors)

    def test_zero_retries_valid(self):
        task = {"id": "t1", "cmd": "echo", "image": "alpine", "retries": 0}
        assert validate_task(task, 0) == []


class TestCheckDependencyCycles:
    def test_no_deps(self):
        tasks = [{"id": "a"}, {"id": "b"}]
        assert check_dependency_cycles(tasks) == []

    def test_valid_chain(self):
        tasks = [
            {"id": "a", "depends_on": []},
            {"id": "b", "depends_on": ["a"]},
            {"id": "c", "depends_on": ["b"]},
        ]
        assert check_dependency_cycles(tasks) == []

    def test_direct_cycle(self):
        tasks = [
            {"id": "a", "depends_on": ["b"]},
            {"id": "b", "depends_on": ["a"]},
        ]
        errors = check_dependency_cycles(tasks)
        assert any("cycle" in e.lower() for e in errors)

    def test_unknown_dependency(self):
        tasks = [{"id": "a", "depends_on": ["nonexistent"]}]
        errors = check_dependency_cycles(tasks)
        assert any("unknown task" in e for e in errors)

    def test_self_cycle(self):
        tasks = [{"id": "a", "depends_on": ["a"]}]
        errors = check_dependency_cycles(tasks)
        assert any("cycle" in e.lower() for e in errors)


class TestNormalize:
    def test_basic_manifest(self):
        tasks = [
            {"id": "t1", "cmd": "echo 1", "image": "alpine"},
            {"id": "t2", "cmd": "echo 2", "image": "alpine"},
        ]
        manifest = normalize("test-wave", tasks)
        assert manifest["wave_id"] == "test-wave"
        assert manifest["status"] == "pending"
        assert len(manifest["tasks"]) == 2
        assert manifest["metrics"]["total_tasks"] == 2
        assert manifest["metrics"]["pending"] == 2
        assert manifest["metrics"]["completed"] == 0

    def test_task_defaults(self):
        tasks = [{"id": "t1", "cmd": "echo", "image": "alpine"}]
        manifest = normalize("w", tasks)
        t = manifest["tasks"][0]
        assert t["resource_profile"] == "standard"
        assert t["timeout_seconds"] == 600
        assert t["retries"] == 2
        assert t["status"] == "pending"
        assert t["result"] is None
        assert t["index"] == 0

    def test_preserves_inputs(self):
        tasks = [{"id": "t1", "cmd": "echo", "image": "alpine",
                  "inputs": {"key": "value"}}]
        manifest = normalize("w", tasks)
        assert manifest["tasks"][0]["inputs"] == {"key": "value"}

    def test_duplicate_ids_exits(self):
        tasks = [
            {"id": "dup", "cmd": "echo 1", "image": "alpine"},
            {"id": "dup", "cmd": "echo 2", "image": "alpine"},
        ]
        with pytest.raises(SystemExit):
            normalize("w", tasks)

    def test_config_defaults(self):
        tasks = [{"id": "t1", "cmd": "echo", "image": "alpine"}]
        manifest = normalize("w", tasks)
        assert manifest["config"]["bucket"] == "gs://gke-dispatch-claude-mcp-457317"
        assert manifest["config"]["namespace"] == "gke-dispatch"

    def test_config_overrides(self):
        tasks = [{"id": "t1", "cmd": "echo", "image": "alpine"}]
        manifest = normalize("w", tasks, config_overrides={"namespace": "custom"})
        assert manifest["config"]["namespace"] == "custom"
        assert manifest["config"]["bucket"] == "gs://gke-dispatch-claude-mcp-457317"

    def test_git_sha_preserved(self):
        tasks = [{"id": "t1", "cmd": "echo", "image": "alpine"}]
        manifest = normalize("w", tasks, git_sha="abc123")
        assert manifest["git_sha"] == "abc123"

    def test_framework_recorded(self):
        tasks = [{"id": "t1", "cmd": "echo", "image": "alpine"}]
        manifest = normalize("w", tasks, framework="gsd")
        assert manifest["source_framework"] == "gsd"
