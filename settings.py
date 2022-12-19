from os import environ

# Testing and debug settings
TEST = environ.get("TEST", "false") == "true"
DEBUG = environ.get("DEBUG", "false") == "true"

USER_AGENT = 'TotesMessenger v0.6 by /u/justcool393 and /u/cmd-t'

# Database file
DB_FILE = environ.get("DATABASE", "totes.sqlite3")

# Posting settings
POST_TIME = 2 * 60  # how long to wait until we should post (2 minutes in secs.)
LINKS_BEFORE_TITLE_CUTOFF = 40
TITLE_LIMIT = 140 - 3  # title character limit - 1 (for ellipsis)

# Speed limits
WAIT = int(environ.get("WAIT", 30))  # how long we wait between cycles
LIMIT = int(environ.get("LIMIT", 25))  # how many posts done per cycle

# Footer links
INFO_LINK = "/r/TotesMessenger"
CONTACT_LINK = "/message/compose?to=/r/TotesMessenger"
TRANSLATION_ERROR_LINK = CONTACT_LINK + "&subject=translation error " \
                                        "({language}\)"

IGNORED_SOURCES = set([""])
IGNORED_LINKS = set([""])
IGNORED_BOTH = set([""])
IGNORED_USERS = set([""])
