# PANDA

> **P**lex **A**sia**N** **D**rama **A**gent

This Plex Media Server plugin provides two metadata agents to match TV Shows and Movies in your
Plex media libraries to titles from MyDramaList.com.

## Installation

1. Download this repository by either:
    - using `git clone`, or
    - downloading an archive from GitHub.com and extracting it
2. Copy or symlink the `MyDramaList.bundle` folder into the `Plug-ins` folder in your
    [Plex application data folder][appdata]
3. Restart your Plex Media Server to ensure the plugin is properly loaded

## Usage

Once the plugin is installed, you will be able to [configure your media libraries to use the
metadata agents][agents]. To do so:

1. Open the library you want to modify
2. Click on the vertical three dots button ("Actions") next to your library name to open the menu
3. In the menu, go to Manage Library > Edit...
4. In the modal dialog that appears, go the Advanced tab
5. Scroll to the bottom of the Advanced screen, and find the selectbox/dropdown next to Agent
6. Select the `MyDramaList.com - TV Shows` or `MyDramaList.com - Movies` agent as appropriate for
    the media library type
7. Configure the agent's settings
    - Add your [MyDramaList.com API Client ID][clientid] to the Client ID text field
    - Select whehter or not you want to use translated English titles or the original native
      language title when updating media with metadata

Repeat these steps as needed for the media libraries you want to match against MyDramaList.com.
Please note that these agents are intended to be the primary metadata agent for a given library,
and have not been tested for interactions with other agents set as primary or secondary agents.

## Troubleshooting Unmatched Media

### Validation Errors

Note that due to limitations beyond this plugin's control, validations performed by this plugin are
not presented by Plex clients when configuring libraries or agents. If you are encountering issues,
first check the [Media Server Logs][logs] for any validation errors or warnings emitted by the
plugin (`com.plexapp.plugins.MyDramaList`).

### Title Matching

The plugin does its best to match items using the titles provided by the API. If a filename doesn't
sufficiently match any of the titles, Plex **will not** automatically update the media item using
data from the API.

Here's more information from Plex on:
- [working with your files in general][mediaoverview],
- [organizing movies][movies],
- [organizing TV shows][tvshows],
- [the matching process][matchprocess],
- [fixing matches][fixmatches], and
- [checking for badly named files][badnames]

You can manually view any possible matches along with a confidence score by
selecting "Match..." from a TV Series' or Movie's context menu available from the three-dot menu
visible when hovering over a TV Show or Movie; due note, however, that manual matching cannot be
done from an individual episode or season.

If a filename that has two title versions (such as in different langauges), the agents may not be
able to calculate a good match since each version of an item's title is compared separately. For
example, a folder like "SUITS スーツ" or file like "SUITS スーツ - S01E01 - Episode 1.mkv" should
ideally have either the English ("SUITS") or Japanese ("スーツ") title, but not both if you want
reliable automatic matching.

There may be some exceptions to that rule when the title from MyDramaList.com is itself bilingual.
For any unmatched media, try to update your folder and file names to match as much as possible to
one version of the title from MyDramaList.com. Additionally, the API often does not provide any
alternate "Also Known As" titles even if they are shown on the main site.

Finally, it appears that searching using non-English characters in general is difficult for the
MyDramaList.com API, either due to internal issues of the API with Unicode characters, or problems
when Plex picks up the filename and provides it to the Python-based environment the agents run in.


[appdata]: https://support.plex.tv/articles/201106098-how-do-i-find-the-plug-ins-folder/

[clientid]: https://mydramalist.com/api_request
[agents]: https://support.plex.tv/articles/200241558-agents/#toc-2

[logs]: https://support.plex.tv/articles/200250417-plex-media-server-log-files/#toc-1

[mediaoverview]: https://support.plex.tv/articles/201282253-overview/
[movies]: https://support.plex.tv/articles/categories/your-media/naming-your-movie-media-files/
[tvshows]: https://support.plex.tv/articles/categories/your-media/naming-and-organizing-tv-shows/
[matchprocess]: https://support.plex.tv/articles/200889878-matching-process/
[fixmatches]: https://support.plex.tv/articles/201018497-fix-match-match/
[badnames]: https://support.plex.tv/articles/201019537-rename-a-badly-named-file/
