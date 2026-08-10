#!/usr/bin/env bash
# Nightly Postgres backup for siballe — committed source of truth, symlinked
# to /usr/local/bin/siballe-backup-postgres.sh on the VPS and run by
# backup-postgres.timer. See DEPLOY.md.
set -euo pipefail

BACKUP_DIR=/opt/siballe/backups
STAMP=$(date +%F_%H%M%S)

mkdir -p "$BACKUP_DIR"
sudo -u postgres pg_dump siballe | gzip > "$BACKUP_DIR/siballe_$STAMP.sql.gz"

# Keep the last 14 days of local backups.
find "$BACKUP_DIR" -name 'siballe_*.sql.gz' -mtime +14 -delete
