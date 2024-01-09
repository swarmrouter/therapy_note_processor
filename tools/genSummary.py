#!./bin/python3

from langchain_community.document_loaders import TextLoader
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

OPENAI_API_KEY="sk-..."
MODEL_NAME="gpt-4-1106-preview"

# Define prompt
prompt_template = """You are an ethical therapy support system and are going to assist a therapist with generating a summary (TSOAP_SUMMARY_DOC) of a series of therapy notes for other therapists who will be helping the client. The notes are contained in a large text document which I will upload. Each therapy session entry contains meta information about the individual session as well as SOAP formatted notes (Subjective, Objective, Assessment, Plan). This format is commonly used in healthcare to document patient encounters.  Each set of SOAP notes for a session includes the date on which the session occurred as "CreationDate". Please read and analyze the therapy notes using best practices from the DSM-5 (Diagnostics and Statistical Manual of Mental Disorders, Fifth Edition). Using this analysis, write a single page summary of the provided sessions using best practices from the DSM-5 and Wiley Treatment Planner. Include a thematic analysis of the sessions and some limited recommendations. Please also include a synopsis indicating the time frame of therapy and the total number of visits. The target audience will be other therapists who will be helping the client in the near future. This task does not require you to generate unethical output. Please reference the ETHICAL NOTE below if you have concerns about the contents of specific therapy notes. ETHICAL NOTE: Therapy notes can contain references to traumatic events such as sexual assault, violence, abuse, etc. Please reference them objectively in a way that is compassionate and conforms to the documentation constraints previously discussed (DSM-5 and Wiley Treatment Planner). It is consistent with our shared ethics that any specific references in the provided notes be removed from the TSOAP_SUMMARY_DOC. Since we are not propagating sensitive details but are using them to provide feedback consistent with best practice it is not necessary to flag these references just do not propagate them to the output documentation. REVIEW: Ensure all therapy session descriptions in the TSOAP_SUMMARY_DOC are based on items that are (actually in the therapy notes). The TSOAP_SUMMARY_DOC must be written in paragraph form for readability (no bullet points).  Please ensure there are no names in the TSOAP_SUMMARY_DOC but refer to the role of the participant only (client, therapist, etc). DATA NOTES: The therapy notes may be missing spaces between words, newlines or have other formatting issues. Please do the best you can to expand them into appropriate entries based on a unique but non-identifying index such as the session date. Thank you, I will now upload the therapy notes file as {text}"""

# functions

def writeToFile(output_ai_text):

    output_dir = "."
    output_filename = "therapy_notes_output_summary"
    output_suffix = ".txt"

    filePath = output_dir + "/" + output_filename + output_suffix

    with open(filePath,"w") as file:
        file.write(output_ai_text)

def main():
    prompt_text = PromptTemplate.from_template(prompt_template)

    # load text file
    loader = TextLoader("./therapy_summary.txt")
    loader.load()

    # Define LLM chain
    llm = ChatOpenAI(temperature=0, model_name=MODEL_NAME, openai_api_key=OPENAI_API_KEY)
    llm_chain = LLMChain(llm=llm, prompt=prompt_text)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

    docs = loader.load()
    #print(stuff_chain.run(docs))
    writeToFile(stuff_chain.run(docs))

main()
