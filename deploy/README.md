# deploy/

These files are the source of truth for the VPS's nginx, gunicorn, and backup
configuration. They're symlinked into place on the server (`/etc/nginx/...`,
`/etc/systemd/system/...`) rather than hand-edited only there, so a `git pull`
plus a reload/restart is enough to pick up config changes. Never edit the
live files on the server directly — edit here, commit, then redeploy.

See `DEPLOY.md` at the repo root for full setup and operations instructions.
