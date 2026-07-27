# Gold Intelligence System

An automated system to track gold prices, analyze trends, generate recommendations,
and deliver insights via dashboard and Telegram notifications.

## Features
- Fetches live/historical gold price data via API
- Logs data to Google Sheets
- Performs trend/analytics calculations
- Generates buy/sell/hold recommendations
- Publishes a dashboard
- Sends alerts via Telegram bot
- Runs daily via GitHub Actions

## Project Structure
```
gold-intelligence-system/
├── README.md
├── requirements.txt
├── main.py
├── config.py
├── modules/
│   ├── __init__.py
│   ├── api.py
│   ├── sheets.py
│   ├── analytics.py
│   ├── recommendation.py
│   ├── dashboard.py
│   ├── telegram_bot.py
│   ├── logger.py
│   └── utils.py
├── tests/
│   └── test_api.py
└── .github/
    └── workflows/
        └── daily.yml
```

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/amb09201/gold-intelligence-system.git
   cd gold-intelligence-system
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables (see `config.py`):
   - `GOLD_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `GOOGLE_SHEETS_CREDENTIALS_JSON`
   - `SPREADSHEET_ID`

4. Run locally:
   ```bash
   python main.py
   ```

## Running on Google Colab

You can also run/test this project directly from Google Colab:

```python
!git clone https://github.com/amb09201/gold-intelligence-system.git
%cd gold-intelligence-system
!pip install -r requirements.txt
!python main.py
```

## Automation

This repo includes a GitHub Actions workflow (`.github/workflows/daily.yml`) that
runs `main.py` on a daily schedule automatically.

## License
MIT
