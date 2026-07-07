"""Runtime configuration loaded from environment variables (see .env.example)."""

import os

from dotenv import load_dotenv

load_dotenv()

# Autius account credentials
AUTIUS_USERNAME = os.environ["AUTIUS_USERNAME"]
AUTIUS_PASSWORD = os.environ["AUTIUS_PASSWORD"]

# Discord webhook used to announce newly opened lesson slots
AUTIUS_DISCORD_WEBHOOK_URL = os.environ["AUTIUS_DISCORD_WEBHOOK_URL"]

# Browser automation paths (defaults assume a Debian-based Raspberry Pi image)
CHROMEDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH", "/home/pi/chromedriver")
CHROMIUM_BINARY_PATH = os.environ.get("CHROMIUM_BINARY_PATH", "/usr/bin/chromium-browser")
