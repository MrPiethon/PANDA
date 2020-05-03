# pylint: disable=undefined-variable, import-error, no-name-in-module

from difflib import SequenceMatcher
from unicodedata import normalize

from http import mdlfetchsearch, mdlfetchdetail
from log import dump

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

def mdlsearchresult(name, year, entry, year_affects_match_score):
    fetchedyear = entry["year"]

    candidates = [
        entry["title"],
        entry["original_title"],
        "{0} {1}".format(entry["title"], entry["original_title"]),
        "{0} {1}".format(entry["original_title"], entry["title"]),
    ]
    candidates.extend(mdlfetchdetail(entry["id"])["alt_titles"])
    score = max(map(lambda candidate: mdlcalcscore(name, candidate, year, fetchedyear, year_affects_match_score), candidates))

    return MetadataSearchResult(
        id=str(entry["id"]),
        name="{0} ({1})".format(entry["title"], entry["original_title"]),
        year=fetchedyear,
        score=score,
        lang=Locale.Language.English)

def mdlsearch(name, year, mediatypes, max_episodes, year_affects_match_score):
    Log.Info("Handling search for `%s (%s)` in %s", name, year, mediatypes)

    fetched = mdlfetchsearch(name)
    Log.Debug("Fetched search results len=%s entries=%s", len(fetched), dump(fetched))

    results = [
        mdlsearchresult(name, year, entry, year_affects_match_score)
        for entry in fetched
        if entry["type"] in mediatypes
        and entry.get("episodes", 1) <= max_episodes
    ]

    Log.Info("Populated metadata search results len=%s entries=%s", len(results), dump(results))
    return results
