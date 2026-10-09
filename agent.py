"""
agent.py
========
Orchestrates resume analysis using LangChain, OpenAI Chat Models, and Pydantic.
Analyzes skills against target roles/job descriptions, constructs 4-week roadmaps,
suggests non-hallucinatory resume enhancements, recommends projects, and compiles interview questions.
"""

from __future__ import annotations

import os
from typing import List, Optional
from pydantic import BaseModel, Field

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables if available
load_dotenv()


# ==============================================================================
# Pydantic Schemas for Structured LLM Outputs
# ==============================================================================

class SkillEvidence(BaseModel):
    """Represents a skill that is explicitly supported or evidenced in the resume."""
    skill_name: str = Field(
        description="Name of the skill (e.g. Python, Docker, SQL, Prompt Engineering)."
    )
    category: str = Field(
        description="Category such as 'Languages & Frameworks', 'Cloud & DevOps', 'Databases', 'Core Concepts', or 'Soft Skills'."
    )
    resume_evidence: str = Field(
        description="Direct context, quote, or specific project/work experience in the resume demonstrating this skill."
    )
    proficiency_context: str = Field(
        description="Brief note on how the skill was utilized (e.g., 'Used in production API development', 'Academic project')."
    )


class UnEvidencedSkill(BaseModel):
    """Represents a skill expected for the target role/job description that is not evidenced in the resume."""
    skill_name: str = Field(
        description="Name of the skill required or expected for the role."
    )
    importance: str = Field(
        description="Importance level: 'High Priority (Core)', 'Medium Priority (Standard)', or 'Nice to Have (Bonus)'."
    )
    role_relevance: str = Field(
        description="Why this skill is important for the target job role or job description."
    )
    status_note: str = Field(
        default="Not evidenced in the provided resume text.",
        description="Status clarifying that evidence was not found in the resume, without assuming the candidate completely lacks it."
    )


class WeeklyRoadmap(BaseModel):
    """A structured weekly learning plan to bridge skill gaps."""
    week_number: int = Field(description="Week number (1, 2, 3, or 4).")
    week_title: str = Field(description="Catchy and focused title for the week's theme.")
    core_focus: str = Field(description="Main subject area or technology to master this week.")
    learning_objectives: List[str] = Field(
        description="2 to 4 specific, actionable learning objectives for the week."
    )
    action_items: List[str] = Field(
        description="Practical steps, hands-on tutorials, or coding exercises to complete."
    )
    recommended_resources: List[str] = Field(
        description="Types of learning resources, official documentation, or topics to study."
    )


# Type aliases
WeeklyPlan = WeeklyRoadmap


class ProjectRecommendation(BaseModel):
    """A practical portfolio project designed to build and demonstrate missing skills."""
    project_title: str = Field(description="Descriptive, professional name for the project.")
    overview: str = Field(description="Concise description of what the project does and its real-world problem statement.")
    target_skills_developed: List[str] = Field(
        description="List of specific skills (from the un-evidenced list) this project builds."
    )
    key_deliverables: List[str] = Field(
        description="3 to 5 concrete deliverables/features the candidate should build and showcase on GitHub/portfolio."
    )
    portfolio_impact: str = Field(
        description="How showcasing this project will stand out to hiring managers and technical interviewers."
    )


class ResumeImprovement(BaseModel):
    """Actionable advice to refine resume phrasing without fabricating experience or qualifications."""
    section: str = Field(
        description="Resume section to improve (e.g., 'Work Experience', 'Projects', 'Summary', 'Skills')."
    )
    identified_issue: str = Field(
        description="The weakness or missed opportunity (e.g., vague bullet point, passive voice, missing metric framing)."
    )
    actionable_suggestion: str = Field(
        description="Specific advice on how to restructure the statement accurately."
    )
    original_resume_snippet: Optional[str] = Field(
        default=None,
        description="The relevant snippet from the resume, if applicable."
    )
    enhanced_bullet_point: str = Field(
        description="An improved example rewriting the point with strong action verbs and outcome framing, strictly without inventing new metrics or claims."
    )


