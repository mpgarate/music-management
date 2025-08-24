#!/usr/bin/env python3
import os
import re
import yaml
from pathlib import Path
import glob

def parse_track_number(filename):
    """Extract track number from filename, returns (track_num, filename)"""
    # Try common patterns: "01 - Title.mp3", "01. Title.mp3", "01 Title.mp3"
    patterns = [
        r'^(\d+)\s*[-\.]\s*(.+)',
        r'^(\d+)\s+(.+)',
        r'^track\s*(\d+)',
    ]
    
    for pattern in patterns:
        match = re.match(pattern, filename, re.IGNORECASE)
        if match:
            return int(match.group(1)), filename
    
    # If no track number found, return 0 and filename
    return 0, filename

def find_audio_files(album_path):
    """Find all audio files in an album directory and sort by track number"""
    audio_extensions = ['mp3', 'flac', 'ogg', 'wav', 'm4a', 'aac']
    audio_files = []
    
    # Walk through all subdirectories to find audio files
    for root, dirs, files in os.walk(album_path):
        for file in files:
            if any(file.lower().endswith('.' + ext) for ext in audio_extensions):
                audio_files.append(os.path.join(root, file))
    
    # Sort by track number
    tracked_files = []
    for file_path in audio_files:
        filename = os.path.basename(file_path)
        track_num, _ = parse_track_number(filename)
        tracked_files.append((track_num, file_path))
    
    # Sort by track number, then by filename
    tracked_files.sort(key=lambda x: (x[0], x[1]))
    
    return [file_path for _, file_path in tracked_files]

def sanitize_filename(filename):
    """Remove or replace invalid filename characters"""
    # Replace invalid characters with underscores
    invalid_chars = r'<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def create_playlist_name(album_path):
    """Create playlist name from album folder name only"""
    album_folder = os.path.basename(album_path)
    return sanitize_filename(album_folder)

def main():
    # Load the YAML file
    with open('roon_tags.yaml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Create playlists directory if it doesn't exist
    os.makedirs('Playlists', exist_ok=True)
    
    # Process each collection
    for collection_key, collection_data in data['collections'].items():
        collection_name = collection_data['name']
        sanitized_collection_name = sanitize_filename(collection_name)
        
        # Create collection directory
        collection_dir = os.path.join('Playlists', sanitized_collection_name)
        os.makedirs(collection_dir, exist_ok=True)
        
        for album_rel_path in collection_data['albums']:
            # Convert to full path from Music directory
            album_full_path = os.path.join('Music', album_rel_path)
            
            # Check if the album directory exists
            if not os.path.exists(album_full_path):
                print(f"Warning: Album directory not found: {album_full_path}")
                continue
            
            # Find audio files in the album
            audio_files = find_audio_files(album_full_path)
            
            if not audio_files:
                print(f"Warning: No audio files found in: {album_full_path}")
                continue
            
            # Create playlist name and file
            playlist_name = create_playlist_name(album_rel_path)
            playlist_filename = f"{playlist_name}.m3u8"
            playlist_path = os.path.join(collection_dir, playlist_filename)
            
            # Write playlist file
            with open(playlist_path, 'w', encoding='utf-8') as playlist_file:
                playlist_file.write(f"#EXTM3U\n")
                playlist_file.write(f"#PLAYLIST:{playlist_name}\n")
                
                for audio_file in audio_files:
                    # Make path relative to rockbox root for the playlist
                    playlist_file.write(f"{audio_file}\n")
            
            print(f"Created playlist: {sanitized_collection_name}/{playlist_filename} ({len(audio_files)} tracks)")

if __name__ == "__main__":
    main()