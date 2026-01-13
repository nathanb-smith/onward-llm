from resume_generator import resume_generator
from jd_embedder import jd_embedder
from jd_loader import load_jds
from recommendation_agent import recommendation_generator


def main():
    # Run the resume agent to generate the resume
    print("Starting resume generation...")
    resume_generator()
    print("Loading job descriptions...")
    job_descriptions = load_jds()
    # Run the matchmaking agent to generate embeddings
    print("Starting job description embedding...")
    embeddings = jd_embedder(job_descriptions)
    print("Starting recommendation generation...")
    recommendations = recommendation_generator(embeddings)
    print("Process completed! Here are my top three job recommendations in descending order"
          " based on your resume and job descriptions: Job number ", recommendations[0], ", Job number ",
          recommendations[1], ", Job number ", recommendations[2],".")