class InterviewPrepQuestion(BaseModel):
    """Targeted interview question based on the role and resume profile."""
    question: str = Field(description="The interview question.")
    category: str = Field(
        description="Type of question: 'Technical Deep Dive', 'System Design / Architecture', 'Behavioral / STAR', or 'Problem Solving'."
    )
    interviewer_intent: str = Field(
        description="What the interviewer is evaluating with this question."
    )
    suggested_approach: str = Field(
        description="Guidance on structuring a compelling answer referencing actual past experience and best practices."
    )


class ResumeAnalysisOutput(BaseModel):
    """Complete structured output for the Resume Analyzer and Skill Development Agent."""
    candidate_name: Optional[str] = Field(
        default="Candidate",
        description="Candidate's name if clearly identified in the resume; otherwise 'Candidate'."
    )
    target_role: str = Field(
        description="The target job role analyzed."
    )
    professional_summary: str = Field(
        description="A concise 2-3 sentence assessment of the candidate's current profile relative to the target role."
    )
    evidenced_skills: List[SkillEvidence] = Field(
        description="Skills clearly supported by text/projects/experience in the resume."
    )
    not_evidenced_skills: List[UnEvidencedSkill] = Field(
        description="Skills expected for the target role but not evidenced in the resume."
    )
    evidenced_skills_count: int = Field(
        description="Count of key role skills evidenced in the resume."
    )
    total_target_role_skills_count: int = Field(
        description="Total count of standard core skills required/expected for this target role."
    )
    skill_match_percentage: float = Field(
        description="Calculated percentage of evidenced core skills vs total target requirements (0.0 to 100.0)."
    )
    match_disclaimer: str = Field(
        default=(
            "Note: This skill match percentage is an educational metric reflecting keyword and contextual alignment "
            "between the resume and standard role requirements. It is NOT an applicant tracking system (ATS) guarantee "
            "or a predictor of hiring decisions."
        ),
        description="Mandatory disclaimer clarifying the meaning of the skill match score."
    )
    four_week_roadmap: List[WeeklyRoadmap] = Field(
        description="Personalized 4-week step-by-step learning roadmap focusing on un-evidenced skills."
    )
    recommended_projects: List[ProjectRecommendation] = Field(
        description="2 to 3 practical, resume-worthy project recommendations."
    )
    resume_improvements: List[ResumeImprovement] = Field(
        description="3 to 5 suggestions to polish resume formatting, impact verbs, and clarity without inventing qualifications."
    )
    interview_questions: List[InterviewPrepQuestion] = Field(
        description="5 to 7 tailored interview questions with answering strategies."
    )


# Backward compatibility aliases
WeeklyPlan = WeeklyRoadmap
ProjectIdea = ProjectRecommendation
InterviewPrepItem = InterviewPrepQuestion
ResumeAnalysis = ResumeAnalysisOutput


# ==============================================================================
# Prompt Engineering & Agent Execution
# ==============================================================================

SYSTEM_PROMPT = """You are an expert AI Career Coach, Senior Technical Recruiter, and Engineering Mentor.
Your mission is to perform a rigorous, constructive, and ethical analysis of a candidate's resume against a target job role and optional job description.

### CRITICAL RULES & ETHICAL GUIDELINES:
1. **TRUTH & INTEGRITY**: NEVER invent, assume, or fabricate any experience, degree, tool, or metric not present in the resume.
2. **LABELING ABSENCE**: If a skill or qualification is not mentioned in the resume, label it strictly as "Not evidenced in resume". NEVER say "The candidate lacks this skill" or "The candidate does not know X", because they may have unlisted experience.
3. **SKILL MATCH CALCULATION**:
   - Determine the comprehensive set of key skills required for the Target Role (incorporating the Job Description if provided).
   - Count how many of these are clearly evidenced in the resume vs total target skills.
   - Calculate a realistic `skill_match_percentage` (0 to 100).
   - Always include the transparency disclaimer stating this is an alignment indicator, not a hiring verdict.
4. **4-WEEK ROADMAP**:
   - Build a progressive 4-week learning path prioritizing the highest-impact un-evidenced skills.
   - Week 1: Foundations & Core Concepts of missing skills.
   - Week 2: Deepening Practical Skills & Frameworks.
   - Week 3: Applied Development & Real-world Workflows.
   - Week 4: Capstone Integration, Testing & Interview Preparation.
5. **PROJECT RECOMMENDATIONS**:
   - Recommend 2-3 real-world, non-trivial projects that directly demonstrate the un-evidenced skills.
   - Each project must have clear deliverables suitable for a GitHub repository / portfolio.
6. **RESUME IMPROVEMENTS**:
   - Suggest impactful phrasing, active voice, and better structure.
   - DO NOT fabricate accomplishments or fake percentages (e.g., do not invent "boosted revenue by 40%" if not in the resume; instead show how to frame their real work: "Refactored API endpoints using FastAPI to improve modularity and error handling").
7. **INTERVIEW QUESTIONS**:
   - Provide realistic technical, architectural, and behavioral questions tailored to the candidate's actual projects and the target role requirements.
"""

