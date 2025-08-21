#!/usr/bin/env python3

import yaml
import re

def sanitize_menu_name(name):
    """Convert collection name to valid tagnavi menu name"""
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    sanitized = re.sub(r'_+', '_', sanitized)
    sanitized = sanitized.strip('_')
    return sanitized or 'unnamed'

def escape_path(path):
    """Escape special characters in paths for tagnavi"""
    return path.replace('"', '\\"')

def create_tagnavi_config():
    """Read roon_tags.yaml and generate tagnavi_custom.config"""
    
    # Read the YAML file
    with open('roon_tags.yaml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    collections = data.get('collections', {})
    
    # Start building the tagnavi config
    config_lines = [
        '#! rockbox/tagbrowser/2.0',
        '',
        '# Custom tagnavi config generated from Roon tags',
        '# This creates a menu structure: [Tag List] -> [Album List]',
        '',
        '# Tag selection menu',
        '%menu_start "tag_selection" "Select Tag"'
    ]
    
    # Add each tag as a menu item
    for collection_key, collection_data in sorted(collections.items()):
        tag_name = collection_data.get('name', collection_key)
        menu_name = f"tag_{sanitize_menu_name(collection_key)}"
        config_lines.append(f'"{tag_name}" ==> "{menu_name}"')
    
    config_lines.append('%menu_end')
    config_lines.append('')
    
    # Create individual menus for each tag
    for collection_key, collection_data in sorted(collections.items()):
        tag_name = collection_data.get('name', collection_key)
        menu_name = f"tag_{sanitize_menu_name(collection_key)}"
        albums = collection_data.get('albums', [])
        
        # Build a complex filter that matches any of the album paths
        if albums:
            path_conditions = []
            for album_path in albums:
                escaped_path = escape_path(album_path)
                # Use filename contains to match albums in these directories
                path_conditions.append(f'filename ~ "/{escaped_path}/"')
            
            # Combine all path conditions with OR
            filter_condition = ' | '.join(path_conditions)
            config_lines.append(f'# Tag: {tag_name} -> Albums with tracks in order')
            config_lines.append(f'%menu_start "{menu_name}" "{tag_name}"')
            config_lines.append(f'"*" -> album ? {filter_condition} -> title = "fmt_title"')
            config_lines.append('%menu_end')
        else:
            config_lines.append(f'# Tag: {tag_name} -> No albums')
            config_lines.append(f'%menu_start "{menu_name}" "{tag_name}"')
            config_lines.append('"No albums found" -> album ? filename = "" -> title')
            config_lines.append('%menu_end')
        
        config_lines.append('')
    
    # Write the tagnavi config file
    with open('tagnavi_custom.config', 'w', encoding='utf-8') as f:
        f.write('\n'.join(config_lines))
    
    print(f"Generated tagnavi_custom.config with {len(collections)} tag menus")
    print("Copy this file to your Rockbox device's .rockbox directory")

if __name__ == "__main__":
    create_tagnavi_config()
