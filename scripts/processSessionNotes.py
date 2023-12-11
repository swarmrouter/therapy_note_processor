#!/usr/bin/python3

# Import the required modules
import sys
import os
import yaml
import fitz # PyMuPDF module
from openai import OpenAI # OpenAI API module
from openai import AzureOpenAI # Azure OpenAI Service module

CONFIG_FILE = "./therapy_note_processor.yaml" # The name of the configuration file
SYSTEM_PROMPT = "system_prompt" # The key for the system prompt in the configuration file
SESSION_PROMPT = "session_prompt" # The key for the session prompt in the configuration file

# Define the functions
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
    cfig = load_config()
    apiKey = cfig['api_key']
    o_ai_client=OpenAI(api_key=apiKey)
    return o_ai_client

# Execute ai prompt and return result text
def runPrompt(o_ai_client):
    cfig = load_config()
    systemPrompt = cfig['system_prompt']
    sessionPrompt = cfig['session_prompt']
    completion = o_ai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": sessionPrompt}
        ]
    )
    response = completion.choices[0].message
    return response

def main():
    o_ai_client=get_ai_client()
    ai_response = runPrompt(o_ai_client)
    print(ai_response)

main()