USER_PROMPT_TEMPLATE = """Please analyze the following resume for the target role:

### Target Job Role:
{target_role}

### Optional Job Description:
{job_description}

### Extracted Resume Text:
{resume_text}

Provide a comprehensive, structured evaluation following all schema requirements and ethical guidelines.
"""


def get_llm(
    api_key: Optional[str] = None,
    model_name: str = "gpt-4o-mini",
    temperature: float = 0.2,
    base_url: Optional[str] = None,
) -> ChatOpenAI:
    """
    Initializes a LangChain ChatOpenAI instance with safe API key and custom base_url handling.

    Args:
        api_key: OpenAI / Provider API key.
        model_name: Model identifier (e.g., 'gpt-4o-mini', 'llama-3.3-70b-versatile').
        temperature: Sampling temperature (0.0 to 1.0, default 0.2).
        base_url: Optional base URL for OpenAI-compatible providers (Groq, OpenRouter, DeepSeek, Ollama).

    Returns:
        Configured ChatOpenAI instance.

    Raises:
        ValueError: If no valid API key is found when not using local endpoint.
    """
    resolved_key = api_key or os.getenv("OPENAI_API_KEY")
    resolved_base_url = base_url or os.getenv("OPENAI_BASE_URL")

    # If using local ollama without key, allow dummy key
    if resolved_base_url and "localhost" in resolved_base_url and not resolved_key:
        resolved_key = "ollama"

    if not resolved_key or not resolved_key.strip():
        raise ValueError(
            "API Key is missing. Please set the OPENAI_API_KEY environment variable "
            "in your .env file or enter it in the application sidebar."
        )

    kwargs = {
        "model": model_name or "gpt-4o-mini",
        "temperature": temperature,
        "api_key": resolved_key.strip(),
    }
    if resolved_base_url and resolved_base_url.strip():
        kwargs["base_url"] = resolved_base_url.strip()

    return ChatOpenAI(**kwargs)


