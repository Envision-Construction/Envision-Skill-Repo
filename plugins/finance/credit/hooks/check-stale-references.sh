#!/usr/bin/env bash
# SessionStart hook: warn when any root references/*.md has a next_review date in the past.
# Command-type: Claude Code rejects prompt-type hooks on SessionStart (no conversation context).
cd "${CLAUDE_PLUGIN_ROOT:-$(dirname "$0")/..}" || exit 0
today=${TODAY:-$(date +%Y-%m-%d)}
epoch() { date -j -f %Y-%m-%d "$1" +%s 2>/dev/null || date -d "$1" +%s; }
stale=""
for f in references/*.md; do
  d=$(sed -n 's/^next_review: *"\{0,1\}\([0-9-]*\).*/\1/p' "$f" | head -1)
  [ -n "$d" ] && [[ "$d" < "$today" ]] || continue
  stale+="  - ${f#references/}: next_review was $d ($(( ($(epoch "$today") - $(epoch "$d")) / 86400 )) days overdue)"$'\n'
done
[ -n "$stale" ] && printf 'Stale reference data detected:\n%sVerify these references against current market conditions before citing.\n' "$stale"
exit 0
