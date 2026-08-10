# Deploying siballe

This is the complete guide to running siballe in production on a single Ubuntu
24.04 LTS VPS: first-time server setup, the first deploy, day-to-day updates,
rollback, and housekeeping. Everything here assumes one VPS running the backend,
the database, and serving the frontend — that's enough for this app's current
scale.

## Architecture

```
                 ┌────────────────────────── VPS ──────────────────────────┐
                 │                                                          │
 Browser ──80──▶ │  nginx                                                   │
                 │   ├── /              → static files (Flutter web build)  │
                 │   ├── /api/, /admin/ → proxy ──▶ gunicorn (unix socket)  │
                 │   └── /static/       → Django static files (Whitenoise   │
                 │                         also serves these; nginx just    │
                 │                         alias-serves the same directory) │
                 │                                        │                 │
                 │                                        ▼                 │
                 │                               Postgres (localhost only)  │
                 └──────────────────────────────────────────────────────────┘
```

The Flutter web build and the Django API are served from the **same origin**
(same IP/domain, different paths), so the production build needs no CORS
configuration — CORS only matters in local dev, where Flutter runs on its own
port (`:5000`) against the Django dev server (`:8000`).

There is no domain yet. Everything below uses the bare VPS IP address and plain
HTTP. Once you buy a domain, follow the [Appendix](#appendix-adding-a-domain--https-later)
to add HTTPS — nothing before that point needs to be redone, only extended.

---

## 1. One-time VPS setup

Do this once, on a fresh Ubuntu 24.04 LTS VPS. Replace `<VPS_IP>` throughout
with your actual value. Everything here runs as `root` — see the
[Appendix](#appendix-creating-a-dedicated-sudo-user-later) at the end for
switching to a dedicated sudo user once that starts to matter.

### 1.1 System packages

SSH in as `root` (or whatever the provider gives you initially), then:

```sh
apt update && apt full-upgrade -y
apt install -y git curl ufw fail2ban unattended-upgrades nginx \
    postgresql postgresql-contrib rsync
```

### 1.2 Confirm SSH access as root

Confirm you can log in with your key (no password) **before** continuing —
you're about to disable password auth entirely:

```sh
ssh root@<VPS_IP>
```

(Most providers pre-install your local public key for root when you create
the VPS. If yours didn't, paste your `~/.ssh/id_ed25519.pub` into
`/root/.ssh/authorized_keys` by hand, or use your provider's console/rescue
tools.)

Add a convenience alias to your **local** `~/.ssh/config` — the `justfile`'s
deploy recipes use this host alias:

```
Host siballe-vps
    HostName <VPS_IP>
    User root
```

### 1.3 SSH hardening

Root login stays enabled (it's the only account for now), but key-only — no
password auth at all:

```sh
tee /etc/ssh/sshd_config.d/99-siballe.conf <<'EOF'
PermitRootLogin prohibit-password
PasswordAuthentication no
EOF
systemctl restart ssh
```

### 1.4 Firewall

```sh
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw enable
```

(`443/tcp` gets added later, once HTTPS is set up.)

### 1.5 fail2ban and unattended upgrades

fail2ban's default `sshd` jail is enabled out of the box on Ubuntu's package —
just confirm it's running:

```sh
sudo systemctl status fail2ban
sudo fail2ban-client status sshd
```

Enable automatic security updates:

```sh
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

Choose "Yes" when prompted. This writes
`/etc/apt/apt.conf.d/20auto-upgrades` with periodic unattended-upgrade enabled.

### 1.6 App user and directories

```sh
adduser --system --group --home /home/siballe --shell /usr/sbin/nologin siballe
mkdir -p /opt/siballe/{app,frontend-web,backups}
chown -R siballe:siballe /opt/siballe
```

No group-write dance needed here — logged in as `root`, the deploy recipes
(`git pull`, `rsync`) can write into these directories directly. The
[Appendix](#appendix-creating-a-dedicated-sudo-user-later) covers granting a
non-root user the same access.

### 1.7 Install uv and Python for the app user

```sh
sudo -u siballe -H bash -c 'curl -LsSf https://astral.sh/uv/install.sh | sh'
sudo -u siballe -H bash -c 'cd ~ && ~/.local/bin/uv python install 3.14'
```

`pyproject.toml` requires Python ≥3.14, which Ubuntu 24.04's `apt` doesn't ship
(it has 3.12) — `uv` manages its own Python builds, so this sidesteps needing a
PPA.

### 1.8 GitHub deploy key and clone

Generate a **read-only** deploy key on the VPS so the app user can pull without
using your personal SSH key:

```sh
sudo -u siballe -H ssh-keygen -t ed25519 -f /home/siballe/.ssh/id_ed25519 -N ""
sudo -u siballe -H cat /home/siballe/.ssh/id_ed25519.pub
```

Add that public key at **github.com/koljapluemer/siballe → Settings → Deploy
keys → Add deploy key** (leave "Allow write access" unchecked). Then:

```sh
sudo -u siballe -H git clone git@github.com:koljapluemer/siballe.git /opt/siballe/app
```

### 1.9 Postgres

```sh
sudo -u postgres psql -c "CREATE ROLE siballe WITH LOGIN PASSWORD '<generate-a-strong-password>';"
sudo -u postgres psql -c "CREATE DATABASE siballe OWNER siballe;"
```

No `pg_hba.conf` changes needed — Ubuntu's default config already allows
password auth for local TCP connections (`127.0.0.1`), which is how
`DATABASE_URL=postgres://...@localhost:5432/siballe` connects.

### 1.10 Backups

Symlink the committed backup script and systemd units into place:

```sh
sudo ln -s /opt/siballe/app/deploy/backup-postgres.sh /usr/local/bin/siballe-backup-postgres.sh
sudo ln -s /opt/siballe/app/deploy/backup-postgres.service /etc/systemd/system/backup-postgres.service
sudo ln -s /opt/siballe/app/deploy/backup-postgres.timer /etc/systemd/system/backup-postgres.timer
sudo systemctl daemon-reload
sudo systemctl enable --now backup-postgres.timer
```

Confirm it's scheduled: `systemctl list-timers | grep backup-postgres`.

This is everything one-time. From here on you're doing the first deploy.

---

## 2. First deploy

### 2.1 Configure the backend

```sh
sudo -u siballe -H tee /opt/siballe/app/backend/.env <<EOF
DJANGO_SECRET_KEY=$(cd /opt/siballe/app/backend && sudo -u siballe -H /home/siballe/.local/bin/uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=<VPS_IP>
DATABASE_URL=postgres://siballe:<password-from-1.9>@localhost:5432/siballe
DJANGO_CORS_ALLOWED_ORIGINS=
DJANGO_CSRF_TRUSTED_ORIGINS=http://<VPS_IP>
EOF
sudo chmod 600 /opt/siballe/app/backend/.env
sudo chown siballe:siballe /opt/siballe/app/backend/.env
```

(The `EOF` command above needs `DJANGO_SECRET_KEY`'s subshell to actually run
before writing — if copy-pasting fails because of nested `sudo`, just generate
the key first with the same one-liner, copy its output, and paste it into the
file directly.)

### 2.2 Install deps, migrate, collect static, create an admin user

```sh
cd /opt/siballe/app/backend
sudo -u siballe -H /home/siballe/.local/bin/uv sync --frozen
sudo -u siballe -H /home/siballe/.local/bin/uv run manage.py migrate --noinput
sudo -u siballe -H /home/siballe/.local/bin/uv run manage.py collectstatic --noinput
sudo -u siballe -H /home/siballe/.local/bin/uv run manage.py createsuperuser
```

### 2.3 Start gunicorn

```sh
sudo ln -s /opt/siballe/app/deploy/gunicorn.service /etc/systemd/system/gunicorn-siballe.service
sudo systemctl daemon-reload
sudo systemctl enable --now gunicorn-siballe
sudo systemctl status gunicorn-siballe
```

`deploy/gunicorn.service` hardcodes `--workers 3` (the `2 * cores + 1` formula
for a 1-core VPS). If your VPS has more cores, run `nproc` and edit
`deploy/gunicorn.service` in the repo to match, then re-deploy.

### 2.4 Configure nginx

```sh
sudo ln -s /opt/siballe/app/deploy/nginx.conf /etc/nginx/sites-available/siballe
sudo ln -s /etc/nginx/sites-available/siballe /etc/nginx/sites-enabled/siballe
sudo rm -f /etc/nginx/sites-enabled/default
```

Edit `/opt/siballe/app/deploy/nginx.conf` (the real file, since it's the repo's
copy) and replace `YOUR_VPS_IP` with the actual IP, then:

```sh
sudo nginx -t && sudo systemctl reload nginx
```

Commit that IP substitution back in the repo so `deploy/nginx.conf` stays the
source of truth (see the note at the top of that file).

### 2.5 Build and ship the frontend

From your **local machine** (not the VPS — the Flutter SDK is intentionally
never installed on the VPS):

```sh
just build-frontend-prod http://<VPS_IP>/api
just sync-frontend-prod siballe-vps
```

### 2.6 Smoke test

```sh
curl http://<VPS_IP>/api/languages/
```

Then open `http://<VPS_IP>/` in a browser (the app should load) and
`http://<VPS_IP>/admin/` (log in with the superuser from 2.2).

---

## 3. Day-to-day updates

Once everything above is done, shipping a new version is one command from your
local machine:

```sh
just deploy siballe-vps http://<VPS_IP>/api
```

This runs, in order: `deploy-backend` (SSH in, `git pull`, `uv sync --frozen`,
migrate, collectstatic, restart gunicorn), then `build-frontend-prod` (local
Flutter web build), then `sync-frontend-prod` (rsync the build to the VPS).

**Before building for prod**, check your local Flutter matches the version this
project expects, so you're not shipping a build made with a different Flutter
than the one the app was developed against:

```sh
flutter --version   # compare the revision hash to frontend/.metadata
```

If a deploy adds new nginx/gunicorn/backup config (i.e. you edited something
under `deploy/`), `git pull` alone isn't enough — also run on the VPS:

```sh
sudo nginx -t && sudo systemctl reload nginx      # if nginx.conf changed
sudo systemctl daemon-reload && sudo systemctl restart gunicorn-siballe   # if gunicorn.service changed
```

## 4. Rollback

Find the commit you want to roll back to, then on the VPS:

```sh
cd /opt/siballe/app
sudo -u siballe -H git log --oneline -10
sudo -u siballe -H git reset --hard <sha>
cd backend
sudo -u siballe -H /home/siballe/.local/bin/uv sync --frozen
sudo -u siballe -H /home/siballe/.local/bin/uv run manage.py migrate --noinput
sudo -u siballe -H /home/siballe/.local/bin/uv run manage.py collectstatic --noinput
sudo systemctl restart gunicorn-siballe
```

For the frontend, check out the same older commit locally, then re-run
`just build-frontend-prod` / `just sync-frontend-prod` from that checkout.

Rolling back past a migration that isn't reversible needs manual thought —
Django doesn't auto-generate down-migrations; check the migration file before
rolling back across one.

---

## 5. Housekeeping

**Logs**

```sh
journalctl -u gunicorn-siballe -f      # app logs, live
journalctl -u gunicorn-siballe -n 200  # last 200 lines
sudo tail -f /var/log/nginx/access.log /var/log/nginx/error.log
```

nginx's logs are already rotated by Ubuntu's default `/etc/logrotate.d/nginx` —
nothing to add.

**Disk usage**

```sh
df -h
du -sh /opt/siballe/backups/*
journalctl --disk-usage
journalctl --vacuum-time=30d   # if the journal is taking too much space
```

**OS updates**

Security patches install automatically via unattended-upgrades. To check for
and apply everything manually:

```sh
sudo apt update && sudo apt list --upgradable
sudo apt full-upgrade -y
```

Reboot after a kernel update (`sudo systemctl reboot`) — gunicorn, nginx, and
Postgres are all `enable`d systemd services and come back up on their own.

**Restore from a backup**

```sh
sudo systemctl stop gunicorn-siballe
gunzip -c /opt/siballe/backups/siballe_<timestamp>.sql.gz | sudo -u postgres psql siballe
sudo systemctl start gunicorn-siballe
```

Stopping gunicorn first avoids writes racing the restore.

**Verify backups are actually running**

```sh
systemctl list-timers | grep backup-postgres
ls -la /opt/siballe/backups
```

**Rotate the Django secret key**

```sh
cd /opt/siballe/app/backend
sudo -u siballe -H /home/siballe/.local/bin/uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Put the new value in `.env` (`DJANGO_SECRET_KEY=...`), then
`sudo systemctl restart gunicorn-siballe`. This invalidates any existing
sessions/signed cookies — fine at this stage since there's no persistent
end-user login yet.

**Rotate the database password**

```sh
sudo -u postgres psql -c "ALTER ROLE siballe WITH PASSWORD '<new-password>';"
```

Update `DATABASE_URL` in `.env`, then `sudo systemctl restart gunicorn-siballe`.

---

## Known limitations (by design, at this stage)

- **Every API endpoint is `AllowAny`.** JWT auth machinery
  (`djangorestframework-simplejwt`) is wired up in `config/urls.py`, but no view
  currently requires authentication — the app has no login screen yet. Once
  this is deployed publicly, the entire API (situations, exercise generation,
  content search/add) is reachable by anyone. This is expected for the current
  MVP, not a deploy bug — revisit before this matters (e.g. before user-specific
  data exists).
- **Single box.** Postgres, gunicorn, and nginx all run on the same VPS. Fine
  for this app's current scale; moving the database off-box is a future
  concern, not addressed here.

---

## Appendix: adding a domain + HTTPS later

Do this once you've bought a domain. Nothing before this point needs to change
structurally — the same-origin, path-routed layout maps directly onto a domain.

1. Point the domain's `A` (and `AAAA`, if you have an IPv6 address) record at
   `<VPS_IP>`. Wait for DNS to propagate (`dig example.com`).

2. Install certbot:

   ```sh
   sudo apt install -y certbot python3-certbot-nginx
   ```

3. In the repo, edit `deploy/nginx.conf`: change
   `server_name YOUR_VPS_IP;` to `server_name example.com www.example.com;`.
   Deploy this (`git pull` on the VPS, or just edit the symlinked file directly
   since it points at the repo copy), then `sudo nginx -t && sudo systemctl reload nginx`.

4. Request the certificate:

   ```sh
   sudo certbot --nginx -d example.com -d www.example.com
   ```

   Certbot edits the live nginx config in place to add the `443` server block
   and an HTTP→HTTPS redirect. Since `/etc/nginx/sites-available/siballe` is a
   symlink to the repo's `deploy/nginx.conf`, certbot's edits land in the
   tracked file too — **diff it and commit the result** so the repo stays the
   source of truth:

   ```sh
   cd /opt/siballe/app && git diff deploy/nginx.conf
   ```

5. Update `/opt/siballe/app/backend/.env` on the VPS:

   ```
   DJANGO_ALLOWED_HOSTS=example.com,www.example.com
   DJANGO_CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
   ```

6. In `backend/config/settings.py`, uncomment the three lines added for this
   moment:

   ```python
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   SECURE_SSL_REDIRECT = True
   ```

   Commit and deploy this change.

7. Open the firewall for HTTPS: `sudo ufw allow 443/tcp`.

8. Rebuild and reship the frontend with the new HTTPS base URL:

   ```sh
   just build-frontend-prod https://example.com/api
   just sync-frontend-prod siballe-vps
   ```

9. Confirm auto-renewal is set up (certbot installs its own systemd timer, no
   cron needed):

   ```sh
   systemctl list-timers | grep certbot
   sudo certbot renew --dry-run
   ```

10. Restart gunicorn to pick up the `.env` changes, and reload nginx:

    ```sh
    sudo systemctl restart gunicorn-siballe
    sudo nginx -t && sudo systemctl reload nginx
    ```

---

## Appendix: creating a dedicated sudo user later

Running everything as `root` is fine to get started. Before this matters in
earnest — real traffic, other people touching the box — switch day-to-day
admin and deploys to a dedicated sudo user instead: root logging in over SSH
is a bigger blast radius than it needs to be (a leaked key is instant root,
not "instant sudo user who still needs to escalate"), and there's no audit
trail for who ran what.

### Create the user

On the VPS, as root:

```sh
adduser <devname>
usermod -aG sudo <devname>
```

Copy your local public key into place so you can log in as `<devname>`:

```sh
rsync --rsync-path="sudo -u <devname> rsync" -avz ~/.ssh/authorized_keys \
    <VPS_IP>:/home/<devname>/.ssh/authorized_keys
```

(Or paste your `~/.ssh/id_ed25519.pub` into `/home/<devname>/.ssh/authorized_keys`
by hand.) From your local machine, confirm `ssh <devname>@<VPS_IP>` works and
logs you in with a key (no password) **before** continuing — you're about to
disable root login entirely.

### Lock out root over SSH

This replaces the `PermitRootLogin prohibit-password` set in step 1.3:

```sh
sudo tee /etc/ssh/sshd_config.d/99-siballe.conf <<'EOF'
PermitRootLogin no
PasswordAuthentication no
EOF
sudo systemctl restart ssh
```

### Let the new user deploy without sudo

The deploy recipes (`just deploy`, `sync-frontend-prod`) write directly into
`/opt/siballe/app` and `/opt/siballe/frontend-web`, both owned by `siballe`.
Give `<devname>` group access to both — not just `frontend-web`, since
`deploy-backend` also needs to `git pull` into `app`:

```sh
sudo usermod -aG siballe <devname>
sudo chmod -R g+w /opt/siballe/app /opt/siballe/frontend-web
```

Log out and back in (or run `newgrp siballe`) for the group change to apply
to your shell.

### Update your local SSH config

```
Host siballe-vps
    HostName <VPS_IP>
    User <devname>
```

Everything else in this guide is unchanged — the commands from Section 2
onward already use `sudo` for root-only actions (systemctl, nginx, ufw) and
`sudo -u siballe` for app-user actions, which work identically whether you're
logged in as `root` or as `<devname>`.
