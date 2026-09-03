#!/usr/bin/env bash
set -euo pipefail

# --- Auth ---

if [ -z "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]; then
  if [ -f /var/secrets/claude-oauth-token ]; then
    export CLAUDE_CODE_OAUTH_TOKEN=$(cat /var/secrets/claude-oauth-token)
  else
    echo "FATAL: CLAUDE_CODE_OAUTH_TOKEN not set and /var/secrets/claude-oauth-token not found." >&2
    exit 1
  fi
fi
export CLAUDE_CODE_OAUTH_TOKEN

# --- Git credentials ---

if [ -n "${GITHUB_APP_KEY_FILE:-}" ] && [ -n "${GITHUB_APP_ID:-}" ]; then
  GITHUB_TOKEN=$(python3 /scripts/generate_github_token.py \
    --app-id "$GITHUB_APP_ID" \
    --key-file "$GITHUB_APP_KEY_FILE" \
    --org "${GITHUB_ORG:-Envision-Construction}")
  git config --global url."https://x-access-token:${GITHUB_TOKEN}@github.com/".insteadOf "https://github.com/"
elif [ -n "${GITHUB_TOKEN:-}" ]; then
  git config --global url."https://x-access-token:${GITHUB_TOKEN}@github.com/".insteadOf "https://github.com/"
elif [ -f /var/secrets/github-deploy-key ]; then
  SSH_HOME="${HOME}/.ssh"
  mkdir -p "$SSH_HOME"
  cp /var/secrets/github-deploy-key "$SSH_HOME/id_ed25519"
  chmod 600 "$SSH_HOME/id_ed25519"
  printf "Host github.com\n  IdentityFile %s/id_ed25519\n  StrictHostKeyChecking no\n" "$SSH_HOME" > "$SSH_HOME/config"
fi

# --- Task context ---

WAVE_ID="${WAVE_ID:?WAVE_ID required}"
TASK_ID="${TASK_ID:?TASK_ID required}"
GCS_BUCKET="${GCS_BUCKET:?GCS_BUCKET required}"

INPUT_PATH="${GCS_BUCKET}/waves/${WAVE_ID}/inputs/${TASK_ID}.json"
OUTPUT_BASE="${GCS_BUCKET}/waves/${WAVE_ID}/outputs/${TASK_ID}"

# --- Repo setup ---

REPO_URL="${REPO_URL:-}"
REPO_BRANCH="${REPO_BRANCH:-main}"
GIT_SHA="${GIT_SHA:-}"

if [ -n "$REPO_URL" ]; then
  git clone --branch "$REPO_BRANCH" "$REPO_URL" /workspace/repo
  cd /workspace/repo
  if [ -n "$GIT_SHA" ]; then
    git checkout "$GIT_SHA"
  fi
  # Merge dependency branches (set by wait-deps init container) so this pod sees prerequisite work.
  if [ -n "${DEP_BRANCHES_FILE:-}" ] && [ -s "${DEP_BRANCHES_FILE}" ]; then
    echo "=== Merging ${DEP_BRANCHES_FILE} dep branches ==="
    while IFS= read -r DEP_BRANCH; do
      [ -z "$DEP_BRANCH" ] && continue
      echo "Fetching+merging dep branch: origin/$DEP_BRANCH"
      git fetch origin "$DEP_BRANCH" || { echo "FATAL: could not fetch $DEP_BRANCH" >&2; exit 1; }
      git merge --no-edit "origin/$DEP_BRANCH" || { echo "FATAL: merge conflict against $DEP_BRANCH" >&2; exit 1; }
    done < "${DEP_BRANCHES_FILE}"
    echo "=== Dep merge complete ==="
  fi
else
  cd /workspace
fi

# --- Download task input ---

mkdir -p /workspace/inputs /workspace/outputs

if gsutil ls "$INPUT_PATH" 2>/dev/null; then
  gsutil cp "$INPUT_PATH" /workspace/inputs/task.json || true
fi || true

# --- Resolve task command ---

TASK_CMD="${TASK_CMD:-}"
PLAN_PATH="${PLAN_PATH:-}"
PLAN_CONTENT=""
MAX_BUDGET_USD="${MAX_BUDGET_USD:-5}"

resolve_plan_content() {
  if [ -n "$PLAN_PATH" ] && [ -f "$PLAN_PATH" ]; then
    PLAN_CONTENT=$(cat "$PLAN_PATH")
    return 0
  fi
  if [ -f /workspace/inputs/task.json ]; then
    local content
    content=$(jq -r '.plan_content // empty' /workspace/inputs/task.json)
    if [ -n "$content" ]; then
      PLAN_CONTENT="$content"
      return 0
    fi
    if [ -z "$PLAN_PATH" ]; then
      PLAN_PATH=$(jq -r '.plan_path // empty' /workspace/inputs/task.json)
    fi
    if [ -n "$PLAN_PATH" ] && [ -f "$PLAN_PATH" ]; then
      PLAN_CONTENT=$(cat "$PLAN_PATH")
      return 0
    fi
  fi
  return 1
}

USE_PROMPT_FILE=""
if resolve_plan_content && [ -n "$PLAN_CONTENT" ]; then
  PROMPT_FILE=$(mktemp /tmp/prompt.XXXXXX)
  printf 'Execute this plan precisely. Commit each change atomically. Do not skip any step.\n\n%s' "$PLAN_CONTENT" > "$PROMPT_FILE"
  USE_PROMPT_FILE="$PROMPT_FILE"
elif [ -z "$TASK_CMD" ] && [ -f /workspace/inputs/task.json ]; then
  TASK_CMD=$(jq -r '.cmd // empty' /workspace/inputs/task.json)
fi

if [ -z "$USE_PROMPT_FILE" ] && [ -z "$TASK_CMD" ]; then
  echo "FATAL: No task command resolved. Set TASK_CMD, PLAN_PATH, or provide inputs." >&2
  exit 1
fi

# --- Execute ---

echo "=== GKE Dispatch Executor ==="
echo "Wave: $WAVE_ID | Task: $TASK_ID"
if [ -n "$USE_PROMPT_FILE" ]; then
  echo "Mode: plan-file ($USE_PROMPT_FILE, $(wc -c < "$USE_PROMPT_FILE") bytes, budget USD $MAX_BUDGET_USD)"
else
  echo "Command: ${TASK_CMD:0:200}..."
fi
echo "=== Starting execution ==="

START=$(date +%s)
CLAUDE_RESULT='{}'
set +e
if [ -n "$USE_PROMPT_FILE" ]; then
  # --max-turns no longer exists in the CLI (gone since at least 2.1.181); the budget cap is the bound.
  # --output-format json yields a result envelope: is_error, subtype, total_cost_usd, num_turns, session_id.
  claude -p --dangerously-skip-permissions --output-format json --max-budget-usd "$MAX_BUDGET_USD" < "$USE_PROMPT_FILE" \
    > /workspace/outputs/claude.json 2> /workspace/outputs/stderr.log
  EXIT_CODE=$?
  rm -f "$USE_PROMPT_FILE"
  # Output is one result object, or an array of events whose last type=="result" element is the
  # envelope (both shapes seen in the field). Same jq as dispatch-worker.sh.
  CLAUDE_RESULT=$(jq -c 'if type=="array" then (map(select(.type=="result"))|last) else . end' \
    /workspace/outputs/claude.json 2>/dev/null)
  if [ -z "$CLAUDE_RESULT" ] || [ "$CLAUDE_RESULT" = "null" ]; then CLAUDE_RESULT='{}'; fi
  jq -r '.result // empty' <<<"$CLAUDE_RESULT" > /workspace/outputs/stdout.log 2>/dev/null || true
  IS_ERROR=$(jq -r '.is_error // false' <<<"$CLAUDE_RESULT")
  # A clean exit with is_error=true (budget exhausted, refusal, tool failure) is still a failure.
  if [ "$EXIT_CODE" -eq 0 ] && [ "$IS_ERROR" = "true" ]; then EXIT_CODE=1; fi
else
  eval "$TASK_CMD" > /workspace/outputs/stdout.log 2> /workspace/outputs/stderr.log
  EXIT_CODE=$?
fi
set -e
END=$(date +%s)
DURATION=$((END - START))

# --- Collect results ---

GIT_LOG=""
if [ -d .git ]; then
  GIT_LOG=$(git log --oneline -10 2>/dev/null || echo "")
fi

cat > /workspace/outputs/result.json <<RESULT
{
  "exit_code": $EXIT_CODE,
  "task_id": "$TASK_ID",
  "wave_id": "$WAVE_ID",
  "duration_seconds": $DURATION,
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "git_commits": $(echo "$GIT_LOG" | jq -R -s 'split("\n") | map(select(length > 0))'),
  "repo_branch": "$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '')",
  "head_sha": "$(git rev-parse HEAD 2>/dev/null || echo '')",
  "is_error": $(jq '.is_error // false' <<<"$CLAUDE_RESULT"),
  "claude_subtype": $(jq '.subtype // null' <<<"$CLAUDE_RESULT"),
  "total_cost_usd": $(jq '.total_cost_usd // null' <<<"$CLAUDE_RESULT"),
  "num_turns": $(jq '.num_turns // null' <<<"$CLAUDE_RESULT"),
  "session_id": $(jq '.session_id // null' <<<"$CLAUDE_RESULT")
}
RESULT

# --- Upload to GCS (best-effort: fails gracefully if bucket doesn't exist) ---

if gsutil ls "${GCS_BUCKET}" 2>/dev/null; then
  gsutil cp /workspace/outputs/stdout.log "${OUTPUT_BASE}/stdout.log" || true
  gsutil cp /workspace/outputs/stderr.log "${OUTPUT_BASE}/stderr.log" || true
  gsutil cp /workspace/outputs/result.json "${OUTPUT_BASE}/result.tmp.json" && \
    gsutil mv "${OUTPUT_BASE}/result.tmp.json" "${OUTPUT_BASE}/result.json" || true
  if [ -d /workspace/outputs ] && [ "$(ls -A /workspace/outputs/*.* 2>/dev/null | grep -v stdout.log | grep -v stderr.log | grep -v result.json)" ]; then
    gsutil -m cp -r /workspace/outputs/* "${OUTPUT_BASE}/artifacts/" 2>/dev/null || true
  fi
else
  echo "GCS bucket ${GCS_BUCKET} not accessible: skipping upload" >&2
fi

# --- Push git changes ---

if [ -d .git ] && [ -n "$(git status --porcelain)" ]; then
  echo "Uncommitted changes detected: staging and pushing" >&2
  git add -A
  git commit -m "[gke-dispatch] ${WAVE_ID}/${TASK_ID}: auto-commit remaining changes"
fi

if [ -d .git ] && [ -n "$REPO_URL" ]; then
  PUSH_BRANCH="${PUSH_BRANCH:-gke-dispatch/${WAVE_ID}/${TASK_ID}}"
  git checkout -b "$PUSH_BRANCH" 2>/dev/null || git checkout "$PUSH_BRANCH"
  git push origin "$PUSH_BRANCH" --force-with-lease 2>/dev/null || echo "Push failed (non-fatal)" >&2
fi

echo "=== Task $TASK_ID completed (exit: $EXIT_CODE, ${DURATION}s) ==="
exit $EXIT_CODE
