# ss-rando-bot

[![Discord](https://img.shields.io/discord/767090759773323264?label=Discord&logo=discord&style=plastic)](https://discord.ssrando.com)

A [racetime.gg](https://racetime.gg) chat bot application for automatically 
generating [SS Randomizer](https://github.com/lepelog/sslib) seeds in race rooms, based on wooferzfg's [TWW Rando Bot](https://github.com/wooferzfg/tww-rando-bot)

## How to get started

### Requirements

* Docker

### Installation

1. Clone the repo
2. Build the Docker image with `docker-compose build`

### Usage

1. Set up environment variables:
```
export GITHUB_TOKEN=... # a GitHub personal access token with permission to create Gists
export CATEGORY_SLUG=... # the slug of the racetime.gg category the bot should operate in (e.g. `twwr`)
export CLIENT_ID=... # the OAuth2 client ID for this bot on racetime.gg
export CLIENT_SECRET=... # the OAuth2 client secret for this bot on racetime.gg
```
2. Run `docker-compose up` to start the bot.


### Commands

This list is not comprehensive, for a full list check the handler.py file.

- *!rollseed*: Rolls a seed with the current settings. If no settings specified defaults to standard settings. If you want to roll another seed, you have to use *!reset* first

- *!permalink*: Sets the permalink for the seed to be rolled

- *!spoiler*: Toggles if a spoiler log should be made publicly available as Github Gist

- *!seed*: Outputs the current seed if one has been rolled already

- *!log*: Gives the link to the spoiler log if enabled before rolling the seed

- *!lock*: Makes seed rolling and elevated commands available only to users with elevated permissions (User who opened the race, Race monitors, category mods/owners)

- *!unlock*: Reverses *!lock* command

- *!reset*: Resets all current settings and the seed

- *!francais*: Translates the bot's messages to French (currently no French translation available)

### Draft Commands
- *!draft*: Enables draft mode

- *!draftoff*: Disables draft mode

- *!draftstatus*: Shows the current status of the draft

- *!draftoptions*: Displays the list of valid options recognized by the draft system

- *!ban*: Registers a preset as banned

- *!pick*: Registers a preset as picked

- *!draftlog*: Turns spoiler log generation in the permalink on if 'on' is the argument, or off if 'off' is the argument (defaults to on).

- *!draftguide*: Given two one-word player names, enables draft guide mode, assuming the first player name is higher seed and the second is lower seed, and guides players through the draft process. This also resets the ban/pick list of the draft.

- *!draftguideoff*: Disables draft guide mode.

### Draft Presets 
- *3D Standard*: ``oQ0AIDADo5oJUgAAAAAAAAAYFA==``

- *3D EUD Off*: ``oQUAIDADo5oJUgAAAAAAAAAcGA==``

- *2D Cubes*: ``IQ0AIBADo5oJUgAAAAAAAAAYEA==``

- *3D Keysanity*: ``oQ0AIDADo5oJmgAAAAAAAAAYFA==``

- *3D Swordless*: ``gQ0AIDADo5oJUgAAAAAAAAAcFA==``

- *3D Open*: ``pw0AADADo5oJUgAAAAAAAAAYFA==``
