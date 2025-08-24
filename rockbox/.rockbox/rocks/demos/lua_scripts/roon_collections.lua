--[[
             __________               __   ___.
   Open      \______   \ ____   ____ |  | _\_ |__   _______  ___
   Source     |       _//  _ \_/ ___\|  |/ /| __ \ /  _ \  \/  /
   Jukebox    |    |   (  <_> )  \___|    < | \_\ (  <_> > <  <
   Firmware   |____|_  /\____/ \___  >__|_ \|___  /\____/__/\_ \
                     \/            \/     \/    \/            \/

 Roon Collections Browser Plugin

 Copyright (C) 2025 Claude Code

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 2
 of the License, or (at your option) any later version.

 This software is distributed on an "AS IS" basis, WITHOUT WARRANTY OF ANY
 KIND, either express or implied.

]]--

require("actions")

-- Global state
local collections = {}
local current_menu = "collections"
local selected_collection = nil
local current_selection = 1
local menu_offset = 0
local max_display_lines = 0

-- Audio file extensions
local audio_extensions = {".mp3", ".flac", ".ogg", ".m4a", ".wav", ".wv", ".mpc", ".ape"}

-- Helper function to read file contents
function file_get_contents(filename)
    local file = io.open(filename, "r")
    if not file then
        return nil
    end
    local contents = file:read("*all")
    file:close()
    return contents
end

-- Simple YAML parser for roon_tags.yaml structure
function parse_yaml(content)
    local result = {}
    local current_collection = nil
    
    for line in content:gmatch("[^\r\n]+") do
        line = line:gsub("^%s*", ""):gsub("%s*$", "")  -- trim whitespace
        
        if line:match("^collections:") then
            -- Start of collections section
        elseif line:match("^'?([^':%s]+)'?:$") or line:match("^\"?([^\":%s]+)\"?:$") then
            -- Collection name (with or without quotes)
            current_collection = line:match("^'?([^':%s]+)'?:") or line:match("^\"?([^\":%s]+)\"?:")
            if current_collection then
                result[current_collection] = {albums = {}, name = current_collection}
            end
        elseif line:match("^albums:") then
            -- Albums section marker
        elseif line:match("^name: (.+)") then
            -- Display name for collection
            if current_collection then
                local name = line:match("^name: (.+)")
                -- Remove quotes if present
                name = name:gsub("^['\"]", ""):gsub("['\"]$", "")
                result[current_collection].name = name
            end
        elseif line:match("^%- (.+)") then
            -- Album path
            if current_collection then
                local album = line:match("^%- (.+)")
                table.insert(result[current_collection].albums, album)
            end
        end
    end
    
    return result
end

-- Load and parse roon_tags.yaml
function load_collections()
    local yaml_path = "/roon_tags.yaml"
    local content = file_get_contents(yaml_path)
    
    if not content then
        rb.splash(2 * rb.HZ, "Error: Could not read roon_tags.yaml")
        return false
    end
    
    collections = parse_yaml(content)
    return true
end

-- Get list of audio files in directory
function get_audio_files(dir_path)
    local files = {}
    local full_path = "/" .. dir_path
    
    -- Try to open directory
    local dir = rb.opendir(full_path)
    if not dir then
        return files
    end
    
    -- Read directory contents
    repeat
        local entry = rb.readdir(dir)
        if entry then
            local filename = entry.name
            if filename ~= "." and filename ~= ".." then
                -- Check if file has audio extension
                for _, ext in ipairs(audio_extensions) do
                    if filename:lower():match(ext:gsub("%.", "%.") .. "$") then
                        table.insert(files, full_path .. "/" .. filename)
                        break
                    end
                end
            end
        end
    until not entry
    
    rb.closedir(dir)
    
    -- Sort files
    table.sort(files)
    return files
end

-- Create playlist from album
function create_album_playlist(album_path)
    local audio_files = get_audio_files(album_path)
    
    if #audio_files == 0 then
        rb.splash(2 * rb.HZ, "No audio files found in album")
        return false
    end
    
    -- Clear current playlist
    rb.playlist("remove_all_tracks")
    
    -- Add all audio files to playlist
    for _, file_path in ipairs(audio_files) do
        rb.playlist("insert_track", file_path, rb.playlist("amount"), false, true)
    end
    
    -- Start playback
    rb.playlist("start", 0, 0, 0)
    
    local message = string.format("Playing album: %d tracks", #audio_files)
    rb.splash(2 * rb.HZ, message)
    
    return true
end

-- Calculate display parameters
function calculate_display()
    local char_height = rb.font_getstringsize("A", rb.FONT_UI)
    max_display_lines = math.floor(rb.LCD_HEIGHT / char_height) - 1
end

-- Draw menu
function draw_menu()
    rb.lcd_clear_display()
    
    local items = {}
    local title = ""
    
    if current_menu == "collections" then
        title = "Roon Collections"
        for collection_id, collection in pairs(collections) do
            table.insert(items, {id = collection_id, name = collection.name})
        end
        -- Sort collections by name
        table.sort(items, function(a, b) return a.name < b.name end)
        
    elseif current_menu == "albums" and selected_collection then
        title = collections[selected_collection].name
        for _, album in ipairs(collections[selected_collection].albums) do
            -- Extract album name from path (last part after /)
            local album_name = album:match("([^/]+)$") or album
            table.insert(items, {id = album, name = album_name})
        end
    end
    
    -- Draw title
    rb.lcd_puts(0, 0, title)
    
    -- Calculate visible range
    if current_selection < menu_offset + 1 then
        menu_offset = current_selection - 1
    elseif current_selection > menu_offset + max_display_lines then
        menu_offset = current_selection - max_display_lines
    end
    
    -- Draw menu items
    for i = 1, math.min(max_display_lines, #items) do
        local item_index = menu_offset + i
        if item_index <= #items then
            local item = items[item_index]
            local line = i
            
            -- Highlight selected item
            if item_index == current_selection then
                -- Use inverse display for selected item
                local text_width = rb.font_getstringsize(item.name, rb.FONT_UI)
                rb.lcd_fillrect(0, line * rb.font_getstringsize("A", rb.FONT_UI), 
                               math.min(text_width, rb.LCD_WIDTH), rb.font_getstringsize("A", rb.FONT_UI))
                rb.lcd_set_drawmode(rb.DRMODE_INVERSEVID)
                rb.lcd_puts(0, line, item.name)
                rb.lcd_set_drawmode(rb.DRMODE_SOLID)
            else
                rb.lcd_puts(0, line, item.name)
            end
        end
    end
    
    -- Store current items for selection handling
    _G.current_items = items
    
    rb.lcd_update()
end

-- Handle user input
function handle_input()
    local action = rb.get_action(rb.contexts.CONTEXT_STD, rb.HZ / 4)
    
    if action == rb.actions.ACTION_STD_CANCEL then
        if current_menu == "albums" then
            -- Go back to collections
            current_menu = "collections"
            selected_collection = nil
            current_selection = 1
            menu_offset = 0
            return true
        else
            -- Exit plugin
            return false
        end
        
    elseif action == rb.actions.ACTION_STD_OK then
        if current_menu == "collections" and _G.current_items then
            -- Select collection
            if current_selection <= #_G.current_items then
                selected_collection = _G.current_items[current_selection].id
                current_menu = "albums"
                current_selection = 1
                menu_offset = 0
            end
            
        elseif current_menu == "albums" and _G.current_items then
            -- Select album and create playlist
            if current_selection <= #_G.current_items then
                local album_path = _G.current_items[current_selection].id
                create_album_playlist(album_path)
            end
        end
        
    elseif action == rb.actions.ACTION_STD_PREV then
        -- Move up
        if _G.current_items and current_selection > 1 then
            current_selection = current_selection - 1
        end
        
    elseif action == rb.actions.ACTION_STD_NEXT then
        -- Move down
        if _G.current_items and current_selection < #_G.current_items then
            current_selection = current_selection + 1
        end
    end
    
    return true
end

-- Main program
function main()
    -- Initialize display parameters
    calculate_display()
    
    -- Load collections from YAML
    if not load_collections() then
        return
    end
    
    -- Check if collections were loaded
    local collection_count = 0
    for _ in pairs(collections) do
        collection_count = collection_count + 1
    end
    
    if collection_count == 0 then
        rb.splash(3 * rb.HZ, "No collections found in roon_tags.yaml")
        return
    end
    
    -- Main loop
    while true do
        draw_menu()
        if not handle_input() then
            break
        end
        rb.yield()
    end
end

-- Start the plugin
main()