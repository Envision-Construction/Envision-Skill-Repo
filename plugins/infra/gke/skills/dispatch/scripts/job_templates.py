#!/usr/bin/env python3
"""K8s Job YAML builders for gke-dispatch.

Two builders, routed by image:
- executor jobs: one Job per task for `claude-executor` images, secrets fetched by an init
  container through Workload Identity, per-task timeout/retries.
- indexed job: a single Indexed Job for generic container tasks. The task image only needs
  `sh`; task id/command are resolved by the cloud-sdk init container into /shared so the
  task container never runs python3 (the 2026-08-18 pilot's false-"completed" trap).

A wave must be homogeneous: all executor tasks, or all generic tasks sharing one image and
one resource_profile. `build_job_yaml` raises ValueError otherwise instead of silently
running every task in tasks[0]'s image.
"""

import base64
import json

from gcs_utils import RESOURCE_PROFILES

EXECUTOR_IMAGE_MARKER = "claude-executor"
GITHUB_APP_ID = "3604031"


def _job_name(wave_id: str, suffix: str = "") -> str:
    name = f"gke-dispatch-{wave_id}"
    if suffix:
        name = f"{name}-{suffix}"
    return name.replace("_", "-").lower()[:63]


def _resources(profile: str) -> dict:
    return RESOURCE_PROFILES.get(profile, RESOURCE_PROFILES["standard"])


def _pending(manifest: dict) -> list[dict]:
    return [t for t in manifest["tasks"] if t["status"] == "pending"]


def _is_executor(task: dict) -> bool:
    return EXECUTOR_IMAGE_MARKER in task.get("image", "")


def _b64(obj) -> str:
    return base64.b64encode(json.dumps(obj).encode()).decode()


def _q(value) -> str:
    """YAML double-quoted scalar via JSON encoding (handles quotes, $, newlines)."""
    return json.dumps(str(value))


