#!/usr/bin/python3

# Import the required modules
import sys
import os
import yaml
import re
import fitz # PyMuPDF module
from openai import OpenAI # OpenAI API module
from openai import AzureOpenAI # Azure OpenAI Service module

CONFIG_FILE = "./therapy_note_processor.yaml" # The name of the configuration file

# Define the functions

# Load the configuration from the YAML file
def load_config():
    """Load the configuration from the YAML file."""
    # Open the YAML file
    with open(CONFIG_FILE, "r") as f:
        # Load the configuration as a dictionary
        config = yaml.safe_load(f)
    # Return the configuration
    return config

# Return an AI client obj
def get_ai_client():
    # load configuration
    config = load_config()
    apiKey = config['api_key']
    o_ai_client=OpenAI(api_key=apiKey)
    return o_ai_client

# Execute ai prompt and return result text
def runPrompt(o_ai_client,session_note_text):
    # load configuration
    config = load_config()
    systemPrompt = config['system_prompt']
    sessionPrompt = config['session_prompt']
    sessionPrompt = sessionPrompt + " " + session_note_text
    print("\nSYSTEM_PROMPT: "+systemPrompt+"\n")
    print("\nSESSION_PROMPT: "+sessionPrompt+"\n")
    completion = o_ai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": sessionPrompt}
        ]
    )
    response = completion.choices[0].message
    return response.content

class SessionNote:

    def __init__(self, file_name, file_path, note_text):
        """Initialize the attributes of a session note."""
        self.file_name = file_name # The name of the file containing the session note
        self.file_path = file_path # The path of the file containing the session note
        self.note_text = note_text # The text of the session note

    def __str__(self):
        """Return a string representation of a session note."""
        return f"Session note from file {self.file_name}:\n{self.note_text}"

def extract_session_notes():
    # load configuration
    config = load_config()
    input_dir = config['input_dir']
    # Create an empty list to store the session notes
    session_notes = []
    p = re.compile(r'\s+')
    # Loop through the files in the input directory
    for file_name in os.listdir(input_dir):
        # Check if the file is a PDF file
        if file_name.endswith(".pdf"):
            # Create the file path
            file_path = os.path.join(input_dir, file_name)
            # Open the PDF file
            pdf = fitz.open(file_path)
            # Extract the text from the first page
            note_text = pdf[0].get_text()
            # Strip the whitespace from the text
            note_text = note_text.strip()
            # Close the PDF file
            pdf.close()
            # Create a session note object
            session_note = SessionNote(
                file_name=file_name,
                file_path=file_path,
                note_text=note_text
            )

            # filter out white space and new lines 
            session_note.note_text = re.sub(p,'',session_note.note_text)
            session_note_text = session_note.note_text
            session_note_text = session_note_text.replace("\n", " ")
            session_note.note_text = session_note_text
            # Append the session note object to the list
            session_notes.append(session_note)
    # Return the list of session notes
    return session_notes

def main():

    # get session note contents
    session_notes = extract_session_notes()

    for session_note in session_notes:
        print("file name: "+session_note.file_name+"\n")
        print("session note: "+session_note.note_text+"#####\n")

        session_note_text = session_note.note_text
        o_ai_client=get_ai_client()
        ai_response = runPrompt(o_ai_client,session_note_text)
        print(ai_response)

main()
