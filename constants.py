# The main URL off of which to poll product statuses.
URL = 'https://www.bestbuy.com/site/searchpage.jsp?st=pokemon+tcg'

# ------------ Email Constants. See GET_STARTED.md to learn how to generate. ------------
# The sender's email address.
SENDER = ''
# Password from gmail.
SUPER_SECRET_PASSWORD = ''
# A list of email recipients. Emails will be sent out in BCC fashion.
CHANGE_LISTENERS = []
# A list of admin email addresses to send hourly monitoring emails to.
ADMINS = []

# ------------ Main Logic Constants ------------
# The amount of time to wait between loop iterations. A random value is chosen between FREQUENCY_LOW and FREQUENCY_HIGH
# and that's how long we wait in seconds.
FREQUENCY_LOW = 10
FREQUENCY_HIGH = 20

# Wait time if main loop crashes. Currently set to 2 minutes.
WAIT_TIME = 2 * 60

# If a product contains any of these substrings, ignore that product!
IGNORE_LIST_SUBSTRINGS = [
    'collector chest',
    'poke ball tin',
    'first partner pack',
    'first partner collector',
    'battle decks',
    'battle academy box set',
    'vmax battle box',
    'theme deck',
]

# ------------ Monitoring Constants ------------
ACTIVATE_HOURLY_MONITORING = True
HISTORY_MAX_SIZE = 1000

# ------------ Test Constants ------------
TEST = []
TEST_RUN_LIMIT = 1
