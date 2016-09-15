# Daily
A gmail-based journalling service.

## Overview
Daily will send you emails asking you to write a journal. You write a journal entry by replying to the email. As you accumulate a history of journal entries, it will remind you of what you wrote a month ago and on the same date in previous years.

## Installation
NOTE: This project is very much in an alpha stage! And it will likely stay that way. 

1. Clone the repo.
2. Modify the variables in settings.py.
3. Set up the GMail API as described [here](https://developers.google.com/gmail/api/quickstart/python) and save client_secrets.json to the Daily working directory.
4. Run daily.py once to authorize Daily to send and read emails in the sending gmail account.
5. Add daily.py to your crontab. You may want to set the HOME variable appropriately. E.g.:
  * ```30 22 * * * user HOME=/home/user /home/user/daily/daily.py >> /home/user/daily/log 2>&1```
  * This will run the script at 10:30 PM every day.


## Dependencies
(All of these can be installed with pip.)
* google-api-python-client
* httplib2
* oauth2client
* SQLAlchemy (with a SQLite backend)
* pytz