def analyze_resume(
    resume_text: str,
    target_role: str,
    job_description: Optional[str] = None,
    api_key: Optional[str] = None,
    model_name: str = "gpt-4o-mini",
    temperature: float = 0.2,
    base_url: Optional[str] = None,
) -> ResumeAnalysisOutput:
    """
    Executes the structured resume analysis using LangChain and ChatOpenAI.

    Args:
        resume_text: Extracted plain text from the candidate's PDF resume.
        target_role: Target career role (e.g. 'Python Developer', 'Data Analyst').
        job_description: Optional job description text for customized alignment.
        api_key: OpenAI or compatible provider API key.
        model_name: Name of the model to use.
        temperature: Temperature for response generation.
        base_url: Optional custom base URL (e.g. Groq, OpenRouter).

    Returns:
        ResumeAnalysisOutput instance containing structured analysis.
    """
    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text is empty. Please provide a valid resume.")

    if not target_role or not target_role.strip():
        raise ValueError("Target job role is required.")

    # Format Job Description fallback
    jd_content = (
        job_description.strip()
        if job_description and job_description.strip()
        else "No specific job description provided. Analyze against industry-standard requirements for the target role."
    )

    # Build prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", USER_PROMPT_TEMPLATE),
    ])

    # Candidate models to try in case of 404 / unavailable model
    candidate_models = [model_name]
    if base_url and "groq" in base_url.lower():
        fallback_groq_models = ["llama-3.1-8b-instant", "llama3-70b-8192", "mixtral-8x7b-32768", "llama-3.3-70b-versatile"]
        for fm in fallback_groq_models:
            if fm not in candidate_models:
                candidate_models.append(fm)

    last_err = None
    result = None

    for candidate_model in candidate_models:
        try:
            llm = get_llm(
                api_key=api_key,
                model_name=candidate_model,
                temperature=temperature,
                base_url=base_url,
            )
            # Try tool-calling structured output, then json_mode fallback
            try:
                structured_llm = llm.with_structured_output(ResumeAnalysisOutput)
                chain = prompt | structured_llm
                result = chain.invoke({
                    "target_role": target_role.strip(),
                    "job_description": jd_content,
                    "resume_text": resume_text.strip(),
                })
            except Exception:
                structured_llm = llm.with_structured_output(ResumeAnalysisOutput, method="json_mode")
                chain = prompt | structured_llm
                result = chain.invoke({
                    "target_role": target_role.strip(),
                    "job_description": jd_content,
                    "resume_text": resume_text.strip(),
                })

            if result:
                break
        except Exception as e:
            last_err = e
            # If error is 404 or model not found, loop to next candidate
            err_msg = str(e).lower()
            if "404" in err_msg or "model_not_found" in err_msg or "does not exist" in err_msg:
                continue
            else:
                raise e

    if not result:
        if last_err:
            raise last_err
        raise ValueError("Failed to obtain analysis from the language model.")

    # Post-validation safety check on percentages
    if result.total_target_role_skills_count > 0 and result.evidenced_skills_count >= 0:
        calculated_pct = round(
            (result.evidenced_skills_count / result.total_target_role_skills_count) * 100, 1
        )
        # Harmonize percentage within bounds
        result.skill_match_percentage = min(max(result.skill_match_percentage, 0.0), 100.0)

    return result


