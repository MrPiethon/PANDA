# pylint: disable=undefined-variable, import-error, no-name-in-module, no-member

import sys

from operator import div

from log import dump
from search import mdlsearch
from update import mdlupdate
from validate import validatepreferences

AGENT_NAME = "MyDramaList.com"

def Start():
    Log.Info("Initializing MyDramaList plugin with metadata agents %s", [MyDramaListMovieAgent, MyDramaListTVAgent])
    Log.Info("MyDramaList plugin initialized successfully")

def ValidatePrefs():
    return validatepreferences()

class MyDramaListBaseAgent:
    languages = [Locale.Language.English]
    primary_proivder = True
    fallback_agent = False
    accepts_from = None
    contributes_to = None

    def search(self, results, media, lang, manual):
        Log.Debug("Handling search lang=%s manual=%s, media:\n%s ", lang, manual, dump(media))
        for result in mdlsearch(self.searchname(media), media.year, self.media_types, self.max_episodes, self.year_affects_match_score):
            results.Append(result)

    def update(self, metadata, media, lang, force):
        mdlupdate(metadata, media)

class MyDramaListMovieAgent(MyDramaListBaseAgent, Agent.Movies):
    name = AGENT_NAME + " - Movies"
    media_types = { "Movie", "Special" }
    year_affects_match_score = True
    max_episodes = 1

    @staticmethod
    def searchname(media):
        return media.name

class MyDramaListTVAgent(MyDramaListBaseAgent, Agent.TV_Shows):
    name = AGENT_NAME + " - TV Shows"
    media_types = { "Drama", "TV Show" }
    year_affects_match_score = False
    max_episodes = sys.maxint

    @staticmethod
    def searchname(media):
        return media.show
