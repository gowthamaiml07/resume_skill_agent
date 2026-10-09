## 📁 Project Structure

```text
resume_skill_agent/
│
├── app.py                      # Main Streamlit application
├── agent.py                    # AI agent and resume analysis logic
├── resume_parser.py            # Extracts text from uploaded PDF resumes
├── config.py                   # Application and API configuration
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Files excluded from Git
│
├── .streamlit/
│   └── secrets.toml.example    # Example configuration for API secrets
│
├── components/
│   ├── __init__.py             # Components package initialization
│   ├── cards.py                # Reusable UI cards
│   ├── header.py               # Page headers and shared UI elements
│   ├── navigation.py           # Application navigation
│   ├── theme.py                # UI theme and styling
│   ├── views_home.py           # Home dashboard
│   ├── views_analysis.py       # Resume analysis interface
│   ├── views_skill_gap.py      # Skill gap analysis
│   ├── views_roadmap.py        # Learning roadmap
│   ├── views_projects.py       # Project recommendations
│   ├── views_interview.py      # Interview preparation
│   └── views_settings.py       # Settings and information page
│
├── generate_sample_pdf.py      # Generates a sample resume PDF
├── sample_resume.pdf           # Sample resume for testing
└── test_suite.py               # Application tests
```

## 🛠️ Technologies Used

* **Python** — Core programming language
* **Streamlit** — Interactive web application interface
* **LangChain** — LLM integration and AI workflows
* **Groq API** — AI model access
* **PyMuPDF** — PDF resume text extraction
* **Pydantic** — Structured data validation, if used by the implementation

## ✨ Main Features

* Resume PDF upload and text extraction
* AI-powered resume analysis
* Skill gap analysis for a target job role
* Personalized learning roadmap
* Recommended hands-on projects
* Interview preparation
* Reusable UI components and consistent styling

## 🔐 API Configuration

Configure your Groq API key locally using Streamlit secrets.

Create `.streamlit/secrets.toml` with:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

Keep the actual secrets file private and excluded from Git. Commit only `.streamlit/secrets.toml.example` with a placeholder value.

## 🚀 Run the Application

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the application:

```bash
streamlit run app.py
```

## 🧪 Run Tests

```bash
python test_suite.py
```

Use the test command supported by your test suite; if it uses `pytest`, run `python -m pytest` instead.
