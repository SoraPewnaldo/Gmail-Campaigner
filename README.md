<!-- Project header -->
<h1 align="center">Free Gmail Campaigner</h1>
<p align="center">
  Personalized Gmail outreach with Python + Gmail API. Send clean, HTML emails from CSV with random template rotation, delays, and optional open tracking.
</p>

<p align="center">
  <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/Python-3.9%2B-blue.svg"></a>
  <a href="https://developers.google.com/gmail/api"><img alt="Gmail API" src="https://img.shields.io/badge/Google-Gmail%20API-red.svg"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/License-MIT-green.svg"></a>
  <a href="https://github.com/E:\Mailing automation\Github version/actions"><img alt="CI" src="https://img.shields.io/badge/CI-none-lightgrey.svg"></a>
  <a href="https://github.com/E:\Mailing automation\Github version/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/E:\Mailing automation\Github version?style=social"></a>
  <a href="https://github.com/E:\Mailing automation\Github version/issues"><img alt="Issues" src="https://img.shields.io/github/issues/E:\Mailing automation\Github version"></a>
  <img alt="PRs Welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg">
  <img alt="Made with love" src="https://img.shields.io/badge/made%20with-%E2%9D%A4%EF%B8%8F-ff69b4.svg">
</p>

---

# Free Gmail Campaigner

Lightweight Gmail outreach sender using Gmail API + HTML templates.

## Features
- Personalized HTML templates with placeholders like `{{first_name}}`
- Random template rotation via `---` separators in `templates.txt`
- Optional open tracking + unsubscribe via Google Apps Script
- CSV-based lead import

## Quick Start
1. **Clone repo** and install deps:
   ```bash
   pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib python-dateutil
   ```
2. **Create Google OAuth credentials:**
   - Google Cloud Console → Enable **Gmail API**
   - Create **OAuth Client ID** (Desktop app)
   - Download as **credentials.json** and place next to `main.py` (not tracked by git)
3. **Copy config template** and edit:
   ```bash
   cp config.sample.json config.json
   ```
   - Set `FROM_NAME`, `FROM_EMAIL`
   - Set `WEBAPP_URL` if using tracking (see below)
4. **Prepare data files** (not tracked by git):
   - Create `leads.csv` with headers: `email,first_name,subject`
   - Create `templates.txt` with 1–N HTML templates separated by a line containing `---`
5. **Run a test:**
   ```bash
   python main.py --campaign "Test-001" --limit 3
   ```

## Open Tracking + Unsubscribe (Optional)
1. Open **appsscript.gs** in Google Apps Script.
2. Deploy as **Web app** with *Anyone with the link*.
3. Put the **deployment URL** into `config.json` as `WEBAPP_URL` and set `TRACK_OPENS` to `true`.

## Important
- **Do NOT commit** `credentials.json`, `token.pickle`, `config.json`, `leads.csv`, `templates.txt`, or any real data.
- Respect Gmail limits (≈500/day free Gmail, ≈2000/day Workspace).
"# Gmail-Gampaigner" 
"# Gmail-Campaigner" 
