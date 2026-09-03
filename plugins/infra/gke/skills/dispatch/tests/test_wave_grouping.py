#!/usr/bin/env python3
"""Tests for wave grouping and phase batching algorithms in run_roadmap.py."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from run_roadmap import (
    build_branch_lookup,
    build_wave_tasks,
    create_roadmap_state,
    extract_files_modified,
    extract_phase_title,
    group_by_declared_waves,
    group_into_waves,
    group_phases_into_batches,
    get_phase_files,
    parse_frontmatter,
    parse_planning_dir,
)


class TestGroupIntoWaves:
    def test_empty(self):
        assert group_into_waves([]) == []

    def test_no_overlap_single_wave(self):
        plans = [
            {"id": "a", "files_modified": ["src/a.ts"]},
            {"id": "b", "files_modified": ["src/b.ts"]},
            {"id": "c", "files_modified": ["src/c.ts"]},
        ]
        waves = group_into_waves(plans)
        assert len(waves) == 1
        assert len(waves[0]) == 3

    def test_full_overlap_sequential(self):
        plans = [
            {"id": "a", "files_modified": ["src/shared.ts"]},
            {"id": "b", "files_modified": ["src/shared.ts"]},
            {"id": "c", "files_modified": ["src/shared.ts"]},
        ]
        waves = group_into_waves(plans)
        assert len(waves) == 3
        assert all(len(w) == 1 for w in waves)

    def test_partial_overlap(self):
        plans = [
            {"id": "a", "files_modified": ["src/auth.ts"]},
            {"id": "b", "files_modified": ["src/db.ts"]},
            {"id": "c", "files_modified": ["src/auth.ts", "src/db.ts"]},
        ]
        waves = group_into_waves(plans)
        assert len(waves) == 2
        wave1_ids = {p["id"] for p in waves[0]}
        assert wave1_ids == {"a", "b"}
        wave2_ids = {p["id"] for p in waves[1]}
        assert wave2_ids == {"c"}

    def test_no_files_modified(self):
        plans = [
            {"id": "a", "files_modified": []},
            {"id": "b", "files_modified": []},
        ]
        waves = group_into_waves(plans)
        assert len(waves) == 1
        assert len(waves[0]) == 2

    def test_missing_files_modified_key(self):
        plans = [{"id": "a"}, {"id": "b"}]
        waves = group_into_waves(plans)
        assert len(waves) == 1

    def test_single_plan(self):
        plans = [{"id": "a", "files_modified": ["x.ts"]}]
        waves = group_into_waves(plans)
        assert len(waves) == 1
        assert waves[0][0]["id"] == "a"


class TestGroupPhasesIntoBatches:
    def _phase(self, files):
        return {"waves": [[{"files_modified": files}]]}

    def test_empty(self):
        assert group_phases_into_batches([]) == []

    def test_no_overlap(self):
        phases = [
            self._phase(["a.ts"]),
            self._phase(["b.ts"]),
            self._phase(["c.ts"]),
        ]
        batches = group_phases_into_batches(phases)
        assert len(batches) == 1
        assert sorted(batches[0]) == [0, 1, 2]

    def test_full_overlap(self):
        phases = [
            self._phase(["shared.ts"]),
            self._phase(["shared.ts"]),
        ]
        batches = group_phases_into_batches(phases)
        assert len(batches) == 2

    def test_start_index(self):
        phases = [
            self._phase(["a.ts"]),
            self._phase(["b.ts"]),
            self._phase(["c.ts"]),
        ]
        batches = group_phases_into_batches(phases, start_index=1)
        assert len(batches) == 1
        assert sorted(batches[0]) == [1, 2]

    def test_mixed_overlap(self):
        phases = [
            self._phase(["a.ts"]),
            self._phase(["b.ts"]),
            self._phase(["a.ts", "b.ts"]),
        ]
        batches = group_phases_into_batches(phases)
        assert len(batches) == 2
        assert sorted(batches[0]) == [0, 1]
        assert batches[1] == [2]


class TestGetPhaseFiles:
    def test_collects_across_waves(self):
        phase = {
            "waves": [
                [{"files_modified": ["a.ts"]}, {"files_modified": ["b.ts"]}],
                [{"files_modified": ["c.ts", "a.ts"]}],
            ]
        }
        assert get_phase_files(phase) == {"a.ts", "b.ts", "c.ts"}

    def test_empty_phase(self):
        assert get_phase_files({"waves": []}) == set()
        assert get_phase_files({}) == set()


class TestExtractFilesModified:
    def test_basic(self):
        text = """# Plan
## Files Modified
- `src/auth.ts`
- `src/db.ts`

## Tasks
"""
        files = extract_files_modified(text)
        assert files == ["src/auth.ts", "src/db.ts"]

    def test_files_to_modify_header(self):
        text = """## Files to Modify
