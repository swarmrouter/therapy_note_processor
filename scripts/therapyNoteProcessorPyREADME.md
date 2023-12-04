# Therapy Note Processor

This is a Python script that helps therapists process their therapy notes using the SOAP format. It also generates an email document that summarizes the session and provides recommendations for the next steps. The script uses either the OpenAI API or the Azure OpenAI Service to generate the documents from the session notes.

## Requirements

- Python 3.6 or higher
- PyMuPDF
- openai
- azure-openai
- A valid API key and organization ID for either the OpenAI API or the Azure OpenAI Service

## Installation

- Clone this repository or download the zip file
- Install the required modules using `pip install -r requirements.txt`
- Create a YAML file named "therapy_notes_processor.yaml" in the same directory as the script and fill in the configuration values (see below for details)
- Create an input directory and an output directory and place the PDF files with the session notes in the input directory

## Configuration

The YAML file "therapy_notes_processor.yaml" contains the following configuration values:

- `service`: The type of the AI service (`openai` or `azure`)
- `api_key`: The API key for the AI service
- `org_id`: The organization ID for the AI service (optional for `openai`, required for `azure`)
- `engine`: The engine name for the AI service
- `temperature`: The temperature parameter for the AI service
- `top_p`: The top_p parameter for the AI service
- `frequency_penalty`: The frequency_penalty parameter for the AI service
- `presence_penalty`: The presence_penalty parameter for the AI service
- `max_tokens`: The max_tokens parameter for the AI service
- `stop`: The stop parameter for the AI service
- `input_dir`: The input directory containing the PDF files with the session notes
- `output_dir`: The output directory where the TSOAP notes will be written
- `tsoap_outfile`: The format of the output file name for each session note
- `email_doc`: The format of the email document in the output file
- `soap_doc`: The format of the SOAP document in the output file
- `system_prompt`: The system prompt for the AI service
- `session_prompt`: The session prompt for the AI service

## Usage

To run the script, use the following command:

`python therapyNoteProcessor.py`

The script will read the PDF files from the input directory, extract the session notes, send them to the AI service, and generate the TSOAP notes in the output directory.

To show the usage of the script, use the following command:

`python therapyNoteProcessor.py --usage`
