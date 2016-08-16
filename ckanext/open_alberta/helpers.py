from ckan.plugins import toolkit
from ckan.lib import search
from pylons import config
import feedparser
from dateutil import parser
from datetime import date


def fetch_feed(feed_url, number_of_entries=1):
    feed = feedparser.parse(feed_url)
    feed['entries'] = feed['entries'][:number_of_entries]
    return feed

def is_future_date(adate):
    strdt = str(adate) or '2063-04-05' # a future date in case adate is empty
    try:
        return parser.parse(adate).date() > date.today()
    except ValueError:
        return False
