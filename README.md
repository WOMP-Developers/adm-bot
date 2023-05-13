# EVE ADM Bot

This is a discord bot which will collect alliance system ADM's daily and provide commands to display them in a convenient tier list.

## ⚡ Quick Start

```shell
# Edit variables in .env
cp .env.example .env

# Install dependencies
pip install -r requirements.txt

# Run bot
python bot.py
```

## 📃 Commands

- `!adm` - send a summary of ADM's
- `!adm csv` - send a csv of ADM's
- `!adm <system>` - send a graph showing system ADM over time
- `!adm refresh` - manually refresh the data
- `!adm update <system> <adm>` - manually update ADM for system
- `!adm help` - print help message

## 🔧 Configuration
Configuration is done using environment variables or `dotenv`. See `.env.example` for example configuration.

- `DISCORD_TOKEN` - the token bot should use when communicating with discord.
- `DISCORD_CHANNEL` - the channel name bot should listen too, if this is empty the bot will listen to all channels.
- `ALLIANCE_ID` - the alliance ID for collecting ADM values, only systems owned by this alliance will be collected.

## 🔍 Caveats
* The ADM data from ESI is only updated once a day, so refreshing more often than that is not necessary.
* The database will continue to fill up with historic entries, manually inspect size and purge older entries if it's too big.

## 💡 Credits
Project is forked from and inspired by [@anjode](https://www.github.com/anjode)
