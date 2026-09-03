#!/usr/bin/env python3
"""Tests for dispatch.py: dry-run must not write to GCS; cluster context pinning; mixed waves."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import dispatch
from normalize_wave import normalize


def _write_manifest(tmp_path, tasks, **config):
    manifest = normalize("test-wave", tasks, config_overrides=config or None)
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest))
    return path


class TestKubectlArgs:
    def test_default_pins_envision_compute(self):
        m = normalize("w", [{"id": "t", "cmd": "echo", "image": "alpine"}])
        assert dispatch.kubectl_args(m) == [
            "kubectl", "--context", "gke_claude-mcp-457317_us-central1_envision-compute",
        ]

    def test_null_cluster_falls_back_to_envision_compute(self):
        # Manifests written before 2026-09-03 carry cluster: null; bare kubectl would hit the
        # current context (envision-delta-gke), which has no gke-dispatch namespace.
        m = normalize("w", [{"id": "t", "cmd": "echo", "image": "alpine"}],
                      config_overrides={"cluster": None})
        assert dispatch.kubectl_args(m) == [
            "kubectl", "--context", "gke_claude-mcp-457317_us-central1_envision-compute",
        ]

    def test_current_opts_into_kubectl_current_context(self):
        m = normalize("w", [{"id": "t", "cmd": "echo", "image": "alpine"}],
                      config_overrides={"cluster": "current"})
        assert dispatch.kubectl_args(m) == ["kubectl"]


class TestDryRun:
    def test_dry_run_writes_nothing_to_gcs(self, tmp_path, monkeypatch, capsys):
        path = _write_manifest(tmp_path, [{"id": "t1", "cmd": "echo hi", "image": "alpine:3.20"}])
        monkeypatch.setattr(dispatch, "gcs_read_json", lambda p: None)

        def boom(*a, **k):
            raise AssertionError("GCS write attempted during --dry-run")

        monkeypatch.setattr(dispatch, "gcs_write_json", boom)
        monkeypatch.setattr(dispatch, "upload_inputs", boom)
        monkeypatch.setattr(dispatch, "run", boom)  # no kubectl either
        monkeypatch.setattr(sys, "argv", ["dispatch.py", "--manifest", str(path), "--dry-run"])

        with pytest.raises(SystemExit) as exc:
            dispatch.main()
        assert exc.value.code == 0
        out = capsys.readouterr()
        assert "kind: Job" in out.out
        assert "--context gke_claude-mcp-457317_us-central1_envision-compute" in out.err
        assert "no GCS writes" in out.err

    def test_mixed_wave_rejected_before_any_write(self, tmp_path, monkeypatch, capsys):
        path = _write_manifest(tmp_path, [
            {"id": "a", "cmd": "", "image": "us-central1-docker.pkg.dev/claude-mcp-457317/envision/claude-executor:20260903"},
            {"id": "b", "cmd": "echo", "image": "alpine:3.20"},
        ])
        monkeypatch.setattr(dispatch, "gcs_read_json", lambda p: None)

        def boom(*a, **k):
            raise AssertionError("GCS write attempted for a rejected manifest")

        monkeypatch.setattr(dispatch, "gcs_write_json", boom)
        monkeypatch.setattr(sys, "argv", ["dispatch.py", "--manifest", str(path)])

        with pytest.raises(SystemExit) as exc:
            dispatch.main()
        assert exc.value.code == 1
        assert "Manifest rejected" in capsys.readouterr().err

    def test_cluster_override_flag(self, tmp_path, monkeypatch, capsys):
        path = _write_manifest(tmp_path, [{"id": "t1", "cmd": "echo hi", "image": "alpine:3.20"}])
        monkeypatch.setattr(dispatch, "gcs_read_json", lambda p: None)
        monkeypatch.setattr(sys, "argv", [
            "dispatch.py", "--manifest", str(path), "--dry-run", "--cluster", "my-ctx",
        ])
        with pytest.raises(SystemExit):
            dispatch.main()
        assert "--context my-ctx" in capsys.readouterr().err


class TestSelectMode:
    def test_pod_pool_resolves_to_indexed(self, capsys):
        m = normalize("w", [{"id": "t", "cmd": "echo", "image": "alpine"}],
                      config_overrides={"mode": "pod-pool"})
        assert dispatch.select_mode(m) == "indexed-job"
        assert "not implemented" in capsys.readouterr().err

    def test_auto_is_indexed(self):
        m = normalize("w", [{"id": "t", "cmd": "echo", "image": "alpine"}])
        assert dispatch.select_mode(m) == "indexed-job"


class TestRetrySemantics:
    def test_local_failed_task_is_retried_without_gcs_manifest(self, tmp_path, monkeypatch, capsys):
        # Before: a failed task in a local-only manifest produced "All tasks already completed".
        path = _write_manifest(tmp_path, [{"id": "t1", "cmd": "echo", "image": "alpine:3.20"}])
        m = json.loads(path.read_text())
        m["tasks"][0]["status"] = "failed"
        m["tasks"][0]["result"] = {"exit_code": 1}
        path.write_text(json.dumps(m))
        monkeypatch.setattr(dispatch, "gcs_read_json", lambda p: None)
        monkeypatch.setattr(dispatch, "run", lambda *a, **k: (_ for _ in ()).throw(AssertionError("no writes")))
        monkeypatch.setattr(sys, "argv", ["dispatch.py", "--manifest", str(path), "--dry-run"])
        with pytest.raises(SystemExit) as exc:
            dispatch.main()
        assert exc.value.code == 0
        out = capsys.readouterr()
        assert "Retrying 1 failed task(s)" in out.err
        assert "kind: Job" in out.out

    def test_reconcile_adopts_success_and_archives_failure(self, monkeypatch):
        m = normalize("w", [
            {"id": "done", "cmd": "true", "image": "alpine"},
            {"id": "broke", "cmd": "false", "image": "alpine"},
            {"id": "fresh", "cmd": "true", "image": "alpine"},
        ])
        results = {
            "gs://b/waves/w/outputs/done/result.json": {"exit_code": 0, "duration_seconds": 12},
            "gs://b/waves/w/outputs/broke/result.json": {"exit_code": 1},
        }
        monkeypatch.setattr(dispatch, "gcs_read_json", lambda p: results.get(p))
        moves = []
        monkeypatch.setattr(dispatch, "run", lambda cmd, **k: moves.append(cmd))
        summary = dispatch.reconcile_with_results(m, "gs://b", dry_run=False)
        by_id = {t["id"]: t for t in m["tasks"]}
        assert by_id["done"]["status"] == "completed"
        assert by_id["broke"]["status"] == "pending"
        assert by_id["fresh"]["status"] == "pending"
        assert summary == {"adopted": ["done"], "archived": ["broke"]}
        assert len(moves) == 1 and moves[0][:2] == ["gsutil", "mv"]
        assert "result.prev-" in moves[0][3]
        assert m["metrics"] == {**m["metrics"], "completed": 1, "pending": 2, "failed": 0}

    def test_reconcile_dry_run_moves_nothing(self, monkeypatch):
        m = normalize("w", [{"id": "broke", "cmd": "false", "image": "alpine"}])
        monkeypatch.setattr(dispatch, "gcs_read_json", lambda p: {"exit_code": 1})
        monkeypatch.setattr(dispatch, "run", lambda *a, **k: (_ for _ in ()).throw(AssertionError("moved")))
        assert dispatch.reconcile_with_results(m, "gs://b", dry_run=True) == {"adopted": [], "archived": ["broke"]}

    def test_is_error_result_is_not_adopted(self, monkeypatch):
        m = normalize("w", [{"id": "t", "cmd": "", "image": "us-central1-docker.pkg.dev/claude-mcp-457317/envision/claude-executor:20260903"}])
        monkeypatch.setattr(dispatch, "gcs_read_json", lambda p: {"exit_code": 0, "is_error": True})
        monkeypatch.setattr(dispatch, "run", lambda cmd, **k: None)
        assert dispatch.reconcile_with_results(m, "gs://b", dry_run=False)["archived"] == ["t"]

    def test_unknown_dependency_rejected(self, tmp_path, monkeypatch, capsys):
        # Hand-edited manifests skip normalize_wave.py; the old dispatcher applied them and the
        # pod polled forever for a result that could never appear.
        path = _write_manifest(tmp_path, [{"id": "a", "cmd": "", "image": "us-central1-docker.pkg.dev/claude-mcp-457317/envision/claude-executor:20260903"}])
        m = json.loads(path.read_text()); m["tasks"][0]["depends_on"] = ["plan-32-02"]
        path.write_text(json.dumps(m))
        monkeypatch.setattr(dispatch, "gcs_read_json", lambda p: None)
        monkeypatch.setattr(sys, "argv", ["dispatch.py", "--manifest", str(path), "--dry-run"])
        with pytest.raises(SystemExit) as exc:
            dispatch.main()
        assert exc.value.code == 1
        assert "unknown task 'plan-32-02'" in capsys.readouterr().err
