# pylint: disable=undefined-variable, import-error, no-name-in-module

from difflib import SequenceMatcher
from unicodedata import normalize

from http import mdlfetchsearch, mdlfetchdetail
from log import dump
from mediatypes import MEDIA_TYPE_DRAMA

def prepares(string):
    return normalize("NFC", unicode(string)).lower()

def mdlcalcscore(givenname, fetchedname, givenyear, fetchedyear, deductmissing):
    score = int(SequenceMatcher(None, prepares(givenname), prepares(fetchedname)).ratio() * 100)
    Log.Debug(
        "Calculated similarity score %d for on-disk metadata name `%s` and fetched API entry name `%s`",
        score, givenname, fetchedname)

    if fetchedyear is None:
        deduction = 10 if deductmissing else 0
        Log.Debug("Deducting score %s by %s due to missing year in fetched API entry", score, deduction)
    elif givenyear is None:
        deduction = 10 if deductmissing else 0
        Log.Debug("Deducting score %s by %s due to missing year in on-disk metadata", score, deduction)
    elif int(givenyear) != int(fetchedyear):
        deduction = abs(int(givenyear) - int(fetchedyear))
        Log.Debug(
            "Deducting score %s by %s due to mismatch between on-disk metadata year %s and fetched API entry year %s",
            score, deduction, givenyear, fetchedyear)
    else:
        deduction = 0

    score = max(score - deduction, 0)

    Log.Debug(
        "Calculated final similary score %d for on-disk metadata title `%s (%s)` and fetched API entry title `%s (%s)`",
        score, givenname, givenyear, fetchedname, fetchedyear)

    return score

def mdlsearchresult(name, year, entry, mediatypes):
    fetchedyear = entry.get("year")

    deductscoremissingyear = MEDIA_TYPE_DRAMA not in mediatypes

    return MetadataSearchResult(
        id=str(entry.get("id")),
        name=entry.get("title"),
        year=fetchedyear,
        score=max(
            mdlcalcscore(name, entry.get("title"), year, fetchedyear, deductscoremissingyear),
            mdlcalcscore(name, entry.get("original_title"), year, fetchedyear, deductscoremissingyear),
            *map(
                lambda x: mdlcalcscore(name, x, year, fetchedyear, deductscoremissingyear),
                mdlfetchdetail(entry.get("id")).get("alt_titles"))),
        lang=Locale.Language.English)

def mdlsearch(name, year, mediatypes):
    Log.Info("Handling search for `%s (%s)` in %s", name, year, mediatypes)

    fetched = mdlfetchsearch(name)
    Log.Debug("Fetched search results len=%s entries=%s", len(fetched), dump(fetched))

    results = [
        mdlsearchresult(name, year, entry, mediatypes)
        for entry in fetched
        if entry.get("type") in mediatypes
    ]

    Log.Info("Populated metadata search results len=%s entries=%s", len(results), dump(results))
    return results
