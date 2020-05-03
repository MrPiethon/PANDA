# pylint: disable=undefined-variable, import-error, no-name-in-module, no-member

from operator import div

from env import loadenv
from http import mdlfetch
from log import dump
from mediatypes import MEDIA_TYPE_MOVIE, MEDIA_TYPE_SPECIAL, MEDIA_TYPE_DRAMA
from search import mdlsearch
from update import mdlupdate

AGENT_NAME = "MyDramaList.com"

def Start():
    Log.Info("Initializing MyDramaList plugin with metadata agents %s", [MyDramaListMovieAgent, MyDramaListTVAgent])

    Log.Debug("Loading environment variables from .env")
    loadenv()

    Log.Info("MyDramaList plugin initialized successfully")

class MyDramaListMovieAgent(Agent.Movies):
    name = AGENT_NAME + " - Movies"
    languages = [Locale.Language.English]
    primary_proivder = True
    fallback_agent = False
    accepts_from = None
    contributes_to = None

    def search(self, results, media, lang, manual):
        Log.Debug("Handling search lang=%s manual=%s, media:\n%s ", lang, manual, dump(media))
        for result in mdlsearch(media.name, media.year, { MEDIA_TYPE_MOVIE, MEDIA_TYPE_SPECIAL }):
            results.Append(result)

    def update(self, metadata, media, lang, force):
        mdlupdate(metadata, media, "Movie")

class MyDramaListTVAgent(Agent.TV_Shows):
    name = AGENT_NAME + " - TV Shows"
    languages = [Locale.Language.English]
    primary_proivder = True
    fallback_agent = False
    accepts_from = None
    contributes_to = None

    def search(self, results, media, lang, manual):
        Log.Debug("Handling search lang=%s manual=%s, media:\n%s ", lang, manual, dump(media))
        for result in mdlsearch(media.show, media.year, { MEDIA_TYPE_DRAMA }):
            results.Append(result)

    def update(self, metadata, media, lang, force):
        mdlupdate(metadata, media, "TV Show")

