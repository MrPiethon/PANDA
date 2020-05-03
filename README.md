# MyDramaList.com Plex Metadata Agent

This Plex Media Server plugin provides two metadata agents to match TV Shows and Movies in your
Plex media libraries to titles from MyDramaList.com.

## Installation

1. Download this repository by either:
    - using `git clone`, or
    - downloading an archive on GitLab.com and extracting it
2. Copy or symlink the `MyDramaList.bundle` folder into the `Plug-ins` folder in your
  [Plex application data folder][appdata]
3. Navigate to the `Contents/Code` directory inside the `MyDramaList.bundle` folder
    - If you copied the folder, be sure to navigate to the copy in the
      [Plex application data folder][appdata]
4. Copy the `.example.env` file to a new file named `.env` in the same folder
   (`MyDramaList.bundle/Contents/Code`)
    - If you can't see these "dotfiles", you will need to update your file manager's settings to
      allow you to see them
5. Open the copied `.env` file in a text editor,
6. In that `.env` file, put your MyDramaList.com [API Client ID][clientid] on the `CLIENT_ID=` line
    - For example, if your API Client ID is `myclientid`, make sure the `.env` file has
      `CLIENT_ID=myclientid`
    - This plugin doesn't need your API Secret Key, so you can skip adding it to the `.env` file
7. In that same `.env` file, configure your desired title source
    - You can choose between `title` and `original_title`
    - `title` typically corresponds to the translated English title
    - `original_title` typically corresponds to the original title in the media's native language
    - The default setting is `title` if this setting is invalid or not preseent
8. Restart your Plex Media Server to ensure the plugin is properly loaded

## Usage

Once the plugin is installed, you will be able to [configure your media libraries to use the
metadata agents][agents]. To do so:

1. Open the library you want to modify
2. Click on the vertical three dots button ("Actions") next to your library name to open the menu
3. In the menu, go to Manage Library > Edit...
4. In the modal dialog that appears, go the Advanced
5. Scroll to the bottom of the Advanced screen, and find the selectbox/dropdown next to Agent
6. Select the `MyDramaList.com - TV Shows` or `MyDramaList.com - Movies` agent as appropriate for
  the media library type

Repeat these steps as needed for the media libraries you want to match against MyDramaList.com.
Please note that these agents are intended to be the primary metadata agent for a given library,
and have not been tested for interactions with other agents set as primary or secondary agents.

## Troubleshooting Unmatched Media

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
reliable automatic matching. There may be some exceptions to this rule when the title from
MyDramaList.com is itself bilingual. For any unmatched media, try to update your folder and file
names to match as much as possible to one version of the title from MyDramaList.com.

Finally, it appears that searching using non-English characters in general is difficult for the
MyDramaList.com API, either due to internal issues of the API with Unicode characters, or problems
when Plex picks up the filename and provides it to the Python-based environment the agents run in.


[appdata]: https://support.plex.tv/articles/201106098-how-do-i-find-the-plug-ins-folder/
[clientid]: https://mydramalist.com/api_request

[agents]: https://support.plex.tv/articles/200241558-agents/#toc-2

[mediaoverview]: https://support.plex.tv/articles/201282253-overview/
[movies]: https://support.plex.tv/articles/categories/your-media/naming-your-movie-media-files/
[tvshows]: https://support.plex.tv/articles/categories/your-media/naming-and-organizing-tv-shows/
[matchprocess]: https://support.plex.tv/articles/200889878-matching-process/
[fixmatches]: https://support.plex.tv/articles/201018497-fix-match-match/
[badnames]: https://support.plex.tv/articles/201019537-rename-a-badly-named-file/
