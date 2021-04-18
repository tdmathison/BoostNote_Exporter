# BoostNote Exporter
Export all BoostNote files and attachments to markdown

## Goal
The goal of this script was for migrating out of BoostNote since they have moved the product to be cloud-based and are now monetizing it forcing monthly payments. I wrote this to get my thousands of notes exported out into MarkDown files for use in another editor

Usage:
`python3 ./boostnote_exporter.py -i ./BoostNote/<SpaceName> -o .`

This will parse through:
```
./BoostNote/<SpaceName>/boostnote.json
./BoostNote/<SpaceName>/attachments/*
./BoostNote/<SpaceName>/notes/*
```

... and create the resulting files at `./output/<SpaceName>/`