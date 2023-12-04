#!/usr/bin/python3

import yaml

yaml_file = "therapy_note_processor.yaml"

# Load the yaml file and read the prompt
with open(yaml_file) as f:
    data = yaml.safe_load(f)
    system_prompt = data["SYSTEM_PROMPT"]

print(system_prompt)

# Create an instance of the Azure OpenAI client
#client = azure_openai.OpenAIClient(subscription_key="your_subscription_key")

# Set the model to use
#model = "gpt-4"

# Set the parameters for the completion request
#parameters = {
#    "max_tokens": 100,
#    "temperature": 0.9,
#    "frequency_penalty": 0.1,
#    "presence_penalty": 0.6,
#    "stop": ["\n"]
#}

# Send the prompt to the Azure OpenAI Service and get the completion
#completion = client.complete(model, prompt, parameters)

# Print the completion
#print(completion)
