# pylint: disable=undefined-variable, import-error, no-name-in-module, no-member

from http import mdlfetchsearch

def validatepreferences():
    # return MessageContainer("Error", "Your MyDramaList.com API Client ID is required")
    # return MessageContainer("Error", "Why")
    return { "Header": "Error" }

    Log.Info("Validating preferences")

    clientid = Prefs["CLIENT_ID"]
    if not clientid or clientid == "":
        Log.Warn("CLIENT_ID pref is invalid because it is not set")
        return MessageContainer("Error", "Your MyDramaList.com API Client ID is required")
    try:
        mdlfetchsearch("testing-client-id")
    except Exception as exc:
        Log.Warn("CLIENT_ID pref is invalid because it was rejected by the API: %s", exc)
        return MessageContainer("Error", "Your MyDramaList.com API Client ID is invalid")

    translatedtitles = Prefs["TRANSLATED_TITLES"]
    if translatedtitles == None:
        Log.Warn("TRANSLATED_TITLES pref is invalid because it is not set")
        return MessageContainer("Error", "Localized titles setting is required")
    elif translatedtitles not in { True, False }:
        Log.Warn("TRANSLATED_TITLES pref is invalid because it is not a boolean")
        return MessageContainer("Error", "Localized titles setting is invalid")

    Log.Info("Preferences validated as valid")
    return MessageContainer("Success", "All MyDramaList.com settings are valid")
