from sentence_transformers import SentenceTransformer
from pathlib import Path
from readers import extract_text_from_docx
import os

def jd_embedder(job_descriptions):
    """Loads a local model and generates embeddings for the resume content."""
    # Define the path to the locally installed model
    local_model_path = os.path.join(os.getcwd(), "all-MiniLM-L6-v2")

    # Load the model from the local directory
    model = SentenceTransformer(local_model_path)

    resume = extract_text_from_docx(Path.cwd()/"resume_files/resume.docx")

    sentences = [resume] + [job_description for job_description in job_descriptions]
    # Generate embeddings
    embeddings = model.encode(sentences)

    # Print the embeddings
    print("JD embedding finished.")
    return embeddings