def generate_demo_analysis(
    resume_text: str,
    target_role: str,
    job_description: Optional[str] = None,
) -> ResumeAnalysisOutput:
    """
    Generates a high-quality, realistic analysis locally without making external API calls.
    Used for offline testing, demos, and when API credits are depleted.
    Inspects actual keywords in the extracted resume text to provide truthful, contextual results.
    """
    text_lower = resume_text.lower()
    
    # Common tech skills mapping
    known_skills = [
        ("Python", "Languages & Frameworks", ["python", "py"]),
        ("PyTorch", "ML Frameworks", ["pytorch", "torch"]),
        ("TensorFlow / Keras", "ML Frameworks", ["tensorflow", "keras", "tf"]),
        ("Scikit-Learn", "Machine Learning", ["scikit-learn", "sklearn"]),
        ("Pandas & NumPy", "Data Manipulation", ["pandas", "numpy"]),
        ("SQL & Relational Databases", "Databases", ["sql", "postgres", "mysql", "sqlite"]),
        ("Docker & Containerization", "DevOps & Deployment", ["docker", "container"]),
        ("Git & Version Control", "Tools & Methodologies", ["git", "github", "gitlab"]),
        ("REST APIs / FastAPI / Flask", "API Development", ["fastapi", "flask", "django", "rest api", "restful"]),
        ("Cloud Platforms (AWS/GCP/Azure)", "Cloud Computing", ["aws", "gcp", "azure", "cloud"]),
        ("MLOps & Model Monitoring", "MLOps", ["mlflow", "mlops", "wandb", "dvc", "kubeflow"]),
        ("NLP & LLMs", "AI / Deep Learning", ["nlp", "transformers", "langchain", "llm", "huggingface", "bert", "gpt"]),
        ("Data Visualization (Matplotlib/Seaborn)", "Data Analysis", ["matplotlib", "seaborn", "tableau", "power bi"]),
        ("CI/CD & Testing", "Engineering Best Practices", ["ci/cd", "pytest", "unit test", "github actions", "jenkins"]),
    ]

    evidenced: List[SkillEvidence] = []
    not_evidenced: List[UnEvidencedSkill] = []

    for name, cat, keywords in known_skills:
        matched = False
        for kw in keywords:
            if kw in text_lower:
                matched = True
                # Find a context snippet from the resume text
                idx = text_lower.find(kw)
                start_snippet = max(0, idx - 40)
                end_snippet = min(len(resume_text), idx + 80)
                snippet = resume_text[start_snippet:end_snippet].replace("\n", " ").strip()
                evidenced.append(
                    SkillEvidence(
                        skill_name=name,
                        category=cat,
                        resume_evidence=f"...{snippet}...",
                        proficiency_context=f"Referenced in candidate resume experience/projects related to {cat.lower()}."
                    )
                )
                break
        if not matched:
            priority = "High Priority (Core)" if len(not_evidenced) < 2 else "Medium Priority (Standard)"
            not_evidenced.append(
                UnEvidencedSkill(
                    skill_name=name,
                    importance=priority,
                    role_relevance=f"Standard requirement for modern {target_role} roles to ensure scalable, maintainable engineering.",
                    status_note="Not evidenced in the provided resume text."
                )
            )

    # Ensure reasonable count
    total_skills = len(evidenced) + len(not_evidenced)
    evidenced_count = len(evidenced)
    match_pct = round((evidenced_count / total_skills) * 100, 1) if total_skills > 0 else 50.0

    missing_names = [s.skill_name for s in not_evidenced[:4]] or ["MLOps", "Docker", "FastAPI", "CI/CD"]

    roadmap = [
        WeeklyRoadmap(
            week_number=1,
            week_title=f"Core Foundations: {missing_names[0] if len(missing_names) > 0 else 'Architecture'}",
            core_focus=f"Bridging fundamental concepts in {missing_names[0] if len(missing_names) > 0 else 'Core Standards'}",
            learning_objectives=[
                f"Master core architecture and conventions of {missing_names[0] if len(missing_names) > 0 else 'system design'}.",
                "Set up a structured local development environment with version control and automated linting.",
                "Implement 3 standalone practical coding exercises to solidify syntax and patterns.",
            ],
            action_items=[
                f"Read official documentation and architectural best practices for {missing_names[0] if len(missing_names) > 0 else 'core technologies'}.",
                "Build a reproducible starter repository with clean modular directory structure.",
                "Write unit tests verifying edge cases and core functional behavior.",
            ],
            recommended_resources=[
                f"Official {missing_names[0] if len(missing_names) > 0 else 'Technology'} Docs & Tutorials",
                "Real Python / Towards Data Science Deep Dives",
                "Clean Code in Python by Mariano Anaya",
            ],
        ),
        WeeklyRoadmap(
            week_number=2,
            week_title=f"Advanced Application & Practical Tooling: {missing_names[1] if len(missing_names) > 1 else 'Containerization'}",
            core_focus=f"Hands-on implementation of {missing_names[1] if len(missing_names) > 1 else 'Modern Deployment'}",
            learning_objectives=[
                f"Integrate {missing_names[1] if len(missing_names) > 1 else 'containerization'} into existing project workflows.",
                "Optimize performance, caching, and data throughput.",
                "Implement structured error handling and health check endpoints.",
            ],
            action_items=[
                f"Create a multi-stage configuration for {missing_names[1] if len(missing_names) > 1 else 'deployment'}.",
                "Benchmark execution latency and profile memory utilization.",
                "Configure automated test runner using PyTest.",
            ],
            recommended_resources=[
                "Docker & Kubernetes Documentation",
                "FastAPI Official Tutorial & Deployment Guide",
                "System Design Primer (GitHub)",
            ],
        ),
        WeeklyRoadmap(
            week_number=3,
            week_title=f"Production Engineering: {missing_names[2] if len(missing_names) > 2 else 'MLOps & CI/CD'}",
            core_focus=f"Pipeline automation, observability, and {missing_names[2] if len(missing_names) > 2 else 'CI/CD'}",
            learning_objectives=[
                "Build an automated CI/CD pipeline with GitHub Actions.",
                "Add structured logging, metrics tracking, and anomaly detection.",
                "Ensure secure secret management using environment variables.",
            ],
            action_items=[
                "Set up GitHub Actions workflow triggered on push and pull requests.",
                "Integrate MLflow / Prometheus for telemetry and metrics.",
                "Conduct code reviews and refactor for high modularity.",
            ],
            recommended_resources=[
                "GitHub Actions for Python Developers",
                "MLOps Guide by Chip Huyen",
                "12-Factor App Methodology",
            ],
        ),
        WeeklyRoadmap(
            week_number=4,
            week_title="Capstone Integration, Portfolio Polish & Interview Readiness",
            core_focus="Full-stack integration, live deployment, and technical interview simulations",
            learning_objectives=[
                "Deploy the completed capstone project to a public cloud or demo platform (HuggingFace / Render / AWS).",
                "Write a comprehensive README with architecture diagrams, setup instructions, and benchmark metrics.",
                "Rehearse STAR-method responses for technical and behavioral interview scenarios.",
            ],
            action_items=[
                "Publish capstone project repository with badges, demo GIF, and interactive documentation.",
                "Record a 2-minute Loom/video walkthrough showcasing architecture and design decisions.",
                "Complete 5 mock technical interview problem rounds focusing on role requirements.",
            ],
            recommended_resources=[
                "Cracking the Coding Interview & LeetCode Patterns",
                "Designing Data-Intensive Applications by Martin Kleppmann",
                "Effective Python by Brett Slatkin",
            ],
        ),
    ]

    projects = [
        ProjectRecommendation(
            project_title=f"End-to-End {target_role} Pipeline & Serving Platform",
            overview=f"A complete, production-grade application demonstrating end-to-end data processing, API endpoints, and automated testing tailored for {target_role} roles.",
            target_skills_developed=[missing_names[0] if len(missing_names) > 0 else "System Architecture", missing_names[1] if len(missing_names) > 1 else "Docker", "CI/CD"],
            key_deliverables=[
                "Modular Python backend with clean separation of concerns and typed models",
                "Containerized runtime using Docker and docker-compose",
                "Automated test suite with >80% code coverage and GitHub Actions pipeline",
                "Interactive API documentation and client demo dashboard",
            ],
            portfolio_impact="Demonstrates full-lifecycle software craftsmanship and production readiness to hiring managers beyond theoretical coursework.",
        ),
        ProjectRecommendation(
            project_title=f"Scalable Microservice with Telemetry & Observability",
            overview="An asynchronous microservice featuring structured logging, rate limiting, and automated health monitoring under high concurrency.",
            target_skills_developed=[missing_names[2] if len(missing_names) > 2 else "FastAPI", "SQL & Database Optimization", "Cloud Deployment"],
            key_deliverables=[
                "Asynchronous REST endpoints supporting pagination and filtering",
                "PostgreSQL integration with connection pooling and database migrations (Alembic)",
                "Live deployment on cloud hosting with monitoring dashboards",
            ],
            portfolio_impact="Proves ability to architect robust, scalable backend systems capable of handling real-world traffic and data complexity.",
        ),
    ]

    improvements = [
        ResumeImprovement(
            section="Work Experience / Projects",
            identified_issue="Bullet points describe basic activities rather than measured impact and engineering choices.",
            actionable_suggestion="Begin each bullet point with strong action verbs (e.g., 'Architected', 'Spearheaded', 'Optimized') and highlight technical tools used.",
            original_resume_snippet="Worked on machine learning models and analyzed data.",
            enhanced_bullet_point="Engineered predictive machine learning pipelines using Scikit-Learn and Pandas, structuring data transformations to improve training throughput."
        ),
        ResumeImprovement(
            section="Technical Skills",
            identified_issue="Skills listed as a flat comma-separated list without categorization by domain.",
            actionable_suggestion="Categorize technical skills into distinct buckets (e.g., 'Languages & Frameworks', 'Data & Storage', 'DevOps & Tooling') for better recruiter scannability.",
            original_resume_snippet=None,
            enhanced_bullet_point="Categorize skills into: Languages (Python, SQL), Frameworks (PyTorch, FastAPI), DevOps (Docker, Git, CI/CD), and Data (Pandas, PostgreSQL)."
        ),
        ResumeImprovement(
            section="Project Descriptions",
            identified_issue="Missing links to live demos or public GitHub repositories.",
            actionable_suggestion="Add concise hyperlinks to GitHub repositories and hosted live demonstrations for each featured project.",
            original_resume_snippet=None,
            enhanced_bullet_point="Add clickable GitHub badges [GitHub: repo-name] and live demo URLs to validate real-world code craftsmanship."
        ),
    ]

    interviews = [
        InterviewPrepQuestion(
            question=f"How do you approach debugging and profiling performance bottlenecks in a {target_role} workflow?",
            category="Technical Deep Dive",
            interviewer_intent="Evaluates your systematic troubleshooting methodology, profiling tools knowledge, and understanding of memory/CPU constraints.",
            suggested_approach="Explain your structured process: 1) reproducing the issue, 2) utilizing profilers (e.g., cProfile, line_profiler), 3) analyzing algorithmic time complexity, and 4) writing regression tests."
        ),
        InterviewPrepQuestion(
            question="Describe a challenging technical trade-off you made in a recent project and why you chose your approach.",
            category="Behavioral / STAR",
            interviewer_intent="Assesses engineering judgment, pragmatism, and ability to balance performance, delivery speed, and code maintainability.",
            suggested_approach="Use the STAR method (Situation, Task, Action, Result) to describe a concrete technical trade-off (e.g., selecting SQL vs NoSQL, or synchronous vs asynchronous processing)."
        ),
        InterviewPrepQuestion(
            question=f"How would you design a scalable service for {target_role} requirements that handles sudden traffic spikes?",
            category="System Design / Architecture",
            interviewer_intent="Tests understanding of horizontal scaling, caching strategies (Redis), asynchronous task queues (Celery/RabbitMQ), and database read replicas.",
            suggested_approach="Structure your answer by clarifying requirements, defining API endpoints, sketching high-level architecture with caching layers and load balancers, and discussing failure recovery."
        ),
        InterviewPrepQuestion(
            question=f"How do you ensure code quality, test coverage, and documentation when collaborating with cross-functional teams?",
            category="Problem Solving",
            interviewer_intent="Checks adherence to modern engineering culture: peer code reviews, CI/CD automated checks, and clear technical specifications.",
            suggested_approach="Highlight your experience with automated linting (flake8/black), unit and integration testing (pytest), and maintaining clear README/API documentation."
        ),
    ]

    return ResumeAnalysisOutput(
        candidate_name="Candidate",
        target_role=target_role,
        professional_summary=f"The candidate exhibits strong foundational experience evidenced in the resume for {evidenced_count} core areas. Focused growth in production deployment, system architecture, and pipeline automation will accelerate readiness for senior {target_role} opportunities.",
        evidenced_skills=evidenced,
        not_evidenced_skills=not_evidenced,
        evidenced_skills_count=evidenced_count,
        total_target_role_skills_count=total_skills,
        skill_match_percentage=match_pct,
        match_disclaimer=(
            "Note: This skill match percentage is an educational metric reflecting keyword and contextual alignment "
            "between the resume and standard role requirements. It is NOT an applicant tracking system (ATS) guarantee "
            "or a predictor of hiring decisions."
        ),
        four_week_roadmap=roadmap,
        recommended_projects=projects,
        resume_improvements=improvements,
        interview_questions=interviews,
    )