- src/api.py
- src/models.py
"""
        files = extract_files_modified(text)
        assert files == ["src/api.py", "src/models.py"]

    def test_no_section(self):
        text = "# Just a plan\nSome content"
        assert extract_files_modified(text) == []

    def test_stops_at_next_header(self):
        text = """## files_modified
- a.ts
- b.ts
## Next Section
- not_a_file.ts
"""
        files = extract_files_modified(text)
        assert files == ["a.ts", "b.ts"]


class TestExtractPhaseTitle:
    def test_basic(self):
        text = "## Phase 3: Authentication Layer\n"
        assert extract_phase_title(text, "3") == "Authentication Layer"

    def test_em_dash(self):
        text = "## Phase 1 \u2014 Foundation\n"  # em dash, as real ROADMAP.md files write it
        assert extract_phase_title(text, "1") == "Foundation"

    def test_not_found(self):
        text = "## Something else\n"
        assert extract_phase_title(text, "5") is None

    def test_no_title(self):
        text = "## Phase 2\n"
        title = extract_phase_title(text, "2")
        assert title == "Phase 2"


class TestParseFrontmatter:
    def test_gsd_plan_keys(self):
        text = """---
phase: "330-pathway-parity"
plan: "330-02"
type: "feature"
wave: 2
depends_on:
  - "330-01"
files_modified: [src/a.ts, "src/b.ts"]
must_haves:
  truths:
    - "nested lists are ignored"
---
# Plan body
"""
        fm = parse_frontmatter(text)
        assert fm["wave"] == 2
        assert fm["depends_on"] == ["330-01"]
        assert fm["files_modified"] == ["src/a.ts", "src/b.ts"]
        assert fm["phase"] == "330-pathway-parity"
        assert fm["must_haves"] == []

    def test_block_list_files(self):
        text = """---
wave: 1
files_modified:
  - gateway/server.py
  - gateway/startup.py
