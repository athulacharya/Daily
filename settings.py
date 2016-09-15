import pytz

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-daily.json
SCOPES = ['https://www.googleapis.com/auth/gmail.compose',
        'https://www.googleapis.com/auth/gmail.modify',
        'https://www.googleapis.com/auth/gmail.readonly']

# Where the client secret for API access is stored
CLIENT_SECRET_FILE = 'client_secret.json'

# Sending email address. Must be a gmail account; may be different
# from the account for API access. May be a valid send-as alias
# of the account.
SENDER = 'sender@gmail.com'

# Person who's doing the journalling. AFAIK this can actually be the same
# as the sending account, but I haven't tested it.
RECEIVER = 'recipient@anywhere.com'

# Where is localtime for the receiver?
LOCALTIME = pytz.timezone('US/Pacific')
