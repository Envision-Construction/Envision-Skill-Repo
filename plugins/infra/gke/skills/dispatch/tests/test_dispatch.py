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

    def test_null_cluster_uses_current_context(self):
        m = normalize("w", [{"id": "t", "cmd": "echo", "image": "alpine"}],
                      config_overrides={"cluster": None})
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
            {"id": "a", "cmd": "", "image": "avireddy0/claude-executor:latest"},
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
