# App Ideas Archive

🗂️ A beautiful archive of daily App Store opportunity research, pulled dynamically from the [CryptoSI-DAO/app-ideas](https://github.com/CryptoSI-DAO/app-ideas) repository.

## What This Is

Every day, an automated research agent scans Google Trends, Reddit growth signals, and the App Store to find underserved app opportunities. The top 3 ideas are researched, scored, and documented with full requirements specs — then published to the [app-ideas GitHub repo](https://github.com/CryptoSI-DAO/app-ideas).

This site displays that archive in a mobile-responsive web interface.

## How It Works

The site fetches content **live from the GitHub API** — no backend needed. When the daily research cron adds new ideas to the `app-ideas` repo, they appear here automatically. A GitHub Actions workflow also regenerates `data.json` daily as a fallback.

## Manual Data Refresh

```bash
python3 refresh-data.py
```

## Deployment

Static site — just `index.html`, `data.json`, and `refresh-data.py`. Deploy to GitHub Pages, Vercel, Netlify, or any static host.

## Credits

- **Research:** [Crypto SI](https://t.me/CryptoSI)
- **Agent:** [Hermes Agent](https://github.com/NousResearch/hermes-agent) with Owl Alpha
- **Source data:** [CryptoSI-DAO/app-ideas](https://github.com/CryptoSI-DAO/app-ideas)
