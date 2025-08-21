#!/usr/bin/env python3

import pandas as pd
import yaml
import os
from pathlib import Path
from collections import defaultdict

def extract_album_paths():
    tracks_df = pd.read_excel('LibraryTracks-638913269643781023.xlsx')
    
    album_paths = {}
    for _, row in tracks_df.iterrows():
        if pd.isna(row['Album Artist']) or pd.isna(row['Album']) or pd.isna(row['Path']):
            continue
            
        album_key = f"{row['Album Artist']} - {row['Album']}"
        if album_key not in album_paths:
            path = Path(row['Path'])
            album_path = str(path.parent)
            music_prefix = "/mnt/rhizome/Media Library/Music/"
            if album_path.startswith(music_prefix):
                relative_path = album_path[len(music_prefix):]
                album_paths[album_key] = relative_path
    
    return album_paths

def extract_tags_and_albums():
    albums_df = pd.read_excel('LibraryAlbums-638913204954786245.xlsx')
    
    tag_albums = defaultdict(list)
    
    for _, row in albums_df.iterrows():
        if pd.isna(row['Tags']) or pd.isna(row['Album Artist']) or pd.isna(row['Title']):
            continue
            
        album_key = f"{row['Album Artist']} - {row['Title']}"
        tags = str(row['Tags']).split(',')
        
        for tag in tags:
            tag = tag.strip()
            if tag:
                tag_albums[tag].append(album_key)
    
    return tag_albums

def create_yaml_output():
    album_paths = extract_album_paths()
    tag_albums = extract_tags_and_albums()
    
    collections = {}
    
    for tag, albums in tag_albums.items():
        collection_key = tag.lower().replace(' ', '_').replace('-', '_')
        
        album_paths_for_tag = []
        for album in albums:
            if album in album_paths:
                album_paths_for_tag.append(album_paths[album])
        
        if album_paths_for_tag:
            collections[collection_key] = {
                'name': tag,
                'albums': sorted(album_paths_for_tag)
            }
    
    output = {'collections': collections}
    
    with open('roon_tags.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(output, f, default_flow_style=False, allow_unicode=True, sort_keys=True, width=1000)
    
    print(f"Generated roon_tags.yaml with {len(collections)} collections")

if __name__ == "__main__":
    create_yaml_output()