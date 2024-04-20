# FinBot
FinBot is a GroupMe bot that has various financial related commands.

## GroupMe Set Up

1. Go to https://dev.groupme.com/ and login with your GroupMe credentials.

2. Once logged in, click on "Access Token" in the top right next to your name. The bold string of letters and numbers are what you are going to copy into the groupme_access_token field of the config.py. 

3. Click on "Bots" in the top navigation bar. Click on "Create Bot". From the dropdown menu, select the groupchat you want to add the bot to. The next field is the bot name. This can be whatever you want, but it must match what you have in the botname field of the config. The next field is callback URL and must also match what is in the callback_url field of the config. The callback url should be in the form similar to "https://mydomain.com/financialadvisors". The "financialadvisors" part is important, as this is the current route for the Flask app. The Avatar URL is a link to an image if you want your bot to have a profile picture.

4. Once the bot is created, you should be able to get more information on the bot as well as send a test message to your groupchat from the bot. The important information here is the bot Id.

## General Config Set Up
This applications uses pydantic settings, so configuration can be done through environment variables or through `.env` files. There are various bot and 3rd party api fields that allow FinBot to have the commands that it does and run properly. If you don't put all the API keys in and try to run a command that requires it, the bot will probably break and require the web app to be reloaded.

The AlphaVantage and Finnhub API keys are probably the most important right now and are the easiest to acquire.

AlphaVantage: https://www.alphavantage.co/support/#api-key

Finnhub: https://finnhub.io/register

There is also a variable called bot_char. This is the character that commands to the bot must start with for the bot to process it. The default is "?", but you can change this if you wish. 

Here is an example `.env` file. These values can also be set through environment variables.
```
# Bot settings

# Access token from GroupMe
GROUPME_ACCESS_TOKEN = "<token>"  

# Name of the bot as it will appear in the groupchat
BOT_ID = "<bot_id>"
# Character to start messages that will be interpretted by the bot
BOT_CHAR = "?"

# API Keys

# AlphaVantage API key https://www.alphavantage.co/support/#api-key
AV_API_KEY = "<api_key>"
# Finnhub API key https://finnhub.io/register
FINNHUB_API_KEY = "<api_key>"

```

Once the application is running locally, you can navigate to `localhost:5000/docs` to test. Here's an example payload you can use:
```json
{
  "attachments": [],
  "avatar_url": "",
  "created_at": 0,
  "group_id": "",
  "id": "",
  "name": "string",
  "sender_id": "",
  "sender_type": "",
  "source_guid": "",
  "system": false,
  "text": "?help",
  "user_id": ""
}
```



## Current Bot Commands
Can also use "?help".

1. $<ticker> will reply with a live quote of the ticker, example $TSLA
2. ?chart will return a chart of a given ticker
3. ?po will return opimal weights for a given portfolio
4. ?stats will calculate daily historical statistics over a given time range
5. ?mc will run a Monte Carlo simulation based on data of a give time range
6. ?news will return the latest new articles for the market or a specific ticker (default is 3)
7. ?portfolio allows you to interact with the groupchat paper trading account


