# Collections to Rockbox Playlist

## Claude Instructions

Write a python script that converts the roon_tags.yaml file into a set of playlist files compatible with Rockbox. Assume that the paths in the yaml file are all relative to a top level `Music` directory at the root of the rockbox filesystem. The python script will also be run from the root of the rockbox filesystem. The script should locate the tracks under each album on disk and add them to the playlist, ensuring that the tracks are in order by track number.

Each playlist name should begin with the name of the collection, followed by a hyphen, and then the album folder name with album artist included.

For example, one playlist should be:

```
*to_listen - The Album Leaf/2010 - A Chorus of Storytellers
```

## Usage

### Running the Script

1. Place the `roon_tags.yaml` file in the root of your Rockbox filesystem (same directory as the `Music` folder)
2. Run the script from the root of your Rockbox filesystem:
   ```bash
   python3 convert_collections.py
   ```
3. The script will create a `Playlists` directory and generate `.m3u8` playlist files for each collection-album combination

### Requirements

- Python 3.6 or higher
- PyYAML library (install with `pip install pyyaml`)

### Accessing Playlists in Rockbox

1. Copy the generated `Playlists` directory to your Rockbox device
2. In Rockbox, navigate to **Files** → **Playlists**
3. Select the desired playlist (e.g., `*to_listen - The Album Leaf/2010 - A Chorus of Storytellers.m3u8`)
4. The playlist will load with tracks sorted by track number

### Playlist Naming Convention

Playlists are named using the format: `[Collection Name] - [Album Folder Name]`

Examples:
- `*to_listen - The Album Leaf/2010 - A Chorus of Storytellers.m3u8`
- `jazz - Bill Evans _ Jim Hall/1962 - Undercurrent.m3u8`
- `erhu - 乐典/0000 - 乐典：第五届"敦煌杯"二胡音乐会（壹）.m3u8`
