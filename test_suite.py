"""
test_suite.py
=============
Automated test suite verifying resume extraction, schema validation, demo analysis,
markdown generation, and component loading.
"""

import io
import unittest
import pymupdf as fitz
from resume_parser import (
    extract_text_from_pdf,
    clean_extracted_text,
    get_pdf_metadata,
    EmptyPDFError,
    ScannedPDFError,
    ResumeParsingError,
)
from agent import (
    ResumeAnalysisOutput,
    generate_demo_analysis,
    export_analysis_to_markdown,
)


def create_mock_pdf_bytes(text: str) -> bytes:
    """Creates a valid in-memory PDF containing the specified text using PyMuPDF."""
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 72), text)
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


class TestResumeSkillAgent(unittest.TestCase):

    def setUp(self):
        self.sample_resume_text = (
            "Alex Smith - Senior Python Engineer\n"
            "Email: alex.smith@example.com | GitHub: github.com/alexsmith\n\n"
            "SUMMARY\n"
            "Software engineer with 5 years experience building scalable backend APIs and machine learning systems.\n\n"
            "TECHNICAL SKILLS\n"
            "Languages: Python, SQL\n"
            "Frameworks: FastAPI, Flask, PyTorch, Scikit-Learn, Pandas, NumPy\n"
            "Databases & Cloud: PostgreSQL, SQLite, AWS (EC2, S3), Docker, Git\n\n"
            "EXPERIENCE\n"
            "Senior Backend Engineer - Tech Solutions Inc (2022 - Present)\n"
            "- Designed and implemented high-throughput REST APIs using FastAPI and PostgreSQL.\n"
            "- Built predictive data pipelines using Pandas and Scikit-Learn for user analytics.\n"
            "- Containerized backend microservices using Docker and maintained CI/CD pipelines with GitHub Actions.\n\n"
            "PROJECTS\n"
            "Real-time Analytics Engine\n"
            "- Developed stream processing engine with Python, Redis, and PyTorch for sentiment analysis.\n"
        )
        self.pdf_bytes = create_mock_pdf_bytes(self.sample_resume_text)

    def test_text_cleaning(self):
        raw = "Bullet \u2022 point test \t with   extra   spaces\n\n\n\nand multiple lines."
        cleaned = clean_extracted_text(raw)
        self.assertIn("- point test", cleaned)
        self.assertNotIn("   ", cleaned)
        self.assertNotIn("\n\n\n", cleaned)

    def test_pdf_text_extraction(self):
        extracted = extract_text_from_pdf(self.pdf_bytes)
        self.assertIn("Alex Smith", extracted)
        self.assertIn("Python", extracted)
        self.assertIn("FastAPI", extracted)
        self.assertIn("Docker", extracted)

    def test_pdf_metadata(self):
        meta = get_pdf_metadata(self.pdf_bytes)
        self.assertEqual(meta["page_count"], 1)
        self.assertGreater(meta["word_count"], 30)
        self.assertGreater(meta["character_count"], 100)

    def test_empty_pdf_error(self):
        with self.assertRaises(EmptyPDFError):
            extract_text_from_pdf(b"")

    def test_scanned_or_no_text_pdf_error(self):
        doc = fitz.open()
        doc.new_page()  # Blank page with no text
        pdf_bytes = doc.tobytes()
        doc.close()
        with self.assertRaises(ScannedPDFError):
            extract_text_from_pdf(pdf_bytes)

    def test_demo_analysis_generation(self):
        target_role = "Machine Learning Engineer"
        analysis: ResumeAnalysisOutput = generate_demo_analysis(
            resume_text=self.sample_resume_text,
            target_role=target_role,
        )

        # Assert schema fields
        self.assertIsInstance(analysis, ResumeAnalysisOutput)
        self.assertEqual(analysis.target_role, target_role)
        self.assertGreater(analysis.skill_match_percentage, 0)
        self.assertLessEqual(analysis.skill_match_percentage, 100)
        self.assertGreater(len(analysis.evidenced_skills), 0)
        self.assertGreater(len(analysis.not_evidenced_skills), 0)
        self.assertEqual(len(analysis.four_week_roadmap), 4)
        self.assertGreaterEqual(len(analysis.recommended_projects), 2)
        self.assertGreaterEqual(len(analysis.interview_questions), 3)

        # Verify evidenced skills include Python and PyTorch
        evidenced_names = [s.skill_name for s in analysis.evidenced_skills]
        self.assertTrue(any("Python" in name for name in evidenced_names))
        self.assertTrue(any("PyTorch" in name for name in evidenced_names))

        # Check disclaimer presence
        self.assertTrue(len(analysis.match_disclaimer) > 20)

    def test_markdown_report_export(self):
        analysis = generate_demo_analysis(
            resume_text=self.sample_resume_text,
            target_role="Python Developer",
        )
        report = export_analysis_to_markdown(analysis)
        self.assertIn("# 📄 AI Resume & Skill Analysis Report", report)
        self.assertIn("Python Developer", report)
        self.assertIn("## 📊 Executive Match Overview", report)
        self.assertIn("## 🗺️ 4-Week Personalized Learning Roadmap", report)
        self.assertIn("## 🛠️ Recommended Practical Projects", report)
        self.assertIn("## 💡 Role-Specific Interview Preparation", report)

    def test_components_import(self):
        import components.theme
        import components.header
        import components.cards
        import components.navigation
        import components.views_home
        import components.views_analysis
        import components.views_skill_gap
        import components.views_roadmap
        import components.views_projects
        import components.views_interview
        import components.views_settings
        self.assertTrue(hasattr(components.theme, "inject_theme"))
        self.assertTrue(hasattr(components.header, "render_header"))

    def test_config_placeholder_detection(self):
        from config import is_placeholder
        self.assertTrue(is_placeholder(""))
        self.assertTrue(is_placeholder(None))
        self.assertTrue(is_placeholder("gsk_replace_with_your_new_groq_key"))
        self.assertTrue(is_placeholder("short"))
        self.assertFalse(is_placeholder("gsk_validRealGroqKey1234567890abcdef"))

    def test_config_groq_models(self):
        from config import SUPPORTED_GROQ_MODELS, DEFAULT_GROQ_MODEL
        self.assertIn("llama-3.3-70b-versatile", SUPPORTED_GROQ_MODELS)
        self.assertIn("llama-3.1-8b-instant", SUPPORTED_GROQ_MODELS)
        self.assertIn(DEFAULT_GROQ_MODEL, SUPPORTED_GROQ_MODELS)

    def test_missing_groq_key_error_message(self):
        from agent import get_llm
        with self.assertRaises(ValueError) as ctx:
            get_llm(api_key="gsk_replace_with_your_new_groq_key", is_groq=True)
        err_msg = str(ctx.exception)
        self.assertIn("Groq API Key is missing or invalid", err_msg)
        self.assertIn(".streamlit/secrets.toml", err_msg)
        # Ensure dummy key is not leaked in message
        self.assertNotIn("gsk_replace_with_your_new_groq_key", err_msg)

    def test_groq_model_initialization(self):
        from agent import get_llm
        # Valid format dummy key for model config verification
        llm = get_llm(api_key="gsk_1234567890abcdef1234567890abcdef", model_name="llama-3.3-70b-versatile", is_groq=True)
        self.assertIsNotNone(llm)

    def test_views_callables(self):
        from components.views_home import render_home_view
        from components.views_analysis import render_analysis_view
        from components.views_skill_gap import render_skill_gap_view
        from components.views_roadmap import render_roadmap_view
        from components.views_projects import render_projects_view
        from components.views_interview import render_interview_view
        from components.views_settings import render_settings_view

        self.assertTrue(callable(render_home_view))
        self.assertTrue(callable(render_analysis_view))
        self.assertTrue(callable(render_skill_gap_view))
        self.assertTrue(callable(render_roadmap_view))
        self.assertTrue(callable(render_projects_view))
        self.assertTrue(callable(render_interview_view))
        self.assertTrue(callable(render_settings_view))


if __name__ == "__main__":
    unittest.main()
