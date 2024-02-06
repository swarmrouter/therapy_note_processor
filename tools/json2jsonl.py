#!/usr/bin/python3

# converts a json doc to jsonl
# usage: ./json2jsonl.py input_path output_path

# Import json and sys modules
import json
import sys

# Get the input and output paths from the arguments
input_path = sys.argv[1]
output_path = sys.argv[2]

# Open the input file and load the json data
with open(input_path, "r") as input_file:
    json_data = json.load(input_file)

# Open the output file and write the jsonl data
with open(output_path, "w") as output_file:
    for item in json_data:
        # Convert each item to a json string and add a newline character
        jsonl_item = json.dumps(item) + "\n"
        # Write the jsonl item to the output file
        output_file.write(jsonl_item)
