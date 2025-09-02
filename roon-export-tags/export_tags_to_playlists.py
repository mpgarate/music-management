#!/usr/bin/env python3

import pandas as pd
import os
import re
from pathlib import Path
from collections import defaultdict
import glob
import argparse

OUTPUT_PATH_PREFIX = "Playlists/Roon Tags"


def extract_album_paths(tracks_file):
    tracks_df = pd.read_excel(tracks_file)

    album_paths = {}
    for _, row in tracks_df.iterrows():
        if (
            pd.isna(row["Album Artist"])
            or pd.isna(row["Album"])
            or pd.isna(row["Path"])
        ):
            continue

        album_key = f"{row['Album Artist']} - {row['Album']}"
        if album_key not in album_paths:
            path = Path(row["Path"])
            album_path = str(path.parent)
            music_prefix = "/mnt/rhizome/Media Library/Music/"
            if album_path.startswith(music_prefix):
                relative_path = album_path[len(music_prefix) :]
                album_paths[album_key] = relative_path

    return album_paths


def extract_tags_and_albums(albums_file):
    albums_df = pd.read_excel(albums_file)

    tag_albums = defaultdict(list)

    for _, row in albums_df.iterrows():
        if (
            pd.isna(row["Tags"])
            or pd.isna(row["Album Artist"])
            or pd.isna(row["Title"])
        ):
            continue

        album_key = f"{row['Album Artist']} - {row['Title']}"
        tags = str(row["Tags"]).split(",")

        for tag in tags:
            tag = tag.strip()
            if tag:
                tag_albums[tag].append(album_key)

    return tag_albums


def parse_track_number(filename):
    """Extract track number from filename, returns (track_num, filename)"""
    patterns = [
        r"^(\d+)\s*[-\.]\s*(.+)",
        r"^(\d+)\s+(.+)",
        r"^track\s*(\d+)",
    ]

    for pattern in patterns:
        match = re.match(pattern, filename, re.IGNORECASE)
        if match:
            return int(match.group(1)), filename

    return 0, filename


def find_audio_files(album_path):
    """Find all audio files in an album directory and sort by track number"""
    audio_extensions = ["mp3", "flac", "ogg", "wav", "m4a", "aac"]
    audio_files = []

    for root, dirs, files in os.walk(album_path):
        for file in files:
            if any(file.lower().endswith("." + ext) for ext in audio_extensions):
                audio_files.append(os.path.join(root, file))

    tracked_files = []
    for file_path in audio_files:
        filename = os.path.basename(file_path)
        track_num, _ = parse_track_number(filename)
        tracked_files.append((track_num, file_path))

    tracked_files.sort(key=lambda x: (x[0], x[1]))

    return [file_path for _, file_path in tracked_files]


def sanitize_filename(filename):
    """Remove or replace invalid filename characters"""
    invalid_chars = r'<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    return filename


def create_playlist_name(album_path):
    """Create playlist name from album folder name only"""
    album_folder = os.path.basename(album_path)
    return sanitize_filename(album_folder)


def create_playlists(tracks_file, albums_file):
    album_paths = extract_album_paths(tracks_file)
    tag_albums = extract_tags_and_albums(albums_file)

    os.makedirs(OUTPUT_PATH_PREFIX, exist_ok=True)

    for tag, albums in tag_albums.items():
        collection_key = tag.lower().replace(" ", "_").replace("-", "_")
        sanitized_collection_name = sanitize_filename(tag)

        collection_dir = os.path.join(OUTPUT_PATH_PREFIX, sanitized_collection_name)
        os.makedirs(collection_dir, exist_ok=True)

        for album in albums:
            if album not in album_paths:
                continue

            album_rel_path = album_paths[album]
            album_full_path = os.path.join("Music", album_rel_path)

            if not os.path.exists(album_full_path):
                print(f"Warning: Album directory not found: {album_full_path}")
                continue

            audio_files = find_audio_files(album_full_path)

            if not audio_files:
                print(f"Warning: No audio files found in: {album_full_path}")
                continue

            playlist_name = create_playlist_name(album_rel_path)
            playlist_filename = f"{playlist_name}.m3u8"
            playlist_path = os.path.join(collection_dir, playlist_filename)

            with open(playlist_path, "w", encoding="utf-8") as playlist_file:
                playlist_file.write(f"#EXTM3U\n")
                playlist_file.write(f"#PLAYLIST:{playlist_name}\n")

                for audio_file in audio_files:
                    playlist_file.write(f"{audio_file}\n")

            print(
                f"Created playlist: {sanitized_collection_name}/{playlist_filename} ({len(audio_files)} tracks)"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Roon tags to playlists")
    parser.add_argument(
        "--roon-tracks",
        required=True,
        help="Path to the Roon tracks Excel file",
    )
    parser.add_argument(
        "--roon-albums",
        required=True,
        help="Path to the Roon albums Excel file",
    )

    args = parser.parse_args()
    create_playlists(args.roon_tracks, args.roon_albums)
