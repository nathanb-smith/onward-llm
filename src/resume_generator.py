import os
from openai import AzureOpenAI
from pathlib import Path
from dotenv import load_dotenv
from readers import extract_text_from_pdf, extract_text_from_txt
from writers import save_to_word

load_dotenv()

# --- Configuration ---
# Ensure the environment variables are set (see Prerequisites above)
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME") # Replace with your model deployment name (e.g., "gpt-35-turbo")

if not all([AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, DEPLOYMENT_NAME]):
    print("Error: Required environment variables or deployment name not set.")
    exit()

# --- Initialize the Azure OpenAI Client ---
client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    api_version="2025-04-01-preview" # Use a compatible API version
)

def resume_generator():
    """Reads a file and sends it to Azure AI for initial analysis."""
    rif = extract_text_from_pdf(Path.cwd()/"input_files/RIF.pdf")
    notes = extract_text_from_txt(Path.cwd()/"input_files/notes.txt")
    try:
        # Load the file content
        transcript = extract_text_from_txt(Path.cwd()/"input_files/transcript.txt")
        
        # Create a specialized prompt for analysis
        analysis_request = f"Please create a resume in an optimized Microsoft Word format from the provided information form, transcript, and interview notes. The summary should include 1-3 detailed bullet points for each of the following sections: Skills, Experience, Education, and Projects (if applicable):\n\n{rif}\n\nTranscript:\n\n{transcript}\n\nManager's notes:\n{notes}"
        conversation_history = []
        # Add the file content to history as a user message
        conversation_history.append({"role": "user", "content": analysis_request})
        
        # Call Azure OpenAI API
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=conversation_history,
            max_completion_tokens=30000, # Increased for analysis
        )
        
        assistant_message = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": assistant_message})
        mk = conversation_history[-1]["content"]        
        # Save the assistant message to a Word document
        output_path = Path.cwd() / "resume_files/resume.docx"
        save_to_word(mk, output_path)
        
    except FileNotFoundError:
        print(f"Error: The file '{Path.cwd()/'input_files/transcript.txt'}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
    print("Resume generation complete!")