"""
Copyright (c) 2023, Inclusive Design Institute

Licensed under the BSD 3-Clause License. You may not use this file except
in compliance with this License.

You may obtain a copy of the BSD 3-Clause License at
https://github.com/inclusive-design/baby-bliss-bot/blob/main/LICENSE
"""

import sys
from pprint import pprint

"""
Read and parse a '.wbs' file

file_path: The path to the .wbs file to process.

Example: python parse_wbs.py ./data/wbs/some_wbs_file.wb > output.json

Returns: Prints an array of JSON objects to stdout, one for each line of the
         input '.wbs' file.
"""


def make_shape_entries(shape_string):
    shapes = []
    # Individual shapes are separated by an ampersand.
    shape_splits = shape_string.split('&')
    for asplit in shape_splits:
        # The shape code and grid drawing instructions are separated by '#0'
        # TODO: check this
        shape_and_grid = asplit.split('#0')
        shape_entry = {}
        shape_entry['code'] = shape_and_grid[0].replace('#', '-')
        shape_entry['grid'] = shape_and_grid[1]
        shapes.append(shape_entry)
    return shapes


def make_wbs_entry(wbs_parts_array):
    wbs_entry = {}
    wbs_entry['identifier'] = wbs_parts_array[0]
    wbs_entry['gloss'] = wbs_parts_array[1]
    wbs_entry['pos_colour'] = wbs_parts_array[2]
    wbs_entry['country'] = wbs_parts_array[3]
    wbs_entry['shapes'] = make_shape_entries(wbs_parts_array[4])
    return wbs_entry


def read_parse_wbs_file(wbs_file):
    wbs_json_array = []
    for line in wbs_file:
        line_parts = line.split('$')
        line_dict = make_wbs_entry(line_parts)
        wbs_json_array.append(line_dict)
    return wbs_json_array


def main():
    # Handle command line arguments
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} file_path > output_file')
        print(f'Example: {sys.argv[0]} ./data/wbs/some_wbs_file.wb > output.json')
        sys.exit(1)

    # Handle file type, at least by its extension
    if sys.argv[1].endswith('.wbs') is False:
        print(f'Input file ({sys.argv[1]}) must be a ".wbs" file')
        sys.exit(1)

    # Convert the file
    wbs_file = open(sys.argv[1], mode='r', encoding='latin-1')
    wbs_json_array = read_parse_wbs_file(wbs_file)
    pprint(wbs_json_array)


main()
