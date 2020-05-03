# pylint: disable=undefined-variable, method-hidden

import re
from json import JSONEncoder

class MyDramaListJSONEncoder(JSONEncoder):
    scalars = {
        "Framework.modelling.attributes.StringObject",
        "Framework.modelling.attributes.FloatObject",
        "Framework.modelling.attributes.IntegerObject",
    }

    collections = {
        "Framework.modelling.attributes.SetObject",
        "Framework.modelling.attributes.MapObject",
        "Framework.modelling.attributes.ProxyContainerObject",
    }

    simpledicts = {
        "Framework.objects.MediaContainer",
        "Framework.api.agentkit.MediaTree",
        "Framework.api.agentkit.MediaItem",
        "Framework.api.agentkit.MediaPart",
        "Framework.api.agentkit.MediaStream",
        "Framework.api.agentkit.TV_Show",
        "Framework.api.agentkit.Movie",
        "Framework.objects.MetadataSearchResult",
    }

    DateObject = "Framework.modelling.attributes.DateObject"
    ObjectContainerObject = "Framework.modelling.attributes.ObjectContainerObject"
    MapItem = "Framework.modelling.attributes.MapItem"
    ProxyContainerItem = "Framework.modelling.attributes.ProxyContainerItem"
    ProxiedDataObject = "Framework.modelling.attributes.ProxiedDataObject"
    MediaContainer = "Framework.modelling.objects.MediaContainer"
    MediaContentsDirectory = "Framework.api.agentkit.MediaContentsDirectory"
    SubtitlesDirectory = "Framework.api.agentkit.SubtitlesDirectory"
    RecordObject = "Framework.modelling.attributes.RecordObject"

    def default(self, o):
        try:
            otype = re.findall("^<class '(.*)'>$", repr(type(o)))[0]
        except IndexError:
            raise RuntimeError("Could not get class name for object {0}".format(o))

        if otype in self.scalars:
            return getattr(o, "_value")
        elif otype in self.collections:
            return getattr(o, "_items")
        elif otype in self.simpledicts:
            return {
                key: value
                for key, value
                in getattr(o, "__dict__").iteritems()
                if not key.startswith("_") or key == "__items__"}
        elif otype == self.DateObject:
            return repr(getattr(o, "_value"))
        elif otype == self.ObjectContainerObject:
            return getattr(o, "_container")
        elif otype == self.MapItem:
            return getattr(o, "_value")
        elif otype == self.ProxyContainerItem:
            return getattr(o, "_obj")
        elif otype == self.ProxiedDataObject:
            return "data <len={0} format={1}>".format(
                len(getattr(o, "_data")),
                getattr(o, "_format"))
        elif otype == self.MediaContainer:
            return getattr(o, "_objects")
        elif otype == self.MediaContentsDirectory:
            return { "path": getattr(o, "_path"), "readonly": getattr(o, "_readonly") }
        elif otype == self.SubtitlesDirectory:
            return { "path": getattr(o, "_path"), "lang_dirs": getattr(o, "_lang_dirs") }
        elif otype == self.RecordObject:
            return getattr(o, "_attributes")
        else:
            Log.Debug("unknown type o=%s otype=%s %s", o, otype, getattr(o, "__dict__"))
            return JSONEncoder.default(self, o)

def dump(o):
    return MyDramaListJSONEncoder(indent=None, skipkeys=False).encode(o)
