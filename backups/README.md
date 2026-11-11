# Backups

Back up the complete canonical repository, including Markdown, YAML, templates, source register and Git history.

SQLite and vector indexes are rebuildable and may be backed up for convenience, but they are not the source of truth.

Recommended:
- local working copy;
- second copy on a separate physical drive;
- encrypted off-device backup if permitted;
- periodic restore test.

Do not put credentials or secrets in backups.
