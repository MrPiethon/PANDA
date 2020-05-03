# pylint: disable=undefined-variable, import-error, no-name-in-module

import os

from urllib import urlencode

from ratelimiter import RateLimiter

DETAIL_URL = "https://api.mydramalist.com/v1/titles/{0}"
CREDITS_URL = "https://api.mydramalist.com/v1/titles/{0}/credits"
SEARCH_URL = "https://api.mydramalist.com/v1/search/titles"

@RateLimiter(
    max_calls=5,
    period=1,
    callback=lambda until: Log.Warn(
        "mdlfetch() has been rate limited, sleeping %ss until %s",
        until - time(),
        datetime.fromtimestamp(until)))
def mdlfetch(url, ispost):
    return JSON.ObjectFromURL(
        url,
        values={ "": "" } if ispost else None, # force POST request using `values`
        headers={ "mdl-api-key": Prefs["CLIENT_ID"] })

def mdlfetchdetail(id):
    return mdlfetch(DETAIL_URL.format(id), ispost=False)

def mdlfetchcredits(id):
    return mdlfetch(CREDITS_URL.format(id), ispost=False)

def mdlfetchsearch(query):
    return mdlfetch("{0}?{1}".format(SEARCH_URL, urlencode({ "q": query })), ispost=True)
