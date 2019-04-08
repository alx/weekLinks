from mastodon import Mastodon
import pyperclip
from datetime import datetime, timezone, timedelta
import yaml

config = yaml.safe_load(open("./config.yml"))

mastodon = Mastodon(
    client_id = config['mastodon']['client_id'],
    client_secret = config['mastodon']['client_secret'],
    access_token = config['mastodon']['access_token'],
    api_base_url = config['mastodon']['api_base_url']
)

one_week_ago = datetime.now(timezone.utc) - timedelta(days=8)

account = mastodon.account_search(
    q = config['mastodon']['account_query'],
    limit = 1
)

def get_toots(max_id = None):
    toots = []

    for toot in mastodon.account_statuses(account[0].id, max_id = max_id):
        if toot.created_at > one_week_ago:
            toots.append(toot)
            max_id = toot.id
        else:
            max_id = None

    if(max_id != None):
        toots = toots + get_toots(max_id)

    return toots


toots = get_toots()

content = ''
for toot in toots:
    content += toot.content

pyperclip.copy(content)
