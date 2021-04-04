# FinBot
FinBot is a GroupMe bot that has various financial related commands.

## Set Up
While you can deploy this bot where ever and however, I'm going to be deploying on https://www.pythonanywhere.com/ as it's super easy to set up, use, and it's free.

1. Create an account on pythonanywhere. Once the account is created you should be able to create a new web app. Follow the instructions provided on screen. Choose Flask and Python 3.8+, the rest of the defaults should be fine.

2. Once the app is created you can now clone this repo into the created folder. Open a new Bash console. If you kept all the defaults the same, you should be able to run the following command: "rm -r mysite/* && git clone https://github.com/scaratozzolo/FinBot ./mysite". The terminal should ask for your github username and password. Once this is entered git should finish cloning. Once done you can go into the directory by running: "cd mysite". To check that the clone was successful run: "ls". You should see a list of files/folders that are the same to this repo.

3. The next command that you should run is: "pip3 install -r requirements.txt". This will install all the required packages for the bot to run.

4. Navigating back to the pythonanywhere dashboard, you should see a tab at the top called "Files" that you shoudl click on. This will bring you to the in browser file explorer. On the left are folders and on the right are files in the current directory. Click on "mysite" on the left. You should see all the repo files on the right. Click on the "config.py" which should bring you to the in browser file editor. Here is where you are going to put all the access token/api tokens and other bot configurations. As of right now, if you don't put all the api keys, some of the bot commands won't work and will probably break the bot, requiring a server restart. I'm going to be working on fixing this.

5. Once all the config items are set, you can save the the file using the "Save" button on top. Going back to the dashboard you can click on "Web" at the top. On this page, click "Reload username.pythonanywhere.com". This is the same as a server restart and will reload the web app and therefore the script.

## GroupMe Set Up

1. Go to https://dev.groupme.com/ and login with your GroupMe credentials.

2. Once logged in, click on "Access Token" in the top right next to your name. The bold string of letters and numbers are what you are going to copy into the groupme_access_token field of the config.py. 

3. Click on "Bots" in the top navigation bar. Click on "Create Bot". From the dropdown menu, select the groupchat you want to add the bot to. The next field is the bot name. This can be whatever you want, but it must match what you have in the botname field of the config. The next field is callback URL and must also match what is in the callback_url field of the config. The callback url should be in the form similar to "https://username.pythonanywhere.com/financialadvisors". The "financialadvisors" part is important, as this is the current route for the Flask app. The Avatar URL is a link to an image if you want your bot to have a profile picture.

4. Once the bot is created, you should be able to get more information on the bot as well as send a test message to your groupchat from the bot. The important information here is the Group Id. This ID must go in the group_id field of the config.

5. As soon as you have this information filled in the config, you can save the file, and reload the web app.

## General Config Set Up
The config.py file has various bot and 3rd party api fields that allow FinBot to have the commands that it does and run properly. If you don't put all the API keys in and try to run a command that requires it, the bot will probably break and require the web app to be reloaded.

The AlphaVantage and Finnhub API keys are probably the most important right now and are the easiest to acquire. The Alpaca API keys are also easy, but require you to create a brokerage account with Alpaca. 

AlphaVantage: https://www.alphavantage.co/support/#api-key

Finnhub: https://finnhub.io/register

Alpaca: https://alpaca.markets/


There is also a config field called bot_char. This is the character that commands to the bot must start with for the bot to process it. The default is "?", but you can change this if you wish. 

## Current Bot Commands
Can also use "?help".

1. $<ticker> will reply with a live quote of the ticker, example $TSLA
2. ?chart will return a chart of a given ticker
3. ?po will return opimal weights for a given portfolio
4. ?stats will calculate daily historical statistics over a given time range
5. ?mc will run a Monte Carlo simulation based on data of a give time range
6. ?news will return the latest new articles for the market or a specific ticker (default is 3)
7. ?portfolio allows you to interact with the groupchat paper trading account


