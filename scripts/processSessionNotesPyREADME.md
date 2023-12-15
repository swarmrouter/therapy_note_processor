# Therapy Note Processor

This is a Python script that helps therapists process their therapy notes using the SOAP format. It also generates an email document that summarizes the session and provides recommendations for the next steps. The script uses the OpenAI API to generate the documents from the session notes.

## Requirements

- Python 3.6 or higher
- PyMuPDF (fitz)
- openai
- A valid API key for the OpenAI API

## Installation

- Clone this repository or download the zip file
- Install any required modules (run test/test_deps.py)
- Create a YAML file named "[therapy_notes_processor.yaml](https://github.com/swarmrouter/therapy_note_processor/blob/main/config/therapy_note_processor.yaml)" in the same directory as the script and fill in the configuration values (see below for details)
- Create an input directory and an output directory and place the PDF files with the session notes in the input directory

## Configuration

The YAML file "therapy_notes_processor.yaml" contains the following configuration values:

- `api_key`: The API key for the AI service
- `input_dir`: The input directory containing the PDF files with the session notes
- `output_dir`: The output directory where the TSOAP notes will be written
- `system_prompt`: The system prompt for the AI service
- `session_prompt`: The session prompt for the AI service

## Usage

To run the script, use the following command:

`python processSessionNotes.py`

The script will read the session note pdf files from the input directory, extract and process the session note text, send them to the AI service, and generate the TSOAP notes in the output directory
