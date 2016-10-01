#!/usr/bin/python

import gmail
from gmail import get_credentials, create_message, send_message, query_msgs, get_message, mark_message_read
from apiclient import discovery
import time
import httplib2
from datetime import datetime
from datetime import timezone
from datetime import timedelta
import pytz
import re
import random
import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import dbentry
from dbentry import Entry

from settings import *


APPLICATION_NAME = 'Daily'
PROMPTS = ['What are you grateful for?',
           'What made you happy today?',
           'What did you get done today?',
           'Did you have a productive day?',
           'What\'s on your mind?',
          ]

def main():
    # sqlite setup
    home_dir = os.path.expanduser('~')
    journal_dir = os.path.join(home_dir, '.journals')
    if not os.path.exists(journal_dir):
        os.makedirs(journal_dir)
    journal_dir = os.path.join('sqlite:///' + journal_dir, 'journal.db')
    engine = create_engine(journal_dir, echo=False)
    dbentry.Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)
    dbsession = DBSession()

    # gmail setup
    credentials = get_credentials(CLIENT_SECRET_FILE, SCOPES, APPLICATION_NAME)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    # compose message body with previous journal entries
    utc_today = datetime.now(timezone.utc)
    local_today = utc_today.astimezone(LOCALTIME)
    body = PROMPTS[random.randint(0,len(PROMPTS)-1)]+'\n\n'
    # get ALL entries on the same day-of-month
    previous = dbsession.query(Entry).filter(sqlalchemy.func.strftime('%d', Entry.timestamp)
                                             .is_(str(utc_today.day))).order_by(Entry.timestamp).all()
    previous.reverse()
    for entry in previous:
        if entry.timestamp.year == utc_today.year and entry.timestamp.month == (utc_today.month-1):
            body += '--------------------\n' + 'Last month, you wrote:\n\n' + str(entry.timestamp) + ':\n' + entry.entry + '\n\n'
        elif utc_today.month == 1 and entry.timestamp.month == 12 and entry.timestamp.year == (utc_today.year-1):
            body += '--------------------\n' + 'Last month, you wrote:\n\n' + str(entry.timestamp) + ':\n' + entry.entry + '\n\n'
        elif entry.timestamp.year < utc_today.year and entry.timestamp.month == utc_today.month:
            years_ago = utc_today.year - entry.timestamp.year
            body += '--------------------\n' + str(years_ago) + ' years ago, you wrote:\n\n' + str(entry.timestamp) + ':\n' + entry.entry + '\n\n'

    message = create_message(SENDER, 
                             RECEIVER,
                             "[{}] Would you like to make a journal entry for {}-{}-{}?"
                                .format(
                                        len(dbsession.query(Entry).all()),
                                        local_today.year,
                                        local_today.month,
                                        local_today.day
                                        ),
                             body);
    sent_msg = send_message(service, "me", message)

    while (datetime.now(timezone.utc) - utc_today) < timedelta(days=1):
        time.sleep(600)

        # search for unread messages from user
        messagelist = query_msgs(service, "me", "from:%s label:UNREAD" % RECEIVER)
        if messagelist == []:
            continue

        for unread in messagelist:
            # if there's one in the same thread as the one we just sent, let's get it
            if unread['threadId'] == sent_msg['threadId']:
                response = get_message(service, "me", unread['id'])
                mark_message_read(service, "me", unread['id'])

                if response.is_multipart():     # usually the case I think
                    for part in response.walk():
                        # looks like messages from gmail are usually multipart: one text/plain and one text/html
                        # usually(?) the plaintext one is the first one
                        if part.get_content_type() == 'text/plain':
                            text = part.get_payload()
                else:
                    text = response.get_payload()

                text = re.sub('^>.*?(\n|\r)', '', text, flags=re.MULTILINE)
                text = re.sub('^On.*?wrote:(\n|\r)', '', text, flags=re.MULTILINE)
                text = re.sub('\s*$', '', text)
                journal_entry = Entry(msgid=unread['id'], timestamp=datetime.now(timezone.utc), entry=text)
                dbsession.add(journal_entry)
                dbsession.commit()
                break       # if we find an unread message in the thread we started, we're done

        if unread['threadId'] == sent_msg['threadId']:
            break           # same

if __name__ == '__main__':
    main()

