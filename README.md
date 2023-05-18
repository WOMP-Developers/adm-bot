# EVE ADM Bot

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/agelito/adm-bot/ci-cd.yml)](https://github.com/agelito/adm-bot/actions/workflows/ci-cd.yml)
[![PyPI](https://img.shields.io/pypi/v/pydisadm)](https://pypi.org/project/pydisadm/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pydisadm)](https://pypi.org/project/pydisadm/)
[![codecov](https://codecov.io/gh/agelito/adm-bot/branch/main/graph/badge.svg?token=OHRY3OW18Y)](https://codecov.io/gh/agelito/adm-bot)

This is a discord bot which will collect alliance system ADM's daily and provide commands to display them in a convenient tier list.

## ⚡ Quick Start

### From PyPI
```shell
# 1. Set up environment
export DISCORD_TOKEN=your-token-here
export DISCORD_CHANNEL=your-channel-here
export DISCORD_APP_ID=your-app-id-here
export ALLIANCE_ID=your-alliance-id-here

# 2. Install package from PyPI
pip install pydisadm

# 3. Run Bot
python -m pydisadm
```

### From source
```shell
# 1. Clone repository
git clone https://github.com/agelito/adm-bot
cd adm-bot

# 2. Copy and edit .env
cp .env.example .env

# 3. Install dependencies
poetry install

# 4. Run bot
poetry run python pydisadm/__main__.py
```

## 📃 Commands

- `/adm summary` - send a summary of ADM's
- `/adm csv` - send a csv of ADM's
- `/adm history <name>` - send a graph showing system, constellation, or region ADM over time
- `/adm refresh` - manually refresh the data
- `/adm update <system>` - manually update ADM for system
- `/adm recommend` - recommend a system to raise ADM in

## 🔧 Configuration
Configuration is done using environment variables or `dotenv`. See `.env.example` for example configuration.

- `DISCORD_TOKEN` - the token bot should use when communicating with discord.
- `DISCORD_CHANNEL` - the channel name bot should listen too, if this is empty the bot will listen to all channels.
- `DISCORD_APP_ID` - the bot application ID
- `ALLIANCE_ID` - the alliance ID for collecting ADM values, only systems owned by this alliance will be collected.
- `DB_KEEP_ADM_DAYS` - how many days adm history should be kept in database (default 7).

## 🔍 Caveats
* The ADM data from ESI is only updated once a day, so refreshing more often than that is not necessary.
* The database will continue to fill up with historic entries, manually inspect size and purge older entries if it's too big.

## 🚧 Development

### Environment
The development environment and dependencies is managed using `poetry`. Use the following command to set up environment and install dependencies:
```shell
poetry install
```

A nested poetry shell can be started using this command:
```shell
poetry shell
```

### Run Linting
```shell
pylint --rcfile pylint.rc pydisadm/**/*.py
```

### Run Unit Tests
```shell
pytest tests/ --cov=pydisadm --cov-branch
```

## 💡 Credits
Project is forked from and inspired by [@anjode](https://www.github.com/anjode)
