#!/usr/bin/env node

const RoonApi = require('node-roon-api');
const RoonApiBrowse = require('node-roon-api-browse');
const yaml = require('js-yaml');
const fs = require('fs');
const path = require('path');

const roon = new RoonApi({
    extension_id: 'com.roonexporttags.extension',
    display_name: 'Roon Export Tags',
    display_version: '1.0.0',
    publisher: 'Roon Export Tags',
    email: 'noreply@roonexporttags.com',
    website: 'https://github.com/roon-export-tags',
    
    core_paired: function(core_) {
        console.log('Paired with Roon Core:', core_.display_name);
        core = core_;
        
        setTimeout(() => {
            exportTags();
        }, 1000);
    },

    core_unpaired: function(core_) {
        console.log('Unpaired from Roon Core:', core_.display_name);
        core = null;
    }
});

roon.init_services({
    provided_services: [],
    required_services: [RoonApiBrowse]
});

let core;

function exportTags() {
    if (!core) {
        console.error('Not connected to Roon Core');
        process.exit(1);
    }

    console.log('Browsing tags...');
    
    core.services.RoonApiBrowse.browse({
        hierarchy: 'browse',
        pop_all: true
    }, (err, r) => {
        if (err) {
            console.error('Error browsing:', err);
            process.exit(1);
        }

        const tagItem = r.items.find(item => item.title === 'Tags');
        if (!tagItem) {
            console.error('Tags not found in browse hierarchy');
            process.exit(1);
        }

        core.services.RoonApiBrowse.browse({
            hierarchy: 'browse',
            item_key: tagItem.item_key
        }, (err, tagsList) => {
            if (err) {
                console.error('Error browsing tags:', err);
                process.exit(1);
            }

            const collections = {};
            let completed = 0;
            const totalTags = tagsList.items.length;

            if (totalTags === 0) {
                console.log('No tags found');
                outputResults({});
                return;
            }

            tagsList.items.forEach(tag => {
                const tagId = tag.title.toLowerCase().replace(/\s+/g, '_').replace(/[^a-z0-9_]/g, '');
                
                core.services.RoonApiBrowse.browse({
                    hierarchy: 'browse',
                    item_key: tag.item_key
                }, (err, albumsList) => {
                    if (err) {
                        console.error(`Error browsing albums for tag ${tag.title}:`, err);
                        completed++;
                        checkCompletion();
                        return;
                    }

                    const albums = albumsList.items
                        .filter(item => item.hint === 'list')
                        .map(album => {
                            if (album.image_key && album.image_key.startsWith('file://')) {
                                return album.image_key.replace('file://', '').replace(/^.*\/Music\//, '');
                            }
                            return album.title;
                        });

                    collections[tagId] = {
                        name: tag.title,
                        albums: albums
                    };

                    completed++;
                    console.log(`Processed tag: ${tag.title} (${albums.length} albums)`);
                    checkCompletion();
                });
            });

            function checkCompletion() {
                if (completed === totalTags) {
                    outputResults(collections);
                }
            }
        });
    });
}

function outputResults(collections) {
    const output = {
        collections: collections
    };

    const yamlStr = yaml.dump(output, {
        indent: 2,
        lineWidth: -1
    });

    const outputFile = process.argv[2] || 'roon-tags.yaml';
    fs.writeFileSync(outputFile, yamlStr);
    console.log(`\nTags exported to: ${outputFile}`);
    process.exit(0);
}

console.log('Starting Roon Extension...');
console.log('Searching for Roon Core on the network...');
console.log('Make sure to approve this extension in Roon Settings > Extensions when prompted.');

roon.start_discovery();