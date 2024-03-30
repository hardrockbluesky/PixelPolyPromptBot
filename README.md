# PixelPolyPromptBot
Scheduled prompt bot for lowpoly discord server

Will take in ideas and spit them back out on a weekly schedule, or when requested. Pretty simple.

## Installation:
* Change config.ini.dist to config.ini.
* Add your bot token from the Discord dev site and the channel ID for the channel you're putting the bot in.
* Install pip and discord.py. Feel free to follow [the google cloud discord bot setup guide](https://cloud.google.com/blog/topics/developers-practitioners/build-and-run-discord-bot-top-google-cloud).
* These instructions only apply to the installation of this script, you'll need to also set up the bot through Discord.

## Commands:
* !idea - Give it a prompt idea (!idea pizza) or (!idea "pizza party") if you need a space
* !remove - delete a prompt idea
* !reroll - dispense a new weekly prompt
* !gimme - dispense a random prompt
