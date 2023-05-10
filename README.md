# EVE ADM Bot

This is a discord bot which will collect alliance system ADM's daily and provide commands to display them in a convenient tier list.

## Quick Start

`cp .env.example .env` (edit variables in .env)
`pip install -r requirements.txt`
`python bot.py`

## Commands

- `!adm` - send a summary of ADM's
- `!adm <system>` - send a graph showing system ADM over time
- `!adm refresh` - manually refresh the data

## Caveats
* The ADM data from ESI is only updated once a day, so refreshing more often than that is not necessary.
* The database will continue to fill up with historic entries, manually inspect size and purge older entries if it's too big.
