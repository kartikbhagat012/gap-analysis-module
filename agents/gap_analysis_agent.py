"""
Module 2 — Gap Analysis Agent (CORE)
=====================================================
INPUT  : resume.json  (structured, from Module 1)
       + jd.json      (structured, from Module 1)
OUTPUT : gap_report.json  (CTBF-AI-05 envelope)

This module's output (gap_report.json) feeds:
  → Module 3 (Course Suggestions)
  → Module 4 (Mock Interview)
  → Module 5 (Learning Planner)

NOTE: Interview JSON is NOT an input here.
      Interview (Module 4) runs AFTER gap analysis.
=====================================================
"""

import os
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from models.schemas import GapAnalysisData, GapReportEnvelope

load_dotenv()


class GapAnalysisAgent:
    """
    Module 2 — Core gap analysis engine.
    Uses semantic LLM matching (NOT string equality).
    """

    MODEL_NAME = "openai/gpt-oss-120b"

    def __init__(self):
        self.llm = ChatGroq(
            model=self.MODEL_NAME,
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY"),
        )

    def _extract_skills(self, resume_json: dict) -> tuple[list[str], list[str], str]:
        """Helper to extract technical skills, soft skills, and candidate name safely from real or legacy resume JSON."""
        candidate = resume_json.get("candidate", {})
        candidate_name = candidate.get("name", resume_json.get("full_name", "Candidate"))

        tech_skills = []
        if "all_skills_flat" in resume_json:
            tech_skills.extend(resume_json["all_skills_flat"])
        elif "skills" in resume_json and isinstance(resume_json["skills"], list):
            tech_skills.extend(resume_json["skills"])
        elif "skills" in resume_json and isinstance(resume_json["skills"], dict):
            s = resume_json["skills"]
            for k in ["programming_languages", "frameworks", "libraries", "databases", "cloud_technologies", "tools", "domain_specific_skills"]:
                tech_skills.extend(s.get(k, []))

        soft_skills = []
        if "skills" in resume_json and isinstance(resume_json["skills"], dict):
            soft_skills.extend(resume_json["skills"].get("soft_skills", []))

        tech_skills = list(dict.fromkeys(tech_skills))
        soft_skills = list(dict.fromkeys(soft_skills))

        return tech_skills, soft_skills, candidate_name

    def _extract_jd_requirements(self, jd_json: dict) -> tuple[list[str], list[str], list[str], str]:
        """Helper to extract required tech skills, preferred skills, soft skills, and title from real or legacy JD JSON."""
        job = jd_json.get("job", jd_json)
        title = job.get("title", "Target Role")
        required_skills = job.get("required_skills", [])
        preferred_skills = job.get("preferred_skills", [])
        required_soft_skills = job.get("required_soft_skills", [])
        tools = job.get("tools_and_technologies", [])

        all_required_tech = list(dict.fromkeys(required_skills + tools))

        return all_required_tech, preferred_skills, required_soft_skills, title

    def _analyze(
        self,
        candidate_skills: list[str],
        candidate_soft_skills: list[str],
        jd_required_skills: list[str],
        jd_preferred_skills: list[str],
        jd_required_soft_skills: list[str],
    ) -> dict:
        """Perform semantic skill gap analysis (Technical + Soft Skills) using LLM."""

        prompt = ChatPromptTemplate.from_template(
            """You are an expert technical talent assessor and recruiter.
Compare the Candidate's profile against the Job Description (JD) using SEMANTIC understanding.
DO NOT do dumb string matching. E.g. "ReactJS" covers "Frontend/React", "REST APIs" covers "API integration", but missing "Python" or "FastAPI" is a critical gap for a Python Backend role.

Candidate Technical Skills: {candidate_skills}
Candidate Soft Skills: {candidate_soft_skills}

JD Required Technical Skills & Tools: {jd_required_skills}
JD Preferred Skills: {jd_preferred_skills}
JD Required Soft Skills: {jd_required_soft_skills}

Categorize gaps objectively with ZERO hallucination.
Return ONLY a valid JSON object (no markdown, no code fences, no extra text):
{{
  "technical_gaps": {{
    "critical_gaps": ["mandatory required technical skills completely missing in candidate"],
    "important_gaps": ["secondary or preferred skills missing or weak"],
    "optional_gaps": ["bonus nice-to-have skills missing"],
    "matched_skills": ["candidate skills that successfully match JD requirements"],
    "missing_keywords": ["important tools or architectural keywords missing from candidate profile"]
  }},
  "soft_skills_gaps": {{
    "matched_soft_skills": ["soft skills candidate already possesses that match JD"],
    "missing_soft_skills": ["mandatory soft skills required by JD that are not shown in candidate profile"]
  }},
  "improvement_priority_order": ["prioritized sequence of skills the candidate must learn first to qualify"]
}}"""
        )
        chain = prompt | self.llm
        response = chain.invoke({
            "candidate_skills": json.dumps(candidate_skills),
            "candidate_soft_skills": json.dumps(candidate_soft_skills),
            "jd_required_skills": json.dumps(jd_required_skills),
            "jd_preferred_skills": json.dumps(jd_preferred_skills),
            "jd_required_soft_skills": json.dumps(jd_required_soft_skills),
        })

        raw_json = response.content.strip()
        if raw_json.startswith("```"):
            raw_json = raw_json.split("```")[1]
            if raw_json.startswith("json"):
                raw_json = raw_json[4:]

        return json.loads(raw_json)

    def run(self, module1_output: dict) -> dict:
        """
        Run Module 2 — called by the pipeline (Module 1 output passed directly).

        Args:
            module1_output: dict with keys 'resume', 'jd', 'session_id'
                            (Module1Output schema from Module 1)

        Returns:
            dict matching GapReportEnvelope (CTBF-AI-05)
        """
        resume = module1_output["resume"]
        jd = module1_output["jd"]
        session_id = module1_output["session_id"]

        return self._build_output(resume=resume, jd=jd, session_id=session_id)

    def run_from_json(self, resume_json: dict, jd_json: dict) -> dict:
        """
        Run Module 2 — called directly with separate JSON inputs.
        Use this when you have resume.json + jd.json as standalone files.

        ─── INPUT ────────────────────────────────────────────
        resume_json  →  resume.json  (output of Module 1)
            Required keys:
                user_id         : str (UUID)
                resume_id       : str (UUID)
                skills          : List[str]
                experience_years: float

        jd_json      →  jd.json  (output of Module 1)
            Required keys:
                job_id          : str (UUID)
                required_skills : List[str]

        ─── OUTPUT ───────────────────────────────────────────
        gap_report.json  →  CTBF-AI-05 envelope
            Goes to: Module 3 (Course Suggestions)
                     Module 4 (Mock Interview)
                     Module 5 (Learning Planner)

        ─── WHAT IS NOT AN INPUT ─────────────────────────────
        ❌ interview_report.json  — Interview is Module 4, runs AFTER gap analysis
        ❌ courses.json           — Courses are Module 3 output, not input here
        ──────────────────────────────────────────────────────

        Args:
            resume_json: Parsed resume dict (resume.json from Module 1)
            jd_json    : Parsed JD dict     (jd.json from Module 1)

        Returns:
            dict matching GapReportEnvelope (CTBF-AI-05)
        """
        import uuid
        session_id = str(uuid.uuid4())
        return self._build_output(resume=resume_json, jd=jd_json, session_id=session_id)

    def run_from_files(self, resume_json_path: str, jd_json_path: str) -> dict:
        """
        Run Module 2 — load resume.json + jd.json directly from file paths.

        Args:
            resume_json_path: Absolute or relative path to resume.json
            jd_json_path    : Absolute or relative path to jd.json

        Returns:
            dict matching GapReportEnvelope (CTBF-AI-05)
        """
        resume_path = Path(resume_json_path)
        jd_path = Path(jd_json_path)

        if not resume_path.exists():
            raise FileNotFoundError(f"resume.json not found: {resume_json_path}")
        if not jd_path.exists():
            raise FileNotFoundError(f"jd.json not found: {jd_json_path}")

        with open(resume_path, "r", encoding="utf-8") as f:
            resume_json = json.load(f)

        with open(jd_path, "r", encoding="utf-8") as f:
            jd_json = json.load(f)

        return self.run_from_json(resume_json=resume_json, jd_json=jd_json)

    def evaluate_screening(self, screening_json: dict) -> tuple[bool, int, str]:
        """
        Check if candidate qualifies for interview based on screening rank.
        Rule: Rank 1-75 -> Qualified (Interview Allowed)
              Rank 76-100 -> Disqualified (No Interview, Direct to Courses)
        """
        rank = screening_json.get("rank", screening_json.get("ranking", 100))
        if 1 <= rank <= 75:
            return True, rank, f"Qualified for interview (Rank: {rank})"
        else:
            return False, rank, f"Did not qualify for interview (Rank: {rank} is in 76-100 bracket)"

    def analyze_interview(self, interview_json: dict) -> dict:
        """
        Analyze mock interview results from Module 4.
        Takes Module 4 output with schema: { interview_id, role, items: [...] }
        Separates technical skill gaps and soft skill gaps with ZERO hallucination (temperature=0.0).
        """
        interview_id = interview_json.get("interview_id", "unknown_interview")
        role = interview_json.get("role", "Target Role")
        items = interview_json.get("items", [])

        prompt = ChatPromptTemplate.from_template(
            """You are a strict, objective technical and HR interview evaluator.
Evaluate the candidate's interview session data strictly based ONLY on the evidence provided in the transcript items.
Pay close attention to:
- Questions answered vs skipped (status: "skipped" indicates an immediate knowledge gap).
- Question difficulty and skill_tested (e.g. LangGraph, RAG, System Design).
- Quality and depth of answer.

Interview Data:
Role: {role}
Interview Items:
{items}

Provide an objective evaluation separating Technical Skills and Soft Skills.
Return ONLY valid JSON (no markdown formatting, no commentary) with this exact schema:
{{
  "overall_interview_score": 0.0,
  "technical_evaluation": {{
    "demonstrated_strong_skills": ["observed solid technical skills where answers were good"],
    "critical_technical_gaps": ["skills/topics where candidate gave weak answers or skipped"],
    "skipped_skills": ["skills where status was skipped"],
    "conceptual_misunderstandings": ["exact technical errors or confusions made by candidate in answers"],
    "priority_technical_topics_to_learn": ["ordered list of technical topics needing immediate study"]
  }},
  "soft_skills_evaluation": {{
    "communication_clarity": "Strong | Average | Needs Improvement",
    "problem_solving_approach": "Analytical | Direct | Unstructured | Hesitant",
    "observed_soft_skill_strengths": ["e.g. Honest about unknown topics, concise phrasing"],
    "critical_soft_skill_gaps": ["e.g. Lacks structured answering (STAR method), vague explanations, low confidence"]
  }},
  "actionable_interview_advice": "1-2 sentence concrete advice for candidate improvement"
}}"""
        )

        chain = prompt | self.llm
        response = chain.invoke({
            "role": role,
            "items": json.dumps(items)
        })
        raw_json = response.content.strip()

        if raw_json.startswith("```"):
            raw_json = raw_json.split("```")[1]
            if raw_json.startswith("json"):
                raw_json = raw_json[4:]

        parsed = json.loads(raw_json)

        return {
            "interview_id": interview_id,
            "role": role,
            "analysis_type": "interview_performance_gap",
            "status": "completed",
            "data": parsed,
            "created_at": datetime.utcnow().isoformat() + "Z"
        }

    def _build_output(self, resume: dict, jd: dict, session_id: str) -> dict:
        """Internal: builds the gap report from parsed resume + jd dicts."""
        candidate_tech, candidate_soft, candidate_name = self._extract_skills(resume)
        jd_required, jd_preferred, jd_soft, job_title = self._extract_jd_requirements(jd)

        gap_data = self._analyze(
            candidate_skills=candidate_tech,
            candidate_soft_skills=candidate_soft,
            jd_required_skills=jd_required,
            jd_preferred_skills=jd_preferred,
            jd_required_soft_skills=jd_soft,
        )

        user_id = resume.get("user_id", resume.get("candidate", {}).get("email", "candidate_user"))
        resume_id = resume.get("resume_id", "resume_001")
        job_id = jd.get("job_id", jd.get("job", {}).get("title", "job_001"))

        tech_critical = gap_data.get("technical_gaps", {}).get("critical_gaps", [])
        tech_important = gap_data.get("technical_gaps", {}).get("important_gaps", [])
        tech_matched = gap_data.get("technical_gaps", {}).get("matched_skills", [])
        tech_missing_kw = gap_data.get("technical_gaps", {}).get("missing_keywords", [])
        priority_order = gap_data.get("improvement_priority_order", tech_critical + tech_important)

        envelope = {
            "user_id": user_id,
            "resume_id": resume_id,
            "job_id": job_id,
            "session_id": session_id,
            "module": "skill_gap_analysis",
            "candidate_name": candidate_name,
            "target_job_title": job_title,
            "status": "completed",
            "data": {
                "critical_gaps": tech_critical,
                "important_gaps": tech_important,
                "optional_gaps": gap_data.get("technical_gaps", {}).get("optional_gaps", []),
                "matched_skills": tech_matched,
                "missing_keywords": tech_missing_kw,
                "soft_skills_analysis": gap_data.get("soft_skills_gaps", {}),
                "improvement_priority_order": priority_order
            },
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
        return envelope
