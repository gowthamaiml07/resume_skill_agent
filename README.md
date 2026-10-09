# 🎯 AI Resume Analyzer and Skill Development Agent

An intelligent, ethical, and privacy-conscious web application that transforms standard PDF resumes into actionable career growth plans. Built using **Python**, **Streamlit**, **PyMuPDF**, and **LangChain** with **OpenAI structured outputs**.

---

## 🌟 Key Features

1. **📄 In-Memory PDF Parsing**: Extracts and validates clean digital text from uploaded PDF resumes using PyMuPDF (`fitz`) without saving files to disk.
2. **🎯 Structured Competency Analysis**: Evaluates resume evidence against target job roles (e.g., *Python Developer*, *Data Analyst*, *Machine Learning Engineer*) and optional custom job descriptions.
3. **🟢 Evidenced vs. Not-Evidenced Skills**: Clearly distinguishes between demonstrated skills and skills marked as *"Not evidenced in resume"* (avoiding unfounded assumptions that a candidate lacks a skill).
4. **📊 Honest Skill-Overlap Metric**: Calculates a realistic skill overlap percentage, accompanied by a clear disclaimer that it is an educational alignment indicator, not a hiring decision.
5. **🗺️ 4-Week Personalized Learning Roadmap**: Delivers a structured week-by-week curriculum with learning objectives, hands-on tasks, and recommended resources to bridge identified skill gaps.
6. **🛠️ Portfolio Project Recommendations**: Suggests real-world, resume-worthy projects designed to build and prove un-evidenced competencies with concrete deliverables.
7. **✍️ Non-Hallucinatory Resume Enhancements**: Suggests impactful phrasing, action verbs, and structure improvements without fabricating qualifications, degrees, or fake metrics.
8. **💡 Tailored Interview Preparation**: Generates role-specific technical, behavioral, and architectural interview questions with answer guidelines.
9. **📥 Markdown Export**: Allows users to download their complete customized analysis and roadmap as a clean `.md` document.

---

## 📂 Project Structure

```text
resume_skill_agent/
│
├── app.py               # Streamlit web application & user interface
├── agent.py             # LangChain agent, Pydantic schemas, and report generator
├── resume_parser.py     # PyMuPDF-based text extraction & error validation
├── requirements.txt     # Python dependencies
├── .env.example         # Template for environment variables
├── .gitignore           # Git ignore rules for secrets and temporary files
└── README.md            # Comprehensive project documentation & guide
```

### Module Breakdown

| File | Purpose |
| :--- | :--- |
| [`app.py`](file:///c:/Users/AIML/Documents/resume_skill_agent/app.py) | Streamlit dashboard with tabs for Match Score, Skills Matrix, 4-Week Roadmap, Projects, Resume Polish, Interview Prep, and Markdown Export. |
| [`agent.py`](file:///c:/Users/AIML/Documents/resume_skill_agent/agent.py) | LangChain chain using `ChatOpenAI.with_structured_output(ResumeAnalysisOutput)` and Pydantic models for safe, type-enforced LLM responses. |
| [`resume_parser.py`](file:///c:/Users/AIML/Documents/resume_skill_agent/resume_parser.py) | Memory-safe PDF text extractor, blank/scanned PDF detector, and document statistics calculator. |
| [`requirements.txt`](file:///c:/Users/AIML/Documents/resume_skill_agent/requirements.txt) | Compatible, modern package versions for Streamlit, LangChain, PyMuPDF, and Pydantic. |
| [`.env.example`](file:///c:/Users/AIML/Documents/resume_skill_agent/.env.example) | Example environment file for `OPENAI_API_KEY` and model configuration. |

---

## 🛠️ Step-by-Step Windows Setup Guide

Follow these exact steps in **Windows Command Prompt (`cmd.exe`)** or **PowerShell**:

### 1. Open Terminal and Navigate to Project Directory

```cmd
cd c:\Users\AIML\Documents\resume_skill_agent
```

### 2. Create a Python Virtual Environment

```cmd
python -m venv venv
```
*(If `python` is not recognized, try `py -m venv venv`)*

### 3. Activate the Virtual Environment

- **In Windows Command Prompt (`cmd.exe`):**
  ```cmd
  venv\Scripts\activate
  ```
- **In PowerShell:**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  *(If you see an execution policy warning in PowerShell, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` first)*

### 4. Upgrade pip and Install Dependencies

```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Your API Key or Select Execution Mode

The app supports 3 execution modes:
- **🟢 OpenAI API (Default):** Set your key in `.env` or paste in sidebar.
  ```env
  OPENAI_API_KEY=sk-proj-yourActualKeyHere
  OPENAI_MODEL=gpt-4o-mini
  ```
- **⚡ Groq / OpenRouter / Custom (Free / Low Cost Tier):** Select in sidebar and input your free Groq/OpenRouter key.
- **🧪 Offline / Demo Mode:** Select in sidebar to test instantly with local keyword matching without needing API credits!

### 6. Launch the Streamlit Application

```cmd
streamlit run app.py
```

The application will open automatically in your default web browser at `http://localhost:8501`.

---

## 🧪 Manual Testing Checklist

| Step | Action | Expected Result |
| :---: | :--- | :--- |
| **1** | Start the app with `streamlit run app.py` | UI loads with clear title, sidebar settings, and upload form. |
| **2** | Select **🧪 Offline / Demo Mode** or use an active API key | Enables testing immediately even if API quota is 0. |
| **3** | Upload a text-based digital PDF resume | PyMuPDF extracts text, showing page count, word count, and text preview. |
| **4** | Enter target role (e.g. "Machine Learning Engineer") | Role is populated and the **🚀 Run Skill Gap Analysis** button becomes active. |
| **5** | Click **Run Skill Gap Analysis** | Generates executive metric cards and structured analysis tabs. |
| **6** | Inspect **Skills Matrix** tab | Evidenced skills show green badges with resume context; un-evidenced skills show yellow badges with importance level. |
| **7** | Inspect **4-Week Roadmap** & **Projects** tabs | Shows a step-by-step weekly plan and portfolio projects targeting un-evidenced skills. |
| **8** | Inspect **Resume Polish** tab | Provides constructive bullet-point upgrades without fabricated numbers or fake credentials. |
| **9** | Click **Download Full Report (.md)** in the Export tab | Generates and downloads a clean Markdown file (`Resume_Analysis_*.md`). |

---

## 🛡️ Privacy & Ethical AI Principles

- **Zero Permanent Storage:** Resumes are processed purely in-memory (`BytesIO`) and discarded immediately.
- **Strict Anti-Hallucination:** System prompts enforce that no qualifications, past titles, or achievements may be invented.
- **Fair Labeling:** Skills absent from the resume are categorized as *"Not evidenced in resume"* rather than assuming candidate incapacity.
- **Transparent Metrics:** Match score is explicitly framed as keyword and evidence overlap, not a hiring guarantee or ATS pass/fail verdict.
