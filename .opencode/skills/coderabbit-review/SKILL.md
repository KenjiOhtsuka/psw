---
name: coderabbit-review
description: Review and address CodeRabbitAI pull request review comments — analyze, fix, commit, push, and reply
---

When asked to handle CodeRabbitAI reviews on a PR:

1. **Fetch the PR** — Get the PR number and repo (or URL) from the user. Fetch all inline review comments via `gh api repos/<owner>/<repo>/pulls/<number>/comments --jq '.[] | {id, path, line, body, user: .user.login}'`.

2. **Analyze each comment** — For each unresolved review comment, read the relevant file(s) and determine:
   - ✅ **Reasonable** → implement the fix
   - ❌ **Not reasonable** → explain why in the reply (e.g., already handled, out of scope, pre-production concern)

3. **Read files** — Read the relevant files mentioned in each comment using the Read tool.

4. **Implement fixes** — For each ✅ comment, make minimal, clean edits.

5. **Commit and push** — `git add` changed files, `git commit -m "fix: ..."`, `git push`.

6. **Post replies** — Reply to each review thread using:
   ```bash
   echo '{"body":"Addressed in commit <hash> — <description>","in_reply_to":<comment_id>}' | gh api repos/<owner>/<repo>/pulls/<number>/comments --input -
   ```
   For already-resolved comments: `"Already resolved — <reason>"`  
   For skipped comments: `"Not addressed — <reason>"`

7. **Report** — Summarize which comments were fixed, which were already resolved, and which were skipped (with reasons).
