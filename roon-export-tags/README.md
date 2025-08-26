# Roon Export Tags

## Claude Instructions

In this dir we have two scripts:

- export_tags.py - exports roon tags to a yaml file of album names
- convert_collections.py - converts the yaml file to a set of playlists.

Please combine them into a single script 'export_tags_to_playlists.py'. We no longer need the yaml file. Otherwise, ensure the logic remains the same.

The instructions below were used to create the original export_tags.py script.

Note that we have a 'Music' directory available and can test the script to ensure that playlists are created with the correct set of tracks in the right order.

## Previous Instructions

### Extract Roon Tags

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
