# Autius Slot Watcher

A small browser-automation bot that logs into [Autius](https://gestion.autius.com/) (a class-booking platform), scans several weeks of the calendar for newly opened lesson slots, and posts a Discord notification the moment one appears — so you can grab it before anyone else does.

## Why

Autius doesn't offer availability alerts. Slots for popular time windows open up sporadically and get booked within minutes. This bot polls the calendar on a loop and pushes a Discord message as soon as a slot is detected, turning a "keep refreshing the page" problem into a passive notification.

## How it works

1. Launches an [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver) Chrome session and logs in with the configured account.
2. Sets the calendar view to show all availability and walks forward through the next N weeks.
3. For each week, inspects the calendar's event elements and flags any slot matching the "open" color signature.
4. If open slots are found, sends a Discord webhook message with the count and week label.
5. Refreshes and repeats on an interval, reporting any run-time errors to the same Discord channel.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in your Autius credentials and Discord webhook URL
```

You'll also need a matching Chrome/Chromium binary and `chromedriver` available on the machine running the bot (paths are configurable via `.env`, see below).

## Configuration

All configuration is environment-driven — see [`.env.example`](.env.example) for the full list:

| Variable | Description |
|---|---|
| `AUTIUS_USERNAME` / `AUTIUS_PASSWORD` | Login credentials for your Autius account |
| `AUTIUS_DISCORD_WEBHOOK_URL` | Discord webhook that receives slot-availability notifications |
| `CHROMEDRIVER_PATH` / `CHROMIUM_BINARY_PATH` | Optional overrides if Chrome/chromedriver aren't at the default Raspberry Pi locations |

## Running

```bash
python src/autius_tracker.py
```

This runs the polling loop directly (`AutiusTracker` in [`src/autius_tracker.py`](src/autius_tracker.py) is also importable if you want to drive it from your own scheduler instead).

## Tech stack

Python, Selenium, undetected-chromedriver, Discord webhooks.

## Notes

This project targets a specific booking platform's DOM structure (CSS classes, XPath selectors, calendar layout), so it's inherently coupled to Autius's current frontend and will need selector updates if their UI changes. Built for personal use; shared here as a small, self-contained example of scheduled browser automation + notification delivery.
