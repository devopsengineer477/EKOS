# Contributing to EKOS

## Workflow

1. Create a branch for a topic or correction.
2. Choose a document template.
3. Check `knowledge/technologies/github-actions/MASTER-INDEX.md` to avoid duplication.
4. Create a unique ID and complete front matter.
5. Add primary sources and version scope.
6. Write the explanation in your own words.
7. Validate code/commands in a safe environment where possible.
8. Run `python tools/validate_knowledge.py`.
9. Review the quality checklist in `KNOWLEDGE-STANDARD.md`.
10. Commit and merge.

## Suggested commit messages

- `docs(gha): add workflow event reference`
- `docs(gha): document OIDC trust policy troubleshooting`
- `fix(knowledge): correct source and version metadata`
- `test(examples): validate matrix workflow example`

## Review expectations

A reviewer should check correctness, clarity, source quality, version scope, safety, duplication and verification status.

## Do not contribute

- Secrets, credentials, private keys or access tokens.
- Customer data or confidential logs.
- Unlicensed copied documentation.
- Unverified fixes labeled as verified.
- Destructive commands without warnings and safeguards.
