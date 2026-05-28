# App Ideas Archive

🗂️ A beautiful archive of daily App Store opportunity research, pulled dynamically from the [CryptoSI-DAO/app-ideas](https://github.com/CryptoSI-DAO/app-ideas) repository.

## What This Is

Every day, an automated research agent scans Google Trends, Reddit growth signals, and the App Store to find underserved app opportunities. The top 3 ideas are researched, scored, and documented with full requirements specs — then published to the [app-ideas GitHub repo](https://github.com/CryptoSI-DAO/app-ideas).

This site displays that archive in a mobile-responsive web interface.

## Updating the Data

The site loads from `data.json`. To refresh with the latest ideas:

```bash
python3 refresh-data.py
```

This pulls the latest from the GitHub repo and regenerates the JSON. The script can be run on a cron job to keep the site current.

## Deployment

This is a static site — just `index.html`, `data.json`, and optionally `refresh-data.py`. Deploy to:
- GitHub Pages
- Vercel
- Netlify
- Any static host

## Credits

- **Research:** [Crypto SI](https://t.me/CryptoSI)
- **Agent:** [Hermes Agent](https://github.com/NousResearch/hermes-agent) with Owl Alpha
- **Source data:** [CryptoSI-DAO/app-ideas](https://github.com/CryptoSI-DAO/app-ideas)
