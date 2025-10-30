# Autopilot Knowledge Engine (A.K.E.)

A 100% automated, free‑tier, static‑site content engine that:
- Pulls public/CC‑BY‑SA feeds (e.g., Wikipedia Featured content API).
- Auto‑generates daily posts with proper attribution.
- Commits & deploys to **GitHub Pages** via **GitHub Actions** on a daily cron.
- Inserts compliant “house ads” (your default monetization) until affiliate IDs are added.
- Enforces file‑size checks before committing (no >100MB in Git).

## One‑click (hands‑off) flow
1) Open a terminal and run `./setup.sh` (macOS/Linux) or `windows_setup.bat` (Windows).
2) When your browser opens for GitHub auth, approve. *(I can’t click for you.)*
3) The script will create a repo, push this project, and enable Pages + a daily cron.
4) That’s it — new content will publish every day, automatically.

> Note: YouTube/TikTok uploads are **not** required for this starter; this runs 100% on Pages. You can add optional social exporters later.

## What it builds
- **/site**: GitHub Pages site with daily posts in `/site/posts/` and an index.
- **/.github/workflows/daily.yml**: A cron that runs every morning and publishes.
- **/orchestrator**: Python job that pulls news from CC sources and writes posts.
- **/guardians/Guardian_Setup_Wizard.pdf**: Guardian oversight quick‑guide.

## Safe defaults
- If no affiliate IDs are provided, it uses **/house_ads.json** links in all posts.
- Wikipedia content is used with attribution per CC‑BY‑SA requirements.
- No scraping behind logins. No paid APIs. No deceptive content.

## Local testing
```
python3 -m venv .venv && source .venv/bin/activate
pip install -r orchestrator/requirements.txt
python orchestrator/main.py --once
python orchestrator/build_site.py
```
The site will be updated under `site/`. Commit and push to preview.

— Generated on 2025-10-30