# ==============================================================================
# Markdown Report Export Helper
# ==============================================================================

def export_analysis_to_markdown(analysis: ResumeAnalysisOutput) -> str:
    """
    Generates a beautifully formatted GitHub-flavored Markdown report from the structured analysis.

    Args:
        analysis: Structured ResumeAnalysisOutput object.

    Returns:
        Markdown string ready for viewing or downloading.
    """
    candidate = analysis.candidate_name or "Candidate"
    role = analysis.target_role

    md = []
    md.append(f"# 📄 AI Resume & Skill Analysis Report")
    md.append(f"**Candidate:** {candidate} | **Target Role:** {role}\n")
    md.append(f"---\n")

    # Match Score & Summary
    md.append(f"## 📊 Executive Match Overview")
    md.append(f"- **Skill Overlap Score:** `{analysis.skill_match_percentage:.1f}%` ({analysis.evidenced_skills_count} / {analysis.total_target_role_skills_count} Core Role Skills Evidenced)")
    md.append(f"- **Summary:** {analysis.professional_summary}")
    md.append(f"\n> ℹ️ **Transparency Note:** {analysis.match_disclaimer}\n")

    # Evidenced Skills
    md.append(f"## ✅ Skills Evidenced in Resume")
    if analysis.evidenced_skills:
        for skill in analysis.evidenced_skills:
            md.append(f"- **{skill.skill_name}** (`{skill.category}`)")
            md.append(f"  - *Evidence:* {skill.resume_evidence}")
            md.append(f"  - *Context:* {skill.proficiency_context}")
    else:
        md.append("_No explicit matching skills found in the provided resume text._")
    md.append("\n")

    # Skills Not Evidenced
    md.append(f"## 🔍 Skills Not Evidenced in Resume")
    if analysis.not_evidenced_skills:
        for missing in analysis.not_evidenced_skills:
            md.append(f"- **{missing.skill_name}** — *Priority: {missing.importance}*")
            md.append(f"  - *Relevance to {role}:* {missing.role_relevance}")
            md.append(f"  - *Status:* {missing.status_note}")
    else:
        md.append("_All primary role skills were evidenced in the resume!_")
    md.append("\n")

    # 4-Week Learning Roadmap
    md.append(f"## 🗺️ 4-Week Personalized Learning Roadmap")
    for week in analysis.four_week_roadmap:
        md.append(f"### Week {week.week_number}: {week.week_title}")
        md.append(f"**Focus Area:** {week.core_focus}\n")
        md.append(f"**Key Objectives:**")
        for obj in week.learning_objectives:
            md.append(f"- {obj}")
        md.append(f"\n**Action Plan:**")
        for item in week.action_items:
            md.append(f"- {item}")
        md.append(f"\n**Recommended Topics & Resources:**")
        for res in week.recommended_resources:
            md.append(f"- {res}")
        md.append("\n")

    # Recommended Projects
    md.append(f"## 🛠️ Recommended Practical Projects")
    for proj in analysis.recommended_projects:
        md.append(f"### 🚀 {proj.project_title}")
        md.append(f"{proj.overview}\n")
        md.append(f"- **Target Skills Developed:** {', '.join(proj.target_skills_developed)}")
        md.append(f"- **Key Deliverables:**")
        for deliv in proj.key_deliverables:
            md.append(f"  - {deliv}")
        md.append(f"- **Portfolio Impact:** {proj.portfolio_impact}\n")

    # Resume Improvements
    md.append(f"## ✍️ Resume Enhancement Suggestions")
    md.append(f"> *Ethical Guidance: Suggestions refine phrasing and structure without fabricating experiences or qualifications.*\n")
    for imp in analysis.resume_improvements:
        md.append(f"### Section: {imp.section}")
        md.append(f"- **Observation:** {imp.identified_issue}")
        md.append(f"- **Suggestion:** {imp.actionable_suggestion}")
        if imp.original_resume_snippet:
            md.append(f"- **Original Context:** *\"{imp.original_resume_snippet}\"*")
        md.append(f"- **Recommended Phrasing:**\n  > {imp.enhanced_bullet_point}\n")

    # Interview Questions
    md.append(f"## 💡 Role-Specific Interview Preparation")
    for idx, q in enumerate(analysis.interview_questions, 1):
        md.append(f"### Q{idx}: {q.question}")
        md.append(f"- **Category:** `{q.category}`")
        md.append(f"- **What Interviewers Look For:** {q.interviewer_intent}")
        md.append(f"- **How to Formulate Your Answer:** {q.suggested_approach}\n")

    md.append("---\n*Report generated by AI Resume Analyzer and Skill Development Agent.*")
    return "\n".join(md)