def build_executor_job(task: dict, wave_id: str, namespace: str,
                       sa: str, bucket: str) -> str:
    """Single executor Job YAML for one Claude Code plan task."""
    profile = task.get("resource_profile", "standard")
    resources = _resources(profile)
    t_name = _job_name(wave_id, task["id"])
    inputs = task.get("inputs", {})
    retries = task.get("retries", 2)
    timeout = task.get("timeout_seconds", 600)
    is_gpu = "gpu" in resources
    gpu_request = '\n            nvidia.com/gpu: "1"' if is_gpu else ""
    gpu_limit = '\n            nvidia.com/gpu: "1"' if is_gpu else ""
    accelerator = resources.get("accelerator")
    deps = task.get("depends_on") or []
    if deps:
        # Poll each dep's result.json on GCS. Exit 0 only when ALL deps have exit_code 0.
        # Persist each dep's push branch to /shared/dep-branches.txt so the entrypoint can
        # merge prerequisite work before running (DEP_BRANCHES_FILE).
        dep_ids_str = " ".join(deps)
        wait_deps_init = (
            "      - name: wait-deps\n"
            "        image: google/cloud-sdk:slim\n"
            "        command: [\"sh\", \"-c\"]\n"
            "        args:\n"
            "        - |\n"
            "          set -e\n"
            f"          DEPS=\"{dep_ids_str}\"\n"
            "          : > /shared/dep-branches.txt\n"
            "          for dep_id in $DEPS; do\n"
            f"            DEP_RESULT=\"{bucket}/waves/{wave_id}/outputs/$dep_id/result.json\"\n"
            "            echo \"Waiting for dependency: $DEP_RESULT\"\n"
            "            while ! gsutil ls \"$DEP_RESULT\" > /dev/null 2>&1; do sleep 15; done\n"
            "            RJSON=$(gsutil cat \"$DEP_RESULT\")\n"
            "            EC=$(echo \"$RJSON\" | grep -o '\"exit_code\": *[0-9]*' | grep -o '[0-9]*$')\n"
            "            if [ \"$EC\" != \"0\" ]; then\n"
            "              echo \"FATAL: dependency $dep_id failed (exit_code=$EC)\" >&2\n"
            "              exit 1\n"
            "            fi\n"
            f"            BRANCH=\"gke-dispatch/{wave_id}/$dep_id\"\n"
            "            echo \"$BRANCH\" >> /shared/dep-branches.txt\n"
            "            echo \"Dependency satisfied: $dep_id (branch=$BRANCH)\"\n"
            "          done\n"
            "          echo \"Dep branches written to /shared/dep-branches.txt:\"\n"
            "          cat /shared/dep-branches.txt\n"
            "        volumeMounts:\n"
            "        - name: shared\n"
            "          mountPath: /shared\n"
        )
    else:
        wait_deps_init = ""
    if accelerator:
        accelerator_required = (
            "      affinity:\n"
            "        nodeAffinity:\n"
            "          requiredDuringSchedulingIgnoredDuringExecution:\n"
            "            nodeSelectorTerms:\n"
            "            - matchExpressions:\n"
            "              - key: cloud.google.com/gke-accelerator\n"
            "                operator: In\n"
            f"                values: [\"{accelerator}\"]\n"
        )
    else:
        # CPU profiles still pin to spot (nodeSelector below). On envision-compute every spot
        # pool is a GPU pool, so this prefers the dual-L4 pool, then single-L4.
        accelerator_required = (
            "      affinity:\n"
            "        nodeAffinity:\n"
            "          preferredDuringSchedulingIgnoredDuringExecution:\n"
            "          - weight: 100\n"
            "            preference:\n"
            "              matchExpressions:\n"
            "              - key: gpu-type\n"
            "                operator: In\n"
            "                values:\n"
            "                - nvidia-l4-dual\n"
            "          - weight: 50\n"
            "            preference:\n"
            "              matchExpressions:\n"
            "              - key: gpu-type\n"
            "                operator: In\n"
            "                values:\n"
            "                - nvidia-l4\n"
        )

    return f"""apiVersion: batch/v1
kind: Job
metadata:
  name: {t_name}
  namespace: {namespace}
  labels:
    app: gke-dispatch
    wave-id: "{wave_id}"
    task-id: "{task['id']}"
spec:
  backoffLimit: {retries}
  activeDeadlineSeconds: {timeout + 60}
  ttlSecondsAfterFinished: 3600
  template:
    metadata:
      labels:
        app: gke-dispatch
        wave-id: "{wave_id}"
        task-id: "{task['id']}"
    spec:
      serviceAccountName: {sa}
      restartPolicy: OnFailure
      nodeSelector:
        cloud.google.com/gke-spot: "true"
      tolerations:
      - key: cloud.google.com/gke-spot
        operator: Equal
        value: "true"
        effect: NoSchedule
      - key: nvidia.com/gpu
        operator: Exists
        effect: NoSchedule
{accelerator_required.rstrip()}
      volumes:
      - name: secrets
        emptyDir: {{}}
      - name: shared
        emptyDir: {{}}
      initContainers:
{wait_deps_init.rstrip()}
      - name: fetch-secrets
        image: google/cloud-sdk:slim
        command: ["sh", "-c"]
        args:
        - |
          gcloud secrets versions access latest --secret=gsd-claude-oauth-token --project=claude-mcp-457317 > /var/secrets/claude-oauth-token
          gcloud secrets versions access latest --secret=gsd-github-app-private-key --project=claude-mcp-457317 > /var/secrets/github-app-key
        volumeMounts:
        - name: secrets
          mountPath: /var/secrets
      containers:
      - name: executor
        image: {task['image']}
        env:
        - name: WAVE_ID
          value: {_q(wave_id)}
        - name: TASK_ID
          value: {_q(task['id'])}
        - name: GCS_BUCKET
          value: {_q(bucket)}
        - name: REPO_URL
          value: {_q(inputs.get('repo_url', ''))}
        - name: REPO_BRANCH
          value: {_q(inputs.get('repo_branch', 'main'))}
        - name: GIT_SHA
          value: {_q(inputs.get('git_sha', ''))}
        - name: PLAN_PATH
          value: {_q(inputs.get('plan_path', ''))}
        - name: TASK_CMD
          value: {_q(task['cmd'])}
        - name: MAX_BUDGET_USD
          value: {_q(inputs.get('max_budget_usd', '5'))}
        - name: GITHUB_APP_ID
          value: "{GITHUB_APP_ID}"
        - name: GITHUB_APP_KEY_FILE
          value: "/var/secrets/github-app-key"
        - name: DEP_BRANCHES_FILE
          value: "/shared/dep-branches.txt"
        resources:
          requests:
            cpu: "{resources['cpu']}"
            memory: "{resources['memory']}"{gpu_request}
          limits:
            cpu: "{resources['cpu_limit']}"
            memory: "{resources['memory_limit']}"{gpu_limit}
        volumeMounts:
        - name: secrets
          mountPath: /var/secrets
          readOnly: true
        - name: shared
          mountPath: /shared
"""


def build_executor_jobs_yaml(manifest: dict) -> str:
    """Generate per-task Job YAMLs for executor images."""
    tasks = _pending(manifest)
    if not tasks:
        return ""

    wave_id = manifest["wave_id"]
    namespace = manifest["config"].get("namespace", "gke-dispatch")
    sa = manifest["config"].get("service_account", "gke-dispatch-worker")
    bucket = manifest["config"]["bucket"].rstrip("/")

    jobs = [build_executor_job(t, wave_id, namespace, sa, bucket) for t in tasks]
    return "---\n".join(jobs)


