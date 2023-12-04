Therapy Note Processor

This is a python script that automates a set of document processing tasks for therapy notes. It uses PyMuPDF to extract therapy notes from pdf files in an input directory, strip white space from the extracted note, and then use the Azure OpenAI Service to send an initial and then a session prompt containing the session note for analysis and the generation of the email and SOAP documents which will be written to an output directory. All configurations and AI prompts are in one yaml file called “therapy_notes_processor.yaml”.

Requirements

Python 3.6 or higher
PyMuPDF
requests
An Azure OpenAI service account and key

Usage

To run the script, use the following command:

python therapyNoteProcessor.py [service_account_file]

where service_account_file is the path to the service account file for the Azure OpenAI service.

To see the usage message, use the following command:
python therapyNoteProcessor.py --usage

Configuration

The script requires a configuration file named “therapy_notes_processor.yaml” in the same directory as the script. The configuration file should contain the following variables:

log_file: The name of the log file for the script
input_dir: The path to the input directory where the therapy note pdf files are stored
output_dir: The path to the output directory where the email and SOAP documents will be written
azure_endpoint: The endpoint URL for the Azure OpenAI service
system_prompt: The system prompt for activating the latent language model knowledge domains needed to process the therapy notes
session_prompt: The session prompt for submitting the session note and the processing instructions to the Azure OpenAI service
