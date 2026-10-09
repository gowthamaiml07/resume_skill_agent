"""
generate_sample_pdf.py
======================
Generates a realistic sample PDF resume for instant testing of the application.
"""

import pymupdf as fitz

def create_sample_resume():
    doc = fitz.open()
    page = doc.new_page(width=612, height=792)  # Standard Letter size

    resume_text = """ALEX SMITH
alex.smith@example.com | (555) 019-2834 | San Francisco, CA | github.com/alexsmith | linkedin.com/in/alexsmith

PROFESSIONAL SUMMARY
Dynamic and results-driven Software Engineer with 4+ years of experience specializing in Python backend architecture, REST API design, and machine learning workflows. Proven track record of developing high-throughput microservices, optimizing SQL databases, and containerizing distributed applications.

TECHNICAL SKILLS
- Languages: Python (Proficient), SQL, Bash, JavaScript
- Frameworks & Libraries: FastAPI, Flask, PyTorch, Scikit-Learn, Pandas, NumPy, Pydantic
- Databases: PostgreSQL, SQLite, Redis
- DevOps & Tools: Docker, Git, GitHub Actions, AWS (S3, EC2), Linux, PyTest

PROFESSIONAL EXPERIENCE
Senior Backend Engineer | DataCraft Technologies | 2022 – Present
- Architected and deployed 12+ asynchronous RESTful microservices using FastAPI and PostgreSQL, serving over 1.5M monthly requests.
- Integrated predictive machine learning pipelines using Scikit-Learn and Pandas to deliver real-time user behavior analytics.
- Containerized development and staging environments using Docker, cutting developer onboarding time by 45%.
- Implemented automated CI/CD workflows using GitHub Actions and PyTest with 88% unit test coverage.

Python Developer | CloudSphere Innovations | 2020 – 2022
- Developed scalable backend data ingestion endpoints using Flask and Celery task queues.
- Optimized slow SQL relational queries and database indexing, decreasing median API response latency from 420ms to 95ms.
- Built exploratory data analysis notebooks and visualization dashboards using Matplotlib and Pandas.

NOTABLE PROJECTS
Real-Time Stream Sentiment Classifier (GitHub: /alexsmith/stream-sentiment)
- Engineered a streaming NLP pipeline using PyTorch, Redis Streams, and FastAPI to classify live social media streams.
- Packaged complete application with Docker Compose and documented architecture with OpenAPI specifications.

EDUCATION
Bachelor of Science in Computer Science
University of California, Berkeley | Graduated 2020
"""

    rect = fitz.Rect(54, 40, 558, 750)
    page.insert_textbox(rect, resume_text, fontsize=10, fontname="helv", color=(0.1, 0.1, 0.1))
    doc.save("sample_resume.pdf")
    doc.close()
    print("Successfully generated sample_resume.pdf!")

if __name__ == "__main__":
    create_sample_resume()
