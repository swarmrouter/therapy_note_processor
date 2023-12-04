# Import the required modules
import sys
import os
import yaml
import logging
import PyMuPDF
import requests

# Load the configuration file
with open("therapy_notes_processor.yaml", "r") as f:
    config = yaml.safe_load(f)

# Set up the logging
logging.basicConfig(filename=config["log_file"], level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("Starting the therapy note processor script")

# Define the input and output directories
input_dir = config["input_dir"]
output_dir = config["output_dir"]

# Define the Azure OpenAI service endpoint and key
azure_endpoint = config["azure_endpoint"]
azure_key = config["azure_key"]

# Define the system prompt and the session prompt
system_prompt = config["system_prompt"]
session_prompt = config["session_prompt"]

# Define the class for the therapy note object
class TherapyNote:
    # Initialize the object with the file name and the file path
    def __init__(self, file_name, file_path):
        self.file_name = file_name
        self.file_path = file_path
        self.session_note = None
        self.email_doc = None
        self.soap_doc = None

    # Define the method to extract the session note from the pdf file
    def extract_session_note(self):
        logging.info(f"Extracting session note from {self.file_name}")
        # Create a pdf document object to read the pdf file
        pdf_doc = PyMuPDF.open(self.file_path)
        # Initialize an empty string to store the extracted text
        extracted_text = ""
        # Loop through the pages in the pdf file
        for page in pdf_doc:
            # Extract the text from the page and append it to the extracted text
            extracted_text += page.getText()
        # Strip the white space from the extracted text
        extracted_text = extracted_text.strip()
        # Assign the extracted text to the session note attribute
        self.session_note = extracted_text
        logging.info(f"Session note extracted from {self.file_name}")

    # Define the method to process the session note using the Azure OpenAI service
    def process_session_note(self):
        logging.info(f"Processing session note from {self.file_name}")
        # Create a header for the Azure OpenAI service request
        header = {
            "Ocp-Apim-Subscription-Key": azure_key,
            "Content-Type": "application/json"
        }
        # Create a payload for the Azure OpenAI service request
        payload = {
            "system_prompt": system_prompt,
            "session_prompt": session_prompt,
            "session_note": self.session_note
        }
        # Send a post request to the Azure OpenAI service endpoint with the header and the payload
        response = requests.post(azure_endpoint, headers=header, json=payload)
        # Check if the response status code is 200
        if response.status_code == 200:
            # Get the email document and the soap document from the response json
            self.email_doc = response.json()["email_doc"]
            self.soap_doc = response.json()["soap_doc"]
        else:
            # Log the error message from the response
            logging.error(response.json()["error_message"])
        logging.info(f"Session note processed from {self.file_name}")

    # Define the method to write the email document and the soap document to the output file
    def write_output_file(self):
        logging.info(f"Writing output file for {self.file_name}")
        # Get the output file name by replacing the pdf extension with the tsoap extension
        output_file_name = self.file_name.replace(".pdf", ".tsoap")
        # Get the output file path by joining the output directory and the output file name
        output_file_path = os.path.join(output_dir, output_file_name)
        # Create a file object to write the email document and the soap document
        file_obj = open(output_file_path, "w")
        # Write the email document and the soap document to the file object
        file_obj.write(self.email_doc + "\n\n" + self.soap_doc)
        # Close the file object
        file_obj.close()
        logging.info(f"Output file written for {self.file_name}")

# Define the function to get the list of therapy note files from the input directory
def get_therapy_note_files():
    logging.info("Getting the list of therapy note files from the input directory")
    # Initialize an empty list to store the therapy note objects
    therapy_note_list = []
    # Loop through the files in the input directory
    for file in os.listdir(input_dir):
        # Check if the file has the pdf extension
        if file.endswith(".pdf"):
            # Get the file name and the file path
            file_name = file
            file_path = os.path.join(input_dir, file)
            # Create a therapy note object with the file name and the file path
            therapy_note = TherapyNote(file_name, file_path)
            # Append the therapy note object to the therapy note list
            therapy_note_list.append(therapy_note)
    # Return the therapy note list
    return therapy_note_list

# Define the main function to run the script
def main():
    # Get the list of therapy note files from the input directory
    therapy_note_list = get_therapy_note_files()
    # Loop through the therapy note list
    for therapy_note in therapy_note_list:
        # Extract the session note from the pdf file
        therapy_note.extract_session_note()
        # Process the session note using the Azure OpenAI service
        therapy_note.process_session_note()
        # Write the email document and the soap document to the output file
        therapy_note.write_output_file()
    # Log the completion of the script
    logging.info("Therapy note processor script completed")

# Run the main function if the script is executed
if __name__ == "__main__":
    # Check if the --usage argument is passed
    if len(sys.argv) > 1 and sys.argv[1] == "--usage":
        # Print the usage message
        print("Usage: python therapyNoteProcessor.py [service_account_file]")
        print("service_account_file: The path to the service account file for the Azure OpenAI service")
    else:
        # Run the main function
        main()