---
"""
        assert parse_frontmatter(text)["files_modified"] == ["gateway/server.py", "gateway/startup.py"]

    def test_empty_inline_list(self):
        assert parse_frontmatter("---\nfiles_modified: []\n---\n")["files_modified"] == []

    def test_no_frontmatter(self):
        assert parse_frontmatter("# Plan\nno frontmatter") == {}

    def test_unterminated_frontmatter(self):
        assert parse_frontmatter("---\nwave: 1\n") == {}


class TestGroupByDeclaredWaves:
    def test_honors_declared_waves(self):
        plans = [
            {"id": "a", "wave": 1, "files_modified": ["x.ts"]},
            {"id": "b", "wave": 2, "files_modified": ["y.ts"]},
            {"id": "c", "wave": 1, "files_modified": ["z.ts"]},
        ]
        waves = group_by_declared_waves(plans)
        assert [[p["id"] for p in w] for w in waves] == [["a", "c"], ["b"]]

    def test_overlap_inside_a_wave_splits(self):
        plans = [
            {"id": "a", "wave": 1, "files_modified": ["shared.ts"]},
            {"id": "b", "wave": 1, "files_modified": ["shared.ts"]},
        ]
        waves = group_by_declared_waves(plans)
        assert len(waves) == 2

    def test_missing_wave_returns_none(self):
        plans = [{"id": "a", "wave": 1}, {"id": "b"}]
        assert group_by_declared_waves(plans) is None

    def test_empty(self):
        assert group_by_declared_waves([]) is None


class TestParsePlanningDir:
    def _plan(self, wave, files, dep=None):
        dep_block = f"depends_on:\n  - \"{dep}\"\n" if dep else ""
        files_inline = ", ".join(files)
        return f"---\nwave: {wave}\n{dep_block}files_modified: [{files_inline}]\n---\n# Plan\n"

    def test_decimal_phase_dirs_and_declared_waves(self, tmp_path):
        planning = tmp_path / ".planning"
        (planning / "phases" / "91.1-closure").mkdir(parents=True)
        (planning / "phases" / "92-next").mkdir(parents=True)
        (planning / "ROADMAP.md").write_text("## Phase 91.1: Closure\n## Phase 92: Next\n")
        p911 = planning / "phases" / "91.1-closure"
        (p911 / "91.1-01-PLAN.md").write_text(self._plan(1, ["a.ts"]))
        (p911 / "91.1-02-PLAN.md").write_text(self._plan(1, ["b.ts"]))
        (p911 / "91.1-03-PLAN.md").write_text(self._plan(2, ["a.ts", "b.ts"], dep="91.1-01"))
        (planning / "phases" / "92-next" / "92-01-PLAN.md").write_text(self._plan(1, ["c.ts"]))

        roadmap = parse_planning_dir(str(planning))
        ids = [p["id"] for p in roadmap["phases"]]
        assert ids == ["phase-91.1", "phase-92"]
        p1 = roadmap["phases"][0]
        assert p1["title"] == "Closure"
        assert [[t["id"] for t in w] for w in p1["waves"]] == [
            ["phase-91.1-01", "phase-91.1-02"], ["phase-91.1-03"],
        ]
        assert p1["waves"][1][0]["depends_on"] == ["91.1-01"]
        assert p1["waves"][1][0]["cmd"] == ""
        assert p1["waves"][1][0]["image"] == "us-central1-docker.pkg.dev/claude-mcp-457317/envision/claude-executor:20260903"
        # No verification source in PLAN.md -> honest no-gate, not a fake passing placeholder.
        assert p1["verification"] == {"cmd": None, "required": False}

    def test_skips_phases_with_summary(self, tmp_path):
        planning = tmp_path / ".planning"
        done = planning / "phase-1-done"
        done.mkdir(parents=True)
        (planning / "ROADMAP.md").write_text("## Phase 1: Done\n")
        (done / "01-01-PLAN.md").write_text(self._plan(1, ["a.ts"]))
        (done / "SUMMARY.md").write_text("done")
        assert parse_planning_dir(str(planning))["phases"] == []


class TestWaveTaskBuilding:
    def _roadmap(self):
        return {
            "roadmap_id": "rm",
            "phases": [
                {"id": "phase-41", "title": "A", "waves": [
                    [{"id": "phase-41-01", "image": "x"}, {"id": "phase-41-02", "image": "x"}],
                    [{"id": "phase-41-03", "image": "x", "depends_on": ["41-01", "41-02"]}],
                ]},
                {"id": "phase-42", "title": "B", "waves": [
                    [{"id": "phase-42-01", "image": "x", "depends_on": ["phase-41-03"]}],
                ]},
            ],
        }

    def test_cross_wave_deps_become_branch_merges(self):
        rm = self._roadmap(); state = create_roadmap_state(rm, "gs://b")
        lookup = build_branch_lookup(rm, state)
        tasks = build_wave_tasks(rm["phases"][0]["waves"][1], lookup, (0, 1))
        assert "depends_on" not in tasks[0]
        assert tasks[0]["inputs"]["merge_branches"] == [
            "gke-dispatch/rm-phase-41-w0/phase-41-01",
            "gke-dispatch/rm-phase-41-w0/phase-41-02",
        ]
        tasks2 = build_wave_tasks(rm["phases"][1]["waves"][0], lookup, (1, 0))
        assert tasks2[0]["inputs"]["merge_branches"] == ["gke-dispatch/rm-phase-41-w1/phase-41-03"]

    def test_same_wave_dep_stays_a_dependency(self):
        wave = [{"id": "a", "image": "x"}, {"id": "b", "image": "x", "depends_on": ["a"]}]
        tasks = build_wave_tasks(wave, {}, (0, 0))
        assert tasks[1]["depends_on"] == ["a"]
        assert "merge_branches" not in tasks[1]["inputs"]

    def test_forward_or_unknown_dependency_rejected(self):
        rm = self._roadmap(); state = create_roadmap_state(rm, "gs://b")
        lookup = build_branch_lookup(rm, state)
        forward = [{"id": "phase-41-01", "image": "x", "depends_on": ["41-03"]}]
        with pytest.raises(ValueError, match="later wave"):
            build_wave_tasks(forward, lookup, (0, 0))
        with pytest.raises(ValueError, match="unknown task"):
            build_wave_tasks([{"id": "z", "image": "x", "depends_on": ["ghost"]}], lookup, (0, 0))

    def test_nested_inputs_honored_and_limits_pass_through(self):
        # The roadmap-JSON skeleton nests inputs; the old execute_wave read only top-level keys,
        # so a JSON written per the docs ran with REPO_URL="" and a fixed 600 s / 5 USD.
        wave = [{
            "id": "b-01", "image": "us-central1-docker.pkg.dev/claude-mcp-457317/envision/claude-executor:20260903", "timeout_seconds": 3600,
            "retries": 0, "resource_profile": "heavy",
            "inputs": {"repo_url": "https://github.com/o/r.git", "plan_path": "p.md", "max_budget_usd": "20"},
        }]
        t = build_wave_tasks(wave, {}, (0, 0))[0]
        assert t["timeout_seconds"] == 3600 and t["retries"] == 0 and t["resource_profile"] == "heavy"
        assert t["inputs"]["repo_url"] == "https://github.com/o/r.git"
        assert t["inputs"]["plan_path"] == "p.md"
        assert t["inputs"]["max_budget_usd"] == "20"
        assert t["inputs"]["repo_branch"] == "main"

    def test_planning_dir_defaults(self):
        t = build_wave_tasks([{"id": "phase-41-01", "image": "x", "plan_content": "# p", "repo_url": "u"}], {}, (0, 0))[0]
        assert t["timeout_seconds"] == 1800
        assert t["inputs"]["max_budget_usd"] == "15"
        assert t["inputs"]["plan_content"] == "# p"
