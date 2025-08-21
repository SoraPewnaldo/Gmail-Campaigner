<!-- Project header -->
<h1 align="center">Free Gmail Campaigner</h1>
<p align="center">
  Personalized Gmail outreach with Python + Gmail API. Send clean, HTML emails from CSV with random template rotation, delays, and optional open tracking.
</p>

<p align="center">
  <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/Python-3.9%2B-blue.svg"></a>
  <a href="https://developers.google.com/gmail/api"><img alt="Gmail API" src="https://img.shields.io/badge/Google-Gmail%20API-red.svg"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/License-MIT-green.svg"></a>
  <a href="https://github.com/SoraPewnaldo/Gmail-Campaigner/actions"><img alt="CI" src="https://img.shields.io/badge/CI-none-lightgrey.svg"></a>
  <a href="https://github.com/SoraPewnaldo/Gmail-Campaigner/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/SoraPewnaldo/Gmail-Campaigner?style=social"></a>
  <a href="https://github.com/SoraPewnaldo/Gmail-Campaigner/issues"><img alt="Issues" src="https://img.shields.io/github/issues/SoraPewnaldo/Gmail-Campaigner"></a>
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
git clone https://github.com/SoraPewnaldo/Gmail-Campaigner.git
cd Gmail-Campaigner
pip install -r requirements.txt
```

2. **Set up Google API Credentials**  
   - Go to [Google Cloud Console](https://console.cloud.google.com/)  
   - Create a new project and enable Gmail API  
   - Download `credentials.json` and place it in the project root  

3. **Prepare your leads**  
   - Put them in `leads.csv` with headers like `first_name,email`  

4. **Write your templates**  
   - Save them in `templates.txt` separated by `---`  

5. **Run the script**  
```bash
python main.py
```

## License
MIT License - see [LICENSE](LICENSE) for details.

## Contributing
PRs are welcome! Open an issue for suggestions or bug reports.

---
Made with ❤️ by [SoraPewnaldo](https://github.com/SoraPewnaldo)
