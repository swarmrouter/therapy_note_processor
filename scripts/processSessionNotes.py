#!/usr/bin/python3

# Import the required modules
import sys
import os
import yaml
import re
import json
import time
import fitz # PyMuPDF module
from openai import OpenAI # OpenAI API module

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

# Execute ai soap prompt and return result text
def runPrompt(o_ai_client,session_note_text):
    # load configuration
    config = load_config()
    systemPrompt = config['system_prompt']
    sessionPrompt = config['session_prompt']
    soap_analysis_model = config['soap_analysis_model']
    sessionPrompt = sessionPrompt + " " + session_note_text
    print("\nSYSTEM_PROMPT: "+systemPrompt+"\n")
    print("\nSESSION_PROMPT: "+sessionPrompt+"\n")
    completion = o_ai_client.chat.completions.create(
        #model="gpt-3.5-turbo",
        model = soap_analysis_model,
        messages=[
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": sessionPrompt}
        ]
    )
    response = completion.choices[0].message
    return response.content

# Execute follow up email generation assistant
def runEmailAssistant(o_ai_client,session):

    config = load_config()
    ai_prompt_p1 = config['assistant_prompt_p1']
    ai_prompt_p2 = config['assistant_prompt_p2']
    ai_prompt_p3 = config['assistant_prompt_p3']
    resource_file_id = config['resource_file_id']
    email_assistant_model = config['email_assistant_model']

    with open("./note_tmp","w") as file:
        file.write(session.note_text)

    notes_file = o_ai_client.files.create(
        file=open("./note_tmp", "rb"),
        purpose='assistants'
    )

    ai_assistant_prompt = ai_prompt_p1 + resource_file_id + ai_prompt_p2 + notes_file.id + ai_prompt_p3

    print("ai assistant prompt: " + ai_assistant_prompt)

    my_assistant = o_ai_client.beta.assistants.create(
            name = "Follow Up Email Assistant",
            instructions = ai_assistant_prompt,
            model = email_assistant_model,
            tools=[{"type": "code_interpreter"}],
            file_ids=[resource_file_id,notes_file.id]
    )

    my_thread = o_ai_client.beta.threads.create(
        messages=[
            {
                "role":"user",
                "content": config['assistant_run_prompt']
            }
        ]
    )

    run = o_ai_client.beta.threads.runs.create(
        thread_id=my_thread.id,
        assistant_id=my_assistant.id
    )

    print(run)
    time.sleep(5)
    while(run.status != "completed"):
        print("Run not completed: " + run.status)
        time.sleep(5)
        run = o_ai_client.beta.threads.runs.retrieve(
            thread_id=run.thread_id,
            run_id=run.id
        )    

        print(run.status)
        print(run)

    messages = o_ai_client.beta.threads.messages.list(
        thread_id = my_thread.id
    )

    print(messages)
    message_text = ""
    for message in messages:
        print("thread: ")
        print(message.content[0].text.value)
        message_text += message.content[0].text.value

    notes_file_delete_status = o_ai_client.beta.assistants.files.delete(
        assistant_id=my_assistant.id,
        file_id=notes_file.id
    )

    # remove tmp note file
    os.unlink("./note_tmp")

    print(notes_file_delete_status)

    assistant_delete_status = o_ai_client.beta.assistants.delete(
        assistant_id=my_assistant.id
    )

    #print("ai_response: " + message_text)
    return message_text


class SessionNote:

    def __init__(self, file_name, file_path, note_text, note_type):
        """Initialize the attributes of a session note."""
        self.file_name = file_name # The name of the file containing the session note
        self.file_path = file_path # The path of the file containing the session note
        self.note_text = note_text # The text of the session note
        self.note_type = note_type # The type of the session note

    def __str__(self):
        """Return a string representation of a session note."""
        return f"Session note from file {self.file_name}:\n{self.note_text}"

    def writeToFile(self,config,output_ai_text):

        output_dir = config['output_dir']
        output_filename = self.file_name
        output_note = self.note_text
        if (self.note_type == 'soap'):
            output_suffix = ".tsoap"
        else:
            output_suffix = ".email"

        filePath = output_dir + "/" + output_filename + output_suffix 
        with open(filePath,"w") as file:
            file.write(output_ai_text)
            file.write("\n\n#############\n\n")
            file.write(output_note)

def extract_session_notes(note_type):
    # load configuration
    config = load_config()
    if (note_type == "email"):
        input_dir = config['input_dir_email']
    else:
        note_type = "soap"
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
                note_text=note_text,
                note_type=note_type
            )

            # filter out white space and new lines 
            session_note.note_text = re.sub(p,'',session_note.note_text)
            session_note_text = session_note.note_text
            session_note_text = session_note_text.replace("\n", " ")
            session_note.note_text = session_note_text
            # Append the session note object to the list
            session_notes.append(session_note)
            # remove the original notes file
            os.unlink(file_path)
    # Return the list of session notes
    return session_notes

def main():

    # get contents of session notes
    session_notes = extract_session_notes("soap")
    session_email_notes = extract_session_notes("email")
    config = load_config()
    o_ai_client=get_ai_client()

    # generate SOAP notes for sessions
    for session_note in session_notes:
        print("file name: "+session_note.file_name+"\n")
        print("session note: "+session_note.note_text+"#####\n")
        print("session note type: "+session_note.note_type+"#####\n")

        session_note_text = session_note.note_text
        ai_response_text = runPrompt(o_ai_client,session_note_text)
        print(ai_response_text)

        session_note.writeToFile(config,ai_response_text)

    # generate resource EMAIL for sessions
    for session_email_note in session_email_notes:
        print("file name: "+session_email_note.file_name+"\n")
        print("session note: "+session_email_note.note_text+"#####\n")
        print("session note type: "+session_email_note.note_type+"#####\n")

        ai_response_text = runEmailAssistant(o_ai_client,session_email_note)
        print(ai_response_text)
        session_email_note.writeToFile(config,ai_response_text)

main()
