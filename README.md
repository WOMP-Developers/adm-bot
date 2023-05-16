# EVE ADM Bot

This is a discord bot which will collect alliance system ADM's daily and provide commands to display them in a convenient tier list.

## ⚡ Quick Start

### Using poetry
```shell
# Edit variables in .env
cp .env.example .env

poetry install
poetry run python pydisadm/__main__.py
```

### Using pip / venv

```shell
# Edit variables in .env
cp .env.example .env

# Create virtual environment
python -m venv .venv

# Install dependencies
pip install -r requirements.txt

# Run bot
python pydidadm/__main__.py
```

## 📃 Commands

- `/adm summary` - send a summary of ADM's
- `/adm csv` - send a csv of ADM's
- `/adm history <name>` - send a graph showing system, constellation, or region ADM over time
- `/adm refresh` - manually refresh the data
- `/adm update <system> <adm>` - manually update ADM for system
- `/adm recommend` - recommend a system to raise ADM in

## 🔧 Configuration
Configuration is done using environment variables or `dotenv`. See `.env.example` for example configuration.

- `DISCORD_TOKEN` - the token bot should use when communicating with discord.
- `DISCORD_CHANNEL` - the channel name bot should listen too, if this is empty the bot will listen to all channels.
- `DISCORD_APP_ID` - the bot application ID
- `ALLIANCE_ID` - the alliance ID for collecting ADM values, only systems owned by this alliance will be collected.

## 🔍 Caveats
* The ADM data from ESI is only updated once a day, so refreshing more often than that is not necessary.
* The database will continue to fill up with historic entries, manually inspect size and purge older entries if it's too big.

## 💡 Credits
Project is forked from and inspired by [@anjode](https://www.github.com/anjode)
