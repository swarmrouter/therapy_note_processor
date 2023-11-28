#!/usr/bin/python3

# Import fitz (PyMuPDF), sys, os, and time modules
import fitz
import sys
import os
import time
import re

# Get the folder path from the command line argument or use the current directory
folder_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

# Get the merge option from the command line argument or use False
merge = sys.argv[2] == "-merge" if len(sys.argv) > 2 else False

# Initialize an empty list to store the text from the PDF files
text_list = []

# Iterate over the files in the folder
for file in os.listdir(folder_path):
    # Check if the file is a PDF file
    if file.endswith(".pdf"):
        # Get the full path of the PDF file
        pdf_path = os.path.join(folder_path, file)
        # Open the PDF file using fitz
        doc = fitz.open(pdf_path)
        # Initialize an empty string to store the text
        text = ""
        # Iterate over the pages of the PDF file
        for page in doc:
            # Extract the text from the page using get_text() method
            page_text = page.get_text()
            # Replace newlines with spaces in the text
            page_text = page_text.replace("\n", " ")
            # Append the text to the string
            text += page_text
        # Close the PDF file
        doc.close()
        # Strip whitespace
        p = re.compile(r'\s+')
        text = re.sub(p,'',text)
        # Append the text to the list
        text_list.append(text)
        # If merge option is False, write the text to a separate file
        if not merge:
            # Get the output file name by adding ".out" extension to the PDF file name
            output_file = file + ".out"
            # Get the output file path by joining the folder path and the output file name
            output_path = os.path.join(folder_path, output_file)
            # Open the output file in write mode
            with open(output_path, "w") as f:
                # Write the text to the output file
                f.write(text)

# If merge option is True, write all the text to a single file
if merge:
    # Get the output file name by using the current epoch time and adding ".out" extension
    output_file = str(int(time.time())) + ".out"
    # Get the output file path by joining the folder path and the output file name
    output_path = os.path.join(folder_path, output_file)
    # Open the output file in write mode
    with open(output_path, "w") as f:
        # Iterate over the text list
        for text in text_list:
            # Write the text to the output file
            f.write(text)

