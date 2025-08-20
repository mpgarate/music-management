# Roon Export Tags

## Claude Instructions

We have many "tags" in Roon, and each tag has a set of albums within it. The same album can appear in multiple tags.

This folder should provide a command which uses the roon extension API to export tags into a yaml format like the following:

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

## Installation

### Using Nix (Recommended)

If you have Nix installed, enter the development environment:

```bash
nix-shell
```

This will automatically provide Node.js and npm.

### Manual Installation

Ensure you have Node.js (version 16 or higher) and npm installed, then:

```bash
npm install
```

## Usage

### Basic Usage

Run the script to export all Roon tags to a YAML file:

```bash
npm start
```

This will create a file called `roon-tags.yaml` in the current directory.

### Custom Output File

Specify a custom output filename:

```bash
npm start my-tags.yaml
```

or

```bash
node index.js my-tags.yaml
```

## Roon Connection Setup

This extension uses the official Roon Extension API and will automatically discover Roon Cores on your local network. No manual configuration of IP addresses or ports is required.

### First Time Setup

1. **Start Roon Core**: Make sure your Roon Core is running on the same network
2. **Run the Extension**: Execute `npm start` 
3. **Approve the Extension**: When prompted, go to Roon Settings > Extensions and approve "Roon Export Tags"
4. **Export Begins**: The script will automatically connect and begin exporting your tags

### Network Requirements

- The computer running this script must be on the same local network as your Roon Core
- Roon Core must be running and accessible
- No firewall should be blocking the connection between the script and Roon Core

### Troubleshooting Connection Issues

If the script can't find your Roon Core:

1. **Check Network**: Ensure both devices are on the same network
2. **Restart Roon Core**: Sometimes a restart helps with discovery
3. **Check Firewall**: Temporarily disable firewall to test connectivity
4. **Check Extensions**: Go to Roon Settings > Extensions and make sure "Roon Export Tags" is enabled

The extension will automatically retry connection if the Core becomes unavailable and reconnects when it's back online.
