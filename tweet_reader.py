#  Inspiration for the task taken from # https://code.recuweb.com/2015/scraping-tweets-directly-from-twitter-without-authentication/#twitters-advanced-search-without-being-logged

import json
import re
import threading
from urllib.parse import urlencode
from urllib.parse import quote
import requests
import datetime
import time
import argparse
from tweet_api import run_flask

MINUTES_TO_SECONDS = 60

def get_user_agent():
    """
    Adds a fake user agent to the request in order to avoid twitter blocking the search request
    :return: string (agent details)
    """
    return "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36"


session = requests.Session()
session.headers.update(
    {'User-Agent': get_user_agent(),
     })


def get_auth_token():
    """
    Twitter looks to use the same auth token for all unauthenticated users
    :return: string (bearer token)
    """
    return "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"


def get_guest_token():
    """
    Make a generic call to twitter.com to get a guest token to use for their api
    :return: string (guest token)
    """
    url = 'https://twitter.com'
    req = session.prepare_request(requests.Request('GET', url))
    r = session.send(req, allow_redirects=True, timeout=15)
    gt = re.search(r'\("gt=(\d+);', r.text)
    return gt.group(1)


def request(url):
    """
    Wrapper to send get request with auth headers
    :param url: string (encoded url including all query params)
    :return: requests.Response object
    """
    _headers = {
        'authorization': get_auth_token(),
        'x-guest-token': get_guest_token(),
    }
    with session.get(url, headers=_headers) as response:
        return response


def form_query(user, scheduled):
    """
    Forms a query string to request for user information
    :param user: string (Twitter Username/handle to query)
    :param scheduled: POSIX timestamp as float (lower bound time to query from)
    :return: A url to query for tweets
    """
    query = f"from:{user}"
    if scheduled is not None:
        query += f"since:{int(scheduled)}"

    search_options = [('count', 5 if scheduled is None else 100), ('cursor', -1), ('tweet_search_mode', 'live'),
                      ('include_profile_interstitial_type', '1'), ('include_blocking', '1'),
                      ('include_blocked_by', '1'), ('include_followed_by', '1'), ('include_want_retweets', '1'),
                      ('include_mute_edge', '1'), ('include_can_dm', '1'), ('include_can_media_tag', '1'),
                      ('skip_status', '1'), ('cards_platform', 'Web-12'), ('include_cards', '1'),
                      ('include_ext_alt_text', 'true'), ('include_quote_count', 'true'), ('include_reply_count', '1'),
                      ('tweet_mode', 'extended'), ('include_entities', 'true'), ('include_user_entities', 'true'),
                      ('include_ext_media_color', 'true'), ('include_ext_media_availability', 'true'),
                      ('send_error_codes', 'true'), ('simple_quoted_tweet', 'true'), ('query_source', 'typed_query'),
                      ('pc', '1'), ('spelling_corrections', '1'), ('ext', 'mediaStats%2ChighlightedLabel'),
                      ("q", query)]
    return "https://api.twitter.com/2/search/adaptive.json" + "?" + urlencode(search_options, quote_via=quote)


def read_tweets(json_response):
    """
    processes response from twitter into list of json tweets
    :param json_response: string (json response with tweets)
    :return: Array[JSON] (Tweet objects)
    """

    response = json.loads(json_response)
    feed = []
    for timeline_entry in response['timeline']['instructions'][0]['addEntries']['entries']:
        if timeline_entry['entryId'].startswith('sq-I-t-'):
            if 'tweet' in timeline_entry['content']['item']['content']:
                _id = timeline_entry['content']['item']['content']['tweet']['id']
                feed.append(response['globalObjects']['tweets'][_id])
    return feed


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Read a users tweets')
    parser.add_argument("-u", "--username", help="Username of persons tweets to collect", required=True)
    parser.add_argument("-f", "--frequency", type=int, help="polling frequency in minutes", default=10)
    args = parser.parse_args()

    threading.Thread(target=run_flask).start()  # Init flask to serve rest api queries in a new thread

    scheduled_time = None
    while True:
        pre_execution_timestamp = datetime.datetime.now().timestamp()
        url = form_query(args.username, scheduled_time)
        response = request(url).text
        for tweet in reversed(read_tweets(response)):
            print(tweet['created_at'] + " : " + tweet['full_text'])
        time.sleep(args.frequency * MINUTES_TO_SECONDS)
        scheduled_time = pre_execution_timestamp

