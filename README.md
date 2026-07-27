# Gold Intelligence System

Automated tracker for Joyalukkas gold/silver rates: fetches live rates,
logs history to Google Sheets, computes a Buy Score recommendation, updates
a live Dashboard tab, and sends a Telegram alert — twice a day via GitHub
Actions (09:00, 12:00, and 14:30 IST).

## Pipeline

```
Joyalukkas GraphQL API
        │
        ▼
Google Sheets (Gold_Rates)
        │
        ▼
Analytics (7/30/90-day averages, trend, volatility)
        │
        ▼
Recommendation (Buy Score + label + reasons)
        │
        ▼
Dashboard tab update
        │
        ▼
Telegram alert
```

## Project Structure

```
gold-intelligence-system/
├── README.md
├── requirements.txt
├── main.py
├── config.py
├── modules/
│   ├── __init__.py
│   ├── api.py            # Joyalukkas GraphQL fetch
│   ├── sheets.py          # Google Sheets read/write
│   ├── analytics.py       # moving averages, trend, volatility
│   ├── recommendation.py  # Buy Score engine
│   ├── dashboard.py       # updates the "Dashboard" tab
│   ├── telegram_bot.py    # Telegram alert formatting + sending
│   └── logger.py
├── tests/
│   └── test_api.py
└── .github/workflows/daily.yml
```

## Google Sheet setup

Your spreadsheet needs a worksheet named `Gold_Rates` with this header row:

```
Timestamp | Date | Time | Gold 14K | Gold 18K | Gold 22K | Gold 24K | Silver | Platinum | Gold 22K Change | Silver Change | Buy Score | Recommendation | Notes
```

A second worksheet named `Dashboard` will be created automatically on first run if it doesn't exist.

## Multi-user alerts (optional)

To send personalized alerts to more than one person, add a worksheet tab
named `Users` with these columns:

```
Name    | ChatID     | BuyTarget | EnableTelegram
Mahesh  | 987654321  | 13000     | TRUE
Friend1 | 123456789  | 12800     | TRUE
```

Each row gets its own Buy Score/recommendation calculated against their own
`BuyTarget`, sent only to their `ChatID`. Every recipient must first message
your bot at least once in Telegram (search its username, click **Start**) —
bots cannot message someone who hasn't messaged them first. To find someone's
chat ID, have them message a bot like **@userinfobot**, which replies
instantly with their numeric ID.

If no `Users` tab exists, the system falls back to the single-user
`CHAT_ID`/`BUY_TARGET` from GitHub Secrets / the `Settings` tab, exactly as
before.

Share the spreadsheet with your service account's email (found in your
downloaded JSON key) with **Editor** access.

## Local setup

1. Clone the repo and install dependencies:
   ```bash
   git clone https://github.com/amb09201/gold-intelligence-system.git
   cd gold-intelligence-system
   pip install -r requirements.txt
   ```

2. Place your Google service account JSON key file in the project root
   (e.g. `service_account.json`), or point `GOOGLE_SERVICE_ACCOUNT_FILE` at it.

3. Create a `.env` file:
   ```
   SPREADSHEET_ID=1OWl5vSFV3Gbr-M6qL5fTvO6igzmb484mYWUvDkzYm3U
   GOOGLE_SERVICE_ACCOUNT_FILE=service_account.json
   BUY_TARGET=13000
   ENABLE_TELEGRAM=True
   BOT_TOKEN=your-telegram-bot-token
   CHAT_ID=your-telegram-chat-id
   ```

4. Run it:
   ```bash
   python main.py
   ```

## GitHub Actions setup (automated runs)

Add these repository secrets under **Settings → Secrets and variables → Actions**:

| Secret | Value |
|---|---|
| `GOOGLE_CREDENTIALS` | The **entire contents** of your service account JSON key file, pasted as-is |
| `SPREADSHEET_ID` | Your Google Sheet ID |
| `BUY_TARGET` | Your target buy price, e.g. `13000` |
| `BOT_TOKEN` | Your Telegram bot token from @BotFather |
| `CHAT_ID` | Your Telegram chat ID |

The workflow (`.github/workflows/daily.yml`) runs automatically at 09:00,
12:00, and 14:30 IST daily, and can also be triggered manually from the **Actions** tab
using **Run workflow**.

## Running tests

```bash
pip install pytest
pytest tests/
```
