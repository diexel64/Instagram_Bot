# Instagram_Bot

This is a simple bot for liking pictures and following people on instagram according to hashtag lists.

Before using the bot you need to install the following libraries : selenium, pandas, configparser, keyring and pywin32.

First, it is necessary to include your instagram username in the config.ini file.

Optionaly, you can create a new credential in the windows credential manager in order to let the robot get the password in a secure way.

In order to launch selenium you need to insert the path to the webdriver in line 21.

The bot can then be launched for the first time.

Next time the bot is launched, it is necessary to comment line 49 and uncomment lines 50 & 51 in order to keep a .csv record.

When launching the bot it is possible to choose its functionality :
  - 'l' will only like pictures
  - 'f' will only follow people
  - if no parameter is passed then the bot will follow people and like pictures
  
A probability is set in order to make the bot more human, but it can be adjusted. This probability for liking and following is distinct from each other.
