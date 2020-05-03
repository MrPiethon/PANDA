# pylint: disable=undefined-variable, no-name-in-module

import os

from datetime import datetime

from helpers import any
from http import mdlfetchdetail, mdlfetchcredits
from log import dump

MILLISECONDS_PER_MINUTE = 60000

TITLE_SOURCE = None

def mdltitlesource():
    global TITLE_SOURCE

    if TITLE_SOURCE is None:
        source = os.environ.get("TITLE_SOURCE", None)
        if source in {"title", "original_title"}:
            Log.Debug("Using property `%s` for media titles", source)
            TITLE_SOURCE = source
        else:
            Log.Debug("Using default property `title` for media titles")
            TITLE_SOURCE = "title"

    return TITLE_SOURCE

def mdlairdate(fetched):
    airdate = fetched.get("released") or fetched.get("aired_start")

    if airdate is None or airdate == "0001-01-01":
        return None

    return datetime.strptime(airdate, "%Y-%m-%d").date()

def mdlcreditsprops(job):
    if job == "Screenwriter":
        return ["writers"]
    elif job == "Director":
        return ["directors"]
    elif job == "Producer":
        return ["producers"]
    elif job == "Screenwriter & Director":
        return ["writers", "directors"]
    else:
        Log.Warn("Ignoring unknown role '%s'", job)

def mdlupdate(metadata, media, mediatype):
    titlesource = mdltitlesource()

    Log.Debug(
        "Handling request to update %s metadata\n%s\nusing media\n%s",
        mediatype, dump(metadata.attrs), dump(media))

    fetched = mdlfetchdetail(metadata.id)

    if hasattr(metadata, "year"):
        metadata.year = fetched.get("year")

    metadata.title = fetched.get(titlesource)
    metadata.original_title = fetched.get("original_title")
    metadata.summary = fetched.get("synopsis")
    metadata.duration = int(fetched.get("runtime")) * MILLISECONDS_PER_MINUTE
    metadata.content_rating = fetched.get("certification")
    metadata.rating = float(fetched.get("rating"))
    metadata.originally_available_at = mdlairdate(fetched)

    [metadata.genres.add(entry) for entry in fetched.get("genres") if entry not in metadata.genres]
    [metadata.tags.add(entry) for entry in fetched.get("tags") if entry not in metadata.tags]

    country = fetched.get("country")
    if country not in metadata.countries:
        metadata.countries.add(country)

    credits = mdlfetchcredits(metadata.id)
    Log.Debug("Fetched credits %s", credits)

    for person in credits["crew"]:
        Log.Debug("Handling credits for %s", person)
        job = person["job"]
        for property in mdlcreditsprops(job):
            # Only Movies have top-level cast properties
            collection = getattr(metadata, property, None)
            if collection is None:
                Log.Debug("Property '%s' does not exist, skipping", property)
                continue

            name = person["name"]
            if any(entry.name == name for entry in collection):
                Log.Debug("Person %s already exists in property '%s', skipping", person, property)
                continue

            entry = collection.new()
            entry.name = name
            entry.role = job
            entry.photo = person["images"]["poster"]
            Log.Debug("Added person %s to property '%s'", person, property)

    posterURL = fetched.get("images").get("poster")
    metadata.posters[posterURL] = Proxy.Media(HTTP.Request(posterURL, immediate=False))

    fetched.get("images").get("poster")

    Log.Debug("Updated %s metadata to have contents %s", mediatype, dump(metadata.attrs))