def build_indexed_job_yaml(manifest: dict) -> str:
    """Generate a single K8s Indexed Job YAML for generic container tasks.

    The task container needs only `sh`. Task id and command arrive via /shared files written
    by the cloud-sdk init container (which has python3 and base64). /outputs is a subPath of
    the shared emptyDir so artifacts written there are visible to the log-shipper.
    """
    tasks = _pending(manifest)
    if not tasks:
        return ""

    wave_id = manifest["wave_id"]
    namespace = manifest["config"].get("namespace", "gke-dispatch")
    sa = manifest["config"].get("service_account", "gke-dispatch-worker")
    bucket = manifest["config"]["bucket"].rstrip("/")
    parallelism = manifest["config"].get("parallelism_cap") or len(tasks)
    completions = len(tasks)

    profile = tasks[0].get("resource_profile", "standard")
    resources = _resources(profile)
    timeout = max(t.get("timeout_seconds", 600) for t in tasks)
    retries = max(t.get("retries", 2) for t in tasks)

    # base64 keeps quotes/$ in commands out of the shell's way; decoded in the init container.
    task_id_map_b64 = _b64({i: t["id"] for i, t in enumerate(tasks)})
    cmd_map_b64 = _b64({i: t["cmd"] for i, t in enumerate(tasks)})
    image = tasks[0]["image"]
    job_name = _job_name(wave_id)

    gpu_line = '\n            nvidia.com/gpu: "1"' if "gpu" in resources else ""

    # Generic tasks are NOT pinned to spot: default-pool (on-demand, untainted) is the first fit.
    # Tolerations only permit the tainted spot/GPU pools when the request does not fit elsewhere
    # (heavy needs >4 CPU; gpu profiles need an accelerator). Accelerator profiles require it.
    accelerator = resources.get("accelerator")
    if accelerator:
        scheduling = (
            "      affinity:\n"
            "        nodeAffinity:\n"
            "          requiredDuringSchedulingIgnoredDuringExecution:\n"
            "            nodeSelectorTerms:\n"
            "            - matchExpressions:\n"
            "              - key: cloud.google.com/gke-accelerator\n"
            "                operator: In\n"
            f"                values: [\"{accelerator}\"]\n"
        )
    else:
        scheduling = ""
    scheduling += (
        "      tolerations:\n"
        "      - key: cloud.google.com/gke-spot\n"
        "        operator: Equal\n"
        "        value: \"true\"\n"
        "        effect: NoSchedule\n"
        "      - key: nvidia.com/gpu\n"
        "        operator: Exists\n"
        "        effect: NoSchedule\n"
    )

    decode = "base64 -d | python3 -c"
    pick_id = "\"import sys,json,os; print(json.load(sys.stdin)[os.environ['IDX']])\""
    pick_cmd = "\"import sys,json,os; sys.stdout.write(json.load(sys.stdin)[os.environ['IDX']])\""

    return f"""apiVersion: batch/v1
kind: Job
metadata:
  name: {job_name}
  namespace: {namespace}
  labels:
    app: gke-dispatch
    wave-id: "{wave_id}"
spec:
  completions: {completions}
  parallelism: {parallelism}
  completionMode: Indexed
  backoffLimit: {retries}
  activeDeadlineSeconds: {timeout + 60}
  ttlSecondsAfterFinished: 3600
  template:
    metadata:
      labels:
        app: gke-dispatch
        wave-id: "{wave_id}"
    spec:
      serviceAccountName: {sa}
      restartPolicy: OnFailure
{scheduling.rstrip()}
      volumes:
      - name: shared
        emptyDir: {{}}
      initContainers:
      - name: idempotent-check
        image: google/cloud-sdk:slim
        command: ["sh", "-c"]
        args:
        - |
          set -e
          export IDX="$JOB_COMPLETION_INDEX"
          echo '{task_id_map_b64}' | {decode} {pick_id} > /shared/task_id
          echo '{cmd_map_b64}' | {decode} {pick_cmd} > /shared/task_cmd
          TASK_ID=$(cat /shared/task_id)
          RESULT_PATH="{bucket}/waves/{wave_id}/outputs/$TASK_ID/result.json"
          if gsutil ls "$RESULT_PATH" > /dev/null 2>&1; then
            echo "SKIP" > /shared/action
            echo "Task $TASK_ID already completed, skipping"
          else
            echo "RUN" > /shared/action
          fi
        env:
        - name: JOB_COMPLETION_INDEX
          valueFrom:
            fieldRef:
              fieldPath: metadata.annotations['batch.kubernetes.io/job-completion-index']
        volumeMounts:
        - name: shared
          mountPath: /shared
      containers:
      - name: task
        image: {image}
        command: ["sh", "-c"]
        args:
        - |
          ACTION=$(cat /shared/action)
          if [ "$ACTION" = "SKIP" ]; then
            echo "Idempotent skip"
            exit 0
          fi
          TASK_ID=$(cat /shared/task_id)
          TASK_CMD=$(cat /shared/task_cmd)
          if [ -z "$TASK_CMD" ]; then
            echo "FATAL: no task command resolved for index $JOB_COMPLETION_INDEX" >&2
            exit 1
          fi
          mkdir -p /outputs
          echo "Running task $TASK_ID"
          START=$(date +%s)
          eval "$TASK_CMD" > /shared/stdout.log 2> /shared/stderr.log
          EXIT_CODE=$?
          END=$(date +%s)
          DURATION=$((END - START))
          cat > /shared/result.json <<RESULT
          {{
            "exit_code": $EXIT_CODE,
            "task_id": "$TASK_ID",
            "duration_seconds": $DURATION,
            "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
          }}
          RESULT
          exit $EXIT_CODE
        env:
        - name: JOB_COMPLETION_INDEX
          valueFrom:
            fieldRef:
              fieldPath: metadata.annotations['batch.kubernetes.io/job-completion-index']
        - name: WAVE_ID
          value: "{wave_id}"
        - name: GCS_BUCKET
          value: "{bucket}"
        resources:
          requests:
            cpu: "{resources['cpu']}"
            memory: "{resources['memory']}"{gpu_line}
          limits:
            cpu: "{resources['cpu_limit']}"
            memory: "{resources['memory_limit']}"{gpu_line}
        volumeMounts:
        - name: shared
          mountPath: /shared
        - name: shared
          mountPath: /outputs
          subPath: outputs
      - name: log-shipper
        image: google/cloud-sdk:slim
        command: ["sh", "-c"]
        args:
        - |
          while [ ! -f /shared/action ]; do sleep 2; done
          if grep -q SKIP /shared/action; then exit 0; fi
          TASK_ID=$(cat /shared/task_id)
          OUTPUT_BASE="{bucket}/waves/{wave_id}/outputs/$TASK_ID"
          while [ ! -f /shared/result.json ]; do sleep 2; done
          sleep 1
          gsutil cp /shared/stdout.log "$OUTPUT_BASE/stdout.log" 2>/dev/null || true
          gsutil cp /shared/stderr.log "$OUTPUT_BASE/stderr.log" 2>/dev/null || true
          if [ -d /outputs ] && [ "$(ls -A /outputs 2>/dev/null)" ]; then
            gsutil -m cp -r /outputs/* "$OUTPUT_BASE/artifacts/" 2>/dev/null || true
          fi
          gsutil cp /shared/result.json "$OUTPUT_BASE/result.tmp.json"
          gsutil mv "$OUTPUT_BASE/result.tmp.json" "$OUTPUT_BASE/result.json"
        env:
        - name: JOB_COMPLETION_INDEX
          valueFrom:
            fieldRef:
              fieldPath: metadata.annotations['batch.kubernetes.io/job-completion-index']
        volumeMounts:
        - name: shared
          mountPath: /shared
        - name: shared
          mountPath: /outputs
          subPath: outputs
"""


