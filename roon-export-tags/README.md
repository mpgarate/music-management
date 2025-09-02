# Roon Export Tags

## Claude Instructions

In export_tags_to_playlists.py, there are two hard-coded xslx files in the script. Let's add cli arguments to provide them with --roon-tracks and --roon-albums.

When done, run the command with the files in this dir.

To test the script, we can run it using nix and the shell.nix file in this dir.

## Usage

1. In roon, click albums, select all of them, and in the top 3 dots, export as xslx.
1. Click tracks, select all of them, and export as xslx.
1. Copy both xslx to the rockbox device root.
1. In a linux shell, cd to the rockbox directory.
  1. May be needed: `sudo mount -t drvfs 'E:' /mnt/sdcard`
1. Run `nix-shell`
1. Run `./export_tags_to_playlists --roon-albums REPLACEME --roon-tracks REPLACEME`
1. Safely eject the device.


