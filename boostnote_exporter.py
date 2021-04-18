# boostnote_exporter.py
# Export all BoostNote files and attachments to markdown
#
# Goal of this script was for migrating out of BoostNote since they have moved the product to be cloud-based
# and are now monetizing it forcing monthly payments. I wrote this to get my thousands of notes exported out
# into MarkDown files for use in another editor
#
# Travis Mathison
#
# Usage:
# python3 ./boostnote_exporter.py -i ./BoostNote/<SpaceName> -o .
#
# This will parse through:
#   ./BoostNote/<SpaceName>/boostnote.json
#   ./BoostNote/<SpaceName>/attachments/*
#   ./BoostNote/<SpaceName>/notes/*
#
# and create the resulting files at ./output/<SpaceName>/
#

import argparse
import json
import os
import shutil
import re

notes_path = 'notes'
attachments_path = 'attachments'
boostnote_file_path = 'boostnote.json'


def create_directories(input_path, output_path):
    # create basic structure
    if not os.path.isdir(os.path.join(output_path, input_path, notes_path)):
        os.makedirs(os.path.join(output_path, input_path, notes_path))
    if not os.path.isdir(os.path.join(output_path, input_path, attachments_path)):
        os.makedirs(os.path.join(output_path, input_path, attachments_path))

    # create notes folder structure from boostnote.json file
    with open(os.path.join(input_path, boostnote_file_path)) as json_file:
        data = json.load(json_file)
        for folder in data['folderMap']:
            folder_path = data['folderMap'][folder]['_id'][8:]
            path_to_create = os.path.join(output_path, input_path, notes_path, folder_path)
            if not os.path.isdir(path_to_create):
                os.makedirs(path_to_create)
                print("Created directory: ", path_to_create)


def create_files(input_path, output_path):
    # copy the attachment files
    attachment_files = os.listdir(os.path.join(input_path, attachments_path))
    for file in attachment_files:
        shutil.copyfile(
            os.path.join(input_path, attachments_path, file),
            os.path.join(output_path, input_path, attachments_path, file))

    # copy all notes files
    notes_files = os.listdir(os.path.join(input_path, notes_path))
    for file in notes_files:
        with open(os.path.join(input_path, notes_path, file)) as note_file:
            try:
                data = json.load(note_file)
                fixed_filename = data['title'].replace('/', '_').replace(':', '_')
                file_to_create = os.path.join(
                    output_path, input_path, notes_path + data['folderPathname'], fixed_filename + '.md')

                if not os.path.isfile(file_to_create):
                    with open(file_to_create, 'w+') as out_file:
                        content = data['content']

                        # image search
                        image_regex = re.compile(r'!\[([0-9a-zA-Z-_]*\.[a-z]*)]\(([0-9a-zA-Z-_]*\.[a-z]*)\)')
                        mo = image_regex.findall(content)
                        if mo:
                            for match in mo:
                                depth = len(file_to_create.split(r'/')) - 4
                                content = content.replace(
                                    match[1], str.format('{}{}/{}', '../' * depth, attachments_path, match[1]))
                                content = content.replace(match[0], match[1])

                        out_file.write(content)
                        print("Created file: ", file_to_create)
            except json.decoder.JSONDecodeError:
                print(">>> PARSE ERROR: ", file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Export all BoostNote files and attachments to markdown')
    parser.add_argument('-i', '--input', type=str, required=True, help='The root path of the boostNote space')
    parser.add_argument('-o', '--output', type=str, required=True, help='The output directory path')
    args = parser.parse_args()

    output = '{}{}'.format(args.output, '/output')
    create_directories(args.input, output)
    create_files(args.input, output)
    print("Done.")
