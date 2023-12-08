#!/usr/bin/python3

# Import the re module for regular expressions
import re

# Import the sys module for command line arguments
import sys

# Define the regex pattern to apply to the file contents
# For example, this pattern will replace all occurrences of 'foo' with 'bar'
# pattern = re.compile(r'foo')

# Define the function that takes two arguments: input file path and output file path
def process_file(input_file, output_file):
    # Open the input file in read mode
    with open(input_file, 'r') as infile:
        # Read the contents of the input file
        contents = infile.read()
        # Apply the regex pattern to the contents and get the modified contents
        modified_contents = re.sub('Bob', '<<THERAPIST>>', contents)
        modified_contents = re.sub(' ','',modified_contents)
    # Open the output file in write mode
    with open(output_file, 'w') as outfile:
        # Write the modified contents to the output file
        outfile.write(modified_contents)

# Define the usage message to display if the arguments are not passed in
usage = "Usage: python script.py input_file output_file\nThis script will open the input file, apply a regex to the file contents, and write the modified contents to the output file."

# Check if the number of arguments is less than 3 (the script name, input file path, and output file path)
if len(sys.argv) < 3:
    # Print the usage message and exit the script
    print(usage)
    sys.exit()
else:
    # Get the input file path and output file path from the command line arguments
    # The first argument is the script name, so we ignore it
    # The second argument is the input file path
    input_file = sys.argv[1]
    # The third argument is the output file path
    output_file = sys.argv[2]

    # Call the function with the input file path and output file path as arguments
    process_file(input_file, output_file)