def validate_wave_shape(tasks: list[dict]) -> None:
    """A wave is either all executor tasks, or generic tasks sharing one image + profile."""
    executor = [t for t in tasks if _is_executor(t)]
    generic = [t for t in tasks if not _is_executor(t)]
    if executor and generic:
        raise ValueError(
            f"Mixed wave: {len(executor)} claude-executor task(s) and {len(generic)} generic "
            "task(s). Split them into two waves: executor tasks become per-task Jobs, generic "
            "tasks share one Indexed Job."
        )
    if generic:
        images = sorted({t["image"] for t in generic})
        profiles = sorted({t.get("resource_profile", "standard") for t in generic})
        if len(images) > 1:
            raise ValueError(f"Indexed wave needs one image; got {images}. One wave per image.")
        if len(profiles) > 1:
            raise ValueError(
                f"Indexed wave needs one resource_profile; got {profiles}. One wave per profile."
            )


def build_job_yaml(manifest: dict) -> str:
    """Route to executor or indexed job builder. Raises ValueError on a mixed wave."""
    tasks = _pending(manifest)
    if not tasks:
        return ""
    validate_wave_shape(tasks)
    if _is_executor(tasks[0]):
        return build_executor_jobs_yaml(manifest)
    return build_indexed_job_yaml(manifest)
