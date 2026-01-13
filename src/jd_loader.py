import os
from readers import extract_text_from_docx, extract_text_from_pdf


def load_jds():
    # Directory containing job descriptions
    job_descriptions_dir = os.path.join(os.getcwd(), "job_descriptions")

    # Array to store job descriptions
    job_descriptions = []

    # Iterate through files in the directory
    for file_name in os.listdir(job_descriptions_dir):
        file_path = os.path.join(job_descriptions_dir, file_name)

        # Check file extension and extract text accordingly
        if file_name.endswith(".docx"):
            job_descriptions.append(extract_text_from_docx(file_path))
        elif file_name.endswith(".pdf"):
            job_descriptions.append(extract_text_from_pdf(file_path))
    
    print("Job descriptions loaded.")
    return job_descriptions
