# Roon Export Tags

## Claude Instructions

We have many "tags" in Roon, and each tag has a set of albums within it. The same album can appear in multiple tags.

This folder should provide a command which prints out the tags in a yaml file along with a list of the paths for each album in the TAG. In the yaml file we will call a tag a 'collection'.

Example yaml:

```
# Paths are relative to the Music directory

collections:
  dinner_jazz:
    name: "Dinner Jazz"
    albums:
      - "beets-qobuz/Bill Evans _ Jim Hall/1962 - Undercurrent"

  road_trip:
    name: "Road Trip"
    albums:
      - "beets-qobuz/Two Door Cinema Club/2010 - Tourist History/"
```

To achieve this, let's use LibraryAlbums-*.xlsx as the source of truth for which albums have which tags, and LibraryTracks-*.xlsx can provide a file path to the album (we just need to grab one of its tracks and strip off the track filename to get the album path).

Please use python. If any system packages are needed, use a shell.nix file to manage the environment. If only python packages are needed and nothing else, use uv.
