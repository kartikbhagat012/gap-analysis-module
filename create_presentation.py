import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Theme Colors
    BG_DARK = RGBColor(15, 23, 42)          # Slate 900
    CARD_BG = RGBColor(30, 41, 59)          # Slate 800
    CARD_BG_LIGHT = RGBColor(40, 53, 76)    # Slate 750
    CARD_BORDER = RGBColor(51, 65, 85)      # Slate 700
    
    ACCENT_CYAN = RGBColor(45, 212, 191)    # Teal/Cyan 400
    ACCENT_BLUE = RGBColor(56, 189, 248)    # Sky Blue 400
    ACCENT_PURPLE = RGBColor(168, 85, 247)  # Purple 400
    ACCENT_YELLOW = RGBColor(250, 204, 21)  # Yellow 400
    ACCENT_GREEN = RGBColor(34, 197, 94)    # Green 500
    ACCENT_RED = RGBColor(248, 113, 113)    # Coral Red 400
    
    TEXT_LIGHT = RGBColor(248, 250, 252)    # Slate 50
    TEXT_MUTED = RGBColor(148, 163, 184)    # Slate 400
    TEXT_DARK = RGBColor(15, 23, 42)

    def add_blank_slide():
        blank_layout = prs.slide_layouts[6]
        slide = prs.slides.add_slide(blank_layout)
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return slide

    def add_header(slide, title, category="FULL PROJECT PRESENTATION"):
        # Category pill text
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.5), Inches(0.35))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = category.upper()
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN

        # Title text
        tx_box2 = slide.shapes.add_textbox(Inches(0.8), Inches(0.78), Inches(11.5), Inches(0.7))
        tf2 = tx_box2.text_frame
        tf2.word_wrap = True
        tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0
        p2 = tf2.paragraphs[0]
        p2.text = title
        p2.font.size = Pt(26)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_LIGHT

    # ==========================================================
    # SLIDE 1: Title Slide
    # ==========================================================
    s1 = add_blank_slide()
    hero = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5))
    hero.fill.solid()
    hero.fill.fore_color.rgb = CARD_BG
    hero.line.color.rgb = CARD_BORDER
    hero.line.width = Pt(1.5)

    tb = s1.shapes.add_textbox(Inches(1.6), Inches(1.5), Inches(10.133), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "AUTONOMOUS MULTI-AGENT ARCHITECTURE"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_CYAN
    p0.alignment = PP_ALIGN.CENTER

    p1 = tf.add_paragraph()
    p1.text = "AI-Driven Career Preparation &\nJob Guidance Platform"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_LIGHT
    p1.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = "\nEnd-to-End Pipeline: Resume Parsing • Semantic Gap Analysis • Adaptive Mock Interviews • Curated Upskilling Roadmap"
    p2.font.size = Pt(13)
    p2.font.color.rgb = ACCENT_BLUE
    p2.alignment = PP_ALIGN.CENTER

    p3 = tf.add_paragraph()
    p3.text = "\nComprehensive Project Overview & System Walkthrough | Engineering Capstone"
    p3.font.size = Pt(13)
    p3.font.color.rgb = TEXT_MUTED
    p3.alignment = PP_ALIGN.CENTER

    # ==========================================================
    # SLIDE 2: Problem Statement
    # ==========================================
    s2 = add_blank_slide()
    add_header(s2, "Problem Statement: 3 Broken Links in Today's Hiring", "The Problem")

    problems = [
        ("The 'Black Box' Rejection", 
         "Job seekers send hundreds of resumes and only receive generic auto-rejections. Candidates never discover what specific technical skills or soft skills caused the rejection.", 
         "Candidates are left in the dark without actionable feedback.", 
         ACCENT_RED),
        ("Flawed Keyword-Based ATS", 
         "Traditional ATS tools rely on rigid exact-keyword matching. A qualified candidate with 'SQL & Database Optimization' gets rejected simply because the JD wrote 'PostgreSQL'.", 
         "True capability is filtered out by dumb keyword traps.", 
         ACCENT_YELLOW),
        ("Analysis Paralysis & Overload", 
         "When learners attempt to upskill, the internet overwhelms them with thousands of random YouTube links, paid courses, and disjointed blogs without any structured roadmap.", 
         "No customized, time-bound daily guidance exists.", 
         ACCENT_BLUE)
    ]

    for i, (title, desc, impact, color) in enumerate(problems):
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i*3.95), Inches(1.8), Inches(3.7), Inches(5.0))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = color
        card.line.width = Pt(1.5)

        tb = s2.shapes.add_textbox(Inches(1.05 + i*3.95), Inches(2.05), Inches(3.2), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = f"0{i+1}. {title}"
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = color

        p_desc = tf.add_paragraph()
        p_desc.text = f"\n{desc}"
        p_desc.font.size = Pt(13)
        p_desc.font.color.rgb = TEXT_LIGHT

        p_imp = tf.add_paragraph()
        p_imp.text = f"\nImpact:\n{impact}"
        p_imp.font.size = Pt(12)
        p_imp.font.bold = True
        p_imp.font.color.rgb = TEXT_MUTED

    # ==========================================================
    # SLIDE 3: The Solution
    # ==========================================================
    s3 = add_blank_slide()
    add_header(s3, "Our Solution: Autonomous Closed-Loop Career Copilot", "The Solution")

    solutions = [
        ("Semantic Skill Intelligence", 
         "Replaces dumb string matching with deep contextual LLM semantic evaluation. Understands conceptual equivalence between candidate experience and target JD expectations.",
         "No keyword rejection; genuine capability is recognized.",
         ACCENT_CYAN),
        ("Dual-Stage Gap Evaluation", 
         "Analyzes gaps across two distinct stages: Initial Resume-to-JD gap analysis AND live technical/behavioral mock interview performance (testing both technical depth and soft skills).",
         "Validates theoretical claims against actual live answers.",
         ACCENT_BLUE),
        ("Curated Open-Access Upskilling", 
         "Directly connects identified weak points to verified, high-quality 100% free resources (freeCodeCamp, Docs, YouTube) arranged in an actionable 30-day or 3-month daily schedule.",
         "Direct, zero-cost bridge from rejection to hireability.",
         ACCENT_GREEN)
    ]

    for i, (title, desc, highlight, color) in enumerate(solutions):
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i*3.95), Inches(1.8), Inches(3.7), Inches(5.0))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = color
        card.line.width = Pt(1.5)

        tb = s3.shapes.add_textbox(Inches(1.05 + i*3.95), Inches(2.05), Inches(3.2), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = f"✔ {title}"
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = color

        p_desc = tf.add_paragraph()
        p_desc.text = f"\n{desc}"
        p_desc.font.size = Pt(13)
        p_desc.font.color.rgb = TEXT_LIGHT

        p_hi = tf.add_paragraph()
        p_hi.text = f"\nKey Advantage:\n{highlight}"
        p_hi.font.size = Pt(12)
        p_hi.font.bold = True
        p_hi.font.color.rgb = TEXT_MUTED

    # ==========================================================
    # SLIDE 4: 5-Agent Workflow & Screening Gate Flowchart
    # ==========================================================
    s4 = add_blank_slide()
    add_header(s4, "5-Agent System Architecture & Screening Gate Flow", "System Pipeline Flowchart")

    # Flowchart layout:
    # Top banner / summary
    top_bar = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.733), Inches(0.6))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = CARD_BG
    top_bar.line.color.rgb = CARD_BORDER
    tb_t = top_bar.text_frame
    p_t = tb_t.paragraphs[0]
    p_t.text = "Input: Raw Candidate Resume (PDF/Doc) + Target Job Description (JD)"
    p_t.font.size = Pt(13)
    p_t.font.bold = True
    p_t.font.color.rgb = ACCENT_CYAN
    p_t.alignment = PP_ALIGN.CENTER

    # Step 1: Agent 1 Card
    c_a1 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.4), Inches(2.6), Inches(2.1))
    c_a1.fill.solid()
    c_a1.fill.fore_color.rgb = CARD_BG
    c_a1.line.color.rgb = ACCENT_BLUE
    c_a1.line.width = Pt(1.5)
    tb1 = c_a1.text_frame
    tb1.word_wrap = True
    p = tb1.paragraphs[0]
    p.text = "1️⃣ Agent 1: Screening"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    p_sub = tb1.add_paragraph()
    p_sub.text = "• Parses raw files\n• Generates resume.json & jd.json\n• Assigns initial Screening Rank (1-100)"
    p_sub.font.size = Pt(10.5)
    p_sub.font.color.rgb = TEXT_LIGHT

    # Arrow 1 -> 2
    arr1 = s4.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(3.5), Inches(3.2), Inches(0.4), Inches(0.3))
    arr1.fill.solid()
    arr1.fill.fore_color.rgb = ACCENT_CYAN
    arr1.line.fill.background()

    # Step 2: Agent 2 (Central Intelligence Hub & Decision Gate)
    c_a2 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.0), Inches(2.4), Inches(3.2), Inches(2.1))
    c_a2.fill.solid()
    c_a2.fill.fore_color.rgb = CARD_BG
    c_a2.line.color.rgb = ACCENT_CYAN
    c_a2.line.width = Pt(2)
    tb2 = c_a2.text_frame
    tb2.word_wrap = True
    p = tb2.paragraphs[0]
    p.text = "2️⃣ Agent 2: Core Brain"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p_sub = tb2.add_paragraph()
    p_sub.text = "• Semantic Gap Engine\n• Produces resume_gap.json\n• Evaluates Screening Gate:\n  Pass (1-75) vs Fail (76-100)"
    p_sub.font.size = Pt(10.5)
    p_sub.font.color.rgb = TEXT_LIGHT

    # Two Branching Paths:
    # Path A: Upper Branch -> Agent 4 (Interview) -> Agent 2 Phase 2
    path_a_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.5), Inches(2.3), Inches(5.0), Inches(2.2))
    path_a_box.fill.solid()
    path_a_box.fill.fore_color.rgb = CARD_BG_LIGHT
    path_a_box.line.color.rgb = ACCENT_GREEN
    path_a_box.line.width = Pt(1.5)
    tba = path_a_box.text_frame
    tba.word_wrap = True
    pa0 = tba.paragraphs[0]
    pa0.text = "✅ QUALIFIED (Rank 1 to 75): Interview Path"
    pa0.font.size = Pt(12)
    pa0.font.bold = True
    pa0.font.color.rgb = ACCENT_GREEN
    pa1 = tba.add_paragraph()
    pa1.text = "➔ 4️⃣ Agent 4: Conducts targeted Mock Interview (interview.json)\n➔ 2️⃣ Agent 2 (Phase 2): Evaluates answers & communication\n    (produces interview_gap.json: Tech + Soft Skills Gaps)"
    pa1.font.size = Pt(10.5)
    pa1.font.color.rgb = TEXT_LIGHT

    # Path B: Lower Branch -> Skip Interview directly to courses
    path_b_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.0), Inches(4.7), Inches(8.5), Inches(0.9))
    path_b_box.fill.solid()
    path_b_box.fill.fore_color.rgb = CARD_BG_LIGHT
    path_b_box.line.color.rgb = ACCENT_RED
    path_b_box.line.width = Pt(1.5)
    tbb = path_b_box.text_frame
    tbb.word_wrap = True
    pb0 = tbb.paragraphs[0]
    pb0.text = "❌ DISQUALIFIED (Rank 76 to 100): Foundation Path (Interview Bypassed)"
    pb0.font.size = Pt(11)
    pb0.font.bold = True
    pb0.font.color.rgb = ACCENT_RED
    pb1 = tbb.add_paragraph()
    pb1.text = "Candidate has excessive foundational gaps. Agent 4 skipped. Only resume_gap.json sent for basic foundational upskilling."
    pb1.font.size = Pt(10)
    pb1.font.color.rgb = TEXT_MUTED

    # Merged Next Steps: Agent 3 & Agent 5
    c_a3 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.8), Inches(5.6), Inches(1.3))
    c_a3.fill.solid()
    c_a3.fill.fore_color.rgb = CARD_BG
    c_a3.line.color.rgb = ACCENT_YELLOW
    tb3 = c_a3.text_frame
    tb3.word_wrap = True
    p = tb3.paragraphs[0]
    p.text = "3️⃣ Agent 3: Course Suggestion Agent"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_YELLOW
    p_sub = tb3.add_paragraph()
    p_sub.text = "Consumes gaps ➔ Maps each missing skill to verified 100% FREE learning resources (freeCodeCamp, MDN, YouTube, GFG) -> courses.json"
    p_sub.font.size = Pt(10.5)
    p_sub.font.color.rgb = TEXT_LIGHT

    c_a5 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(5.8), Inches(5.6), Inches(1.3))
    c_a5.fill.solid()
    c_a5.fill.fore_color.rgb = CARD_BG
    c_a5.line.color.rgb = ACCENT_GREEN
    tb5 = c_a5.text_frame
    tb5.word_wrap = True
    p = tb5.paragraphs[0]
    p.text = "5️⃣ Agent 5: Personalized Learning Planner"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p_sub = tb5.add_paragraph()
    p_sub.text = "Converts courses into actionable 30-Day Sprint or 3-Month Roadmap with daily tasks & estimated completion hours -> learning_plan.json"
    p_sub.font.size = Pt(10.5)
    p_sub.font.color.rgb = TEXT_LIGHT

    # ==========================================================
    # SLIDE 5: Agent 1 — Resume & Screening Agent
    # ==========================================================
    s5 = add_blank_slide()
    add_header(s5, "Agent 1: Resume & Screening Agent (Module 1)", "Module 1 Deep Dive")

    a1_cards = [
        ("Core Function & Purpose", 
         "• Ingests raw unstructured candidate resumes (PDF, DOCX) and Job Descriptions (JD).\n"
         "• Uses LLM parsing to extract structured attributes: technical skills, soft skills, projects, work experience, and educational background.\n"
         "• Standardizes variable JD formats into normalized competencies and seniority levels.", 
         ACCENT_BLUE),
        ("Initial Screening & Ranking", 
         "• Performs initial profile screening comparison between resume attributes and JD requirements.\n"
         "• Calculates initial candidate readiness score.\n"
         "• Assigns applicant a Screening Rank from 1 (Top match) to 100 (Unmatched) which serves as the gate for downstream agents.", 
         ACCENT_CYAN),
        ("Standard Output Contracts", 
         "• resume.json: Clean normalized candidate profile with parsed skills, experience, and projects.\n"
         "• jd.json: Standardized target requirements, mandatory tech stack, and experience brackets.\n"
         "• screening.json: Initial matching metadata and applicant rank number (1-100).", 
         ACCENT_PURPLE)
    ]

    for i, (title, desc, color) in enumerate(a1_cards):
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i*3.95), Inches(1.8), Inches(3.7), Inches(5.0))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = color
        card.line.width = Pt(1.5)

        tb = s5.shapes.add_textbox(Inches(1.05 + i*3.95), Inches(2.05), Inches(3.2), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.rgb = color

        p_desc = tf.add_paragraph()
        p_desc.text = f"\n{desc}"
        p_desc.font.size = Pt(13)
        p_desc.font.color.rgb = TEXT_LIGHT

    # ==========================================================
    # SLIDE 6: Agent 2 — Core Gap Analysis Agent (Brain)
    # ==========================================================
    s6 = add_blank_slide()
    add_header(s6, "Agent 2: Core Gap Analysis Engine (Central Intelligence)", "Module 2 Deep Dive")

    c1 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    c1.fill.solid()
    c1.fill.fore_color.rgb = CARD_BG
    c1.line.color.rgb = ACCENT_CYAN
    c1.line.width = Pt(1.5)
    tb1 = c1.text_frame
    tb1.word_wrap = True
    p1 = tb1.paragraphs[0]
    p1.text = "Phase 2A: Resume vs JD Gap Analysis"
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.color.rgb = ACCENT_CYAN

    p1_body = tb1.add_paragraph()
    p1_body.text = (
        "\n• Semantic Gap Matching: Groq LLM (temperature=0.0 locked) compares resume.json against jd.json.\n\n"
        "• Granular Skill Categorization:\n"
        "   - Critical Gaps: Core mandatory skills completely missing (e.g. Python, Docker, SQL)\n"
        "   - Important Gaps: Secondary required competencies (e.g. Redis, AWS Cloud)\n"
        "   - Matched Skills: Fully verified abilities already in profile\n"
        "   - Soft Skills Analysis: Matched vs missing behavioral traits\n\n"
        "• Prioritization: Computes improvement_priority_order for optimal learning sequence.\n"
        "• Output Contract: resume_gap.json"
    )
    p1_body.font.size = Pt(12.5)
    p1_body.font.color.rgb = TEXT_LIGHT

    c2 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0))
    c2.fill.solid()
    c2.fill.fore_color.rgb = CARD_BG
    c2.line.color.rgb = ACCENT_BLUE
    c2.line.width = Pt(1.5)
    tb2 = c2.text_frame
    tb2.word_wrap = True
    p2 = tb2.paragraphs[0]
    p2.text = "Phase 2B: Screening Gate & Interview Gap"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = ACCENT_BLUE

    p2_body = tb2.add_paragraph()
    p2_body.text = (
        "\n• The Screening Gate Decision:\n"
        "   - Rank 1–75 (Passed): Cleared for live technical mock interview -> Triggers Agent 4.\n"
        "   - Rank 76–100 (Failed): Skipped straight to basic courses (no interview).\n\n"
        "• Post-Interview Evaluation (For Qualified Candidates):\n"
        "   - Ingests interview.json transcript from Agent 4.\n"
        "   - Technical Answer Gaps: Flags shallow answers, conceptual mistakes, skipped questions.\n"
        "   - Soft Skills Evaluation: Measures clarity, confidence, and STAR response structure.\n\n"
        "• Output Contract: interview_gap.json"
    )
    p2_body.font.size = Pt(12.5)
    p2_body.font.color.rgb = TEXT_LIGHT

    # ==========================================================
    # SLIDE 7: Agent 4 — Mock Interview Agent
    # ==========================================================
    s7 = add_blank_slide()
    add_header(s7, "Agent 4: Adaptive Mock Interview Agent (Module 4)", "Module 4 Deep Dive")

    a4_cards = [
        ("Dynamic & Gap-Targeted Q&A", 
         "• Does NOT ask generic random interview questions.\n"
         "• Reads Agent 2's resume_gap.json and candidate projects to target precise borderline areas.\n"
         "• Generates tailored technical coding, system design, and behavioral situational questions.", 
         ACCENT_PURPLE),
        ("Realistic Interview Simulation", 
         "• Simulates realistic technical rounds with progressive difficulty.\n"
         "• Tracks candidate response duration, answer completeness, and skipped question flags.\n"
         "• Captures verbatim candidate responses for downstream evaluation.", 
         ACCENT_CYAN),
        ("Interview Output Generation", 
         "• Compiles full transcript and metadata into interview.json.\n"
         "• Feeds directly back into Agent 2 (Phase 2B) for rigorous dual-stage evaluation.\n"
         "• Only triggered for candidates clearing the Rank 1–75 screening threshold.", 
         ACCENT_GREEN)
    ]

    for i, (title, desc, color) in enumerate(a4_cards):
        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i*3.95), Inches(1.8), Inches(3.7), Inches(5.0))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = color
        card.line.width = Pt(1.5)

        tb = s7.shapes.add_textbox(Inches(1.05 + i*3.95), Inches(2.05), Inches(3.2), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.rgb = color

        p_desc = tf.add_paragraph()
        p_desc.text = f"\n{desc}"
        p_desc.font.size = Pt(13)
        p_desc.font.color.rgb = TEXT_LIGHT

    # ==========================================================
    # SLIDE 8: Agent 3 — Course Suggestion Agent
    # ==========================================================
    s8 = add_blank_slide()
    add_header(s8, "Agent 3: Curated Course Suggestion Agent (Module 3)", "Module 3 Deep Dive")

    a3_cards = [
        ("Dual Gap Input Ingestion", 
         "• Seamlessly ingests findings from both evaluation streams:\n"
         "   1. resume_gap.json (Resume-level technical & framework deficits)\n"
         "   2. interview_gap.json (Interview-level answer errors & skipped concepts)\n"
         "• Merges and de-duplicates learning priorities.", 
         ACCENT_YELLOW),
        ("100% Free & Open-Source Policy", 
         "• Strictly filters OUT expensive paid courses and subscription paywalls.\n"
         "• Recommends high-authority, verified free resources:\n"
         "   - freeCodeCamp certifications & guides\n"
         "   - Official docs (MDN, Python.org, Docker docs)\n"
         "   - GeeksforGeeks, W3Schools & curated YouTube deep-dives.", 
         ACCENT_GREEN),
        ("Actionable Output Contract", 
         "• Maps each weak skill to 2-3 verified tutorials with direct links, course duration, and difficulty level.\n"
         "• Emits courses.json to feed downstream planning.\n"
         "• Democratizes access to career readiness regardless of budget.", 
         ACCENT_BLUE)
    ]

    for i, (title, desc, color) in enumerate(a3_cards):
        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i*3.95), Inches(1.8), Inches(3.7), Inches(5.0))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = color
        card.line.width = Pt(1.5)

        tb = s8.shapes.add_textbox(Inches(1.05 + i*3.95), Inches(2.05), Inches(3.2), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.rgb = color

        p_desc = tf.add_paragraph()
        p_desc.text = f"\n{desc}"
        p_desc.font.size = Pt(13)
        p_desc.font.color.rgb = TEXT_LIGHT

    # ==========================================================
    # SLIDE 9: Agent 5 — Personalized Learning Planner
    # ==========================================================
    s9 = add_blank_slide()
    add_header(s9, "Agent 5: Personalized Learning Planner Agent (Module 5)", "Module 5 Deep Dive")

    c1 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    c1.fill.solid()
    c1.fill.fore_color.rgb = CARD_BG
    c1.line.color.rgb = ACCENT_GREEN
    c1.line.width = Pt(1.5)
    tb1 = c1.text_frame
    tb1.word_wrap = True
    p1 = tb1.paragraphs[0]
    p1.text = "🚀 30-Day Intensive Sprint Track"
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.color.rgb = ACCENT_GREEN

    p1_body = tb1.add_paragraph()
    p1_body.text = (
        "\n• Target Persona: Candidates preparing for imminent interviews within 3-4 weeks.\n\n"
        "• Structure & Focus:\n"
        "   - Hyper-focused on Critical Gaps identified by Agent 2.\n"
        "   - High daily commitment (2.5 – 3.5 hours/day).\n"
        "   - Rapid conceptual review + hands-on implementation.\n\n"
        "• Sample Schedule:\n"
        "   - Day 1: Docker core fundamentals (2 hrs video + 1 hr lab)\n"
        "   - Day 2: Writing custom Dockerfiles & multi-stage builds\n"
        "   - Day 3: Container networking & docker-compose setup"
    )
    p1_body.font.size = Pt(13)
    p1_body.font.color.rgb = TEXT_LIGHT

    c2 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0))
    c2.fill.solid()
    c2.fill.fore_color.rgb = CARD_BG
    c2.line.color.rgb = ACCENT_BLUE
    c2.line.width = Pt(1.5)
    tb2 = c2.text_frame
    tb2.word_wrap = True
    p2 = tb2.paragraphs[0]
    p2.text = "🎯 3-Month / 6-Month Mastery Track"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = ACCENT_BLUE

    p2_body = tb2.add_paragraph()
    p2_body.text = (
        "\n• Target Persona: Students transitioning domains or candidates ranked 76–100 needing foundational depth.\n\n"
        "• Structure & Focus:\n"
        "   - Balanced pace (1 – 1.5 hours/day).\n"
        "   - Covers Critical Gaps, Important Gaps, and Soft Skills.\n"
        "   - Milestone capstone projects and periodic self-assessments.\n\n"
        "• Final Output:\n"
        "   - learning_plan.json: Day-by-day actionable task checklist with exact links, estimated hours, and milestone deliverables."
    )
    p2_body.font.size = Pt(13)
    p2_body.font.color.rgb = TEXT_LIGHT

    # ==========================================================
    # SLIDE 10: Complete Platform Tech Stack
    # ==========================================================
    s10 = add_blank_slide()
    add_header(s10, "Complete Platform Technology Stack", "Under the Hood")

    tech_stack = [
        ("Multi-Agent Framework", "Python 3.11+, LangChain Core, LangGraph for stateful agent workflows, Pydantic v2 schemas for strict contract validation.", "🤖", ACCENT_CYAN),
        ("LLM Inference Engine", "Groq Cloud API (Llama 3.3 70B & Mixtral). Ultra-fast sub-second generation locked at temperature=0.0 for zero hallucination.", "⚡", ACCENT_BLUE),
        ("Backend & API Layer", "FastAPI asynchronous microservices, RESTful endpoints, background task workers, and JSON contract validation envelopes.", "🚀", ACCENT_PURPLE),
        ("Database & Persistence", "Supabase (PostgreSQL) with JSONB schema columns, Row-Level Security, and Vector embeddings for semantic search.", "🗄️", ACCENT_YELLOW)
    ]

    for i, (title, desc, icon, color) in enumerate(tech_stack):
        row = i // 2
        col = i % 2
        card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + col*5.95), Inches(1.8 + row*2.5), Inches(5.7), Inches(2.25))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = color
        card.line.width = Pt(1.5)

        tb = s10.shapes.add_textbox(Inches(1.05 + col*5.95), Inches(1.95 + row*2.5), Inches(5.2), Inches(1.95))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = f"{icon}  {title}"
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.rgb = color

        p_desc = tf.add_paragraph()
        p_desc.text = f"\n{desc}"
        p_desc.font.size = Pt(13)
        p_desc.font.color.rgb = TEXT_LIGHT

    # ==========================================================
    # SLIDE 11: Real-World Impact & Novelty
    # ==========================================================
    s11 = add_blank_slide()
    add_header(s11, "Traditional Hiring vs Our Autonomous Platform", "Impact & Innovation")

    # Table or 2 comparison cards
    c1 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    c1.fill.solid()
    c1.fill.fore_color.rgb = CARD_BG
    c1.line.color.rgb = ACCENT_RED
    c1.line.width = Pt(1.5)
    tb1 = c1.text_frame
    tb1.word_wrap = True
    p1 = tb1.paragraphs[0]
    p1.text = "❌ Traditional Hiring & Learning"
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.color.rgb = ACCENT_RED

    p1_body = tb1.add_paragraph()
    p1_body.text = (
        "\n• Black Box Rejections: 0 feedback provided to candidates.\n\n"
        "• Strict Keyword Bias: ATS drops candidates over synonym mismatch.\n\n"
        "• Disconnected Mock Tests: Generic interview questions disconnected from target JD requirements.\n\n"
        "• Cost Barriers: Paywalled commercial courses push unnecessary subscriptions.\n\n"
        "• Unstructured Chaos: Candidates drown in random YouTube search results."
    )
    p1_body.font.size = Pt(13)
    p1_body.font.color.rgb = TEXT_LIGHT

    c2 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0))
    c2.fill.solid()
    c2.fill.fore_color.rgb = CARD_BG
    c2.line.color.rgb = ACCENT_GREEN
    c2.line.width = Pt(1.5)
    tb2 = c2.text_frame
    tb2.word_wrap = True
    p2 = tb2.paragraphs[0]
    p2.text = "✅ Our Autonomous Platform"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = ACCENT_GREEN

    p2_body = tb2.add_paragraph()
    p2_body.text = (
        "\n• 100% Transparent Feedback: Exact missing skills pinpointed.\n\n"
        "• Semantic Understanding: Evaluates core conceptual proficiency.\n\n"
        "• Adaptive Mock Interviews: Focuses precisely on resume weak points.\n\n"
        "• 100% Free & Open-Access: High-quality curated open resources.\n\n"
        "• Actionable Daily Plan: Step-by-step roadmap turning rejection into job offer."
    )
    p2_body.font.size = Pt(13)
    p2_body.font.color.rgb = TEXT_LIGHT

    # ==========================================================
    # SLIDE 12: Project Summary & Q&A
    # ==========================================================
    s12 = add_blank_slide()
    hero12 = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5))
    hero12.fill.solid()
    hero12.fill.fore_color.rgb = CARD_BG
    hero12.line.color.rgb = ACCENT_CYAN
    hero12.line.width = Pt(1.5)

    tb12 = s12.shapes.add_textbox(Inches(1.6), Inches(1.3), Inches(10.133), Inches(5.0))
    tf12 = tb12.text_frame
    tf12.word_wrap = True

    p = tf12.paragraphs[0]
    p.text = "EXECUTIVE SUMMARY"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.alignment = PP_ALIGN.CENTER

    p2 = tf12.add_paragraph()
    p2.text = "From Rejection to Job Readiness: Closed-Loop AI Copilot"
    p2.font.size = Pt(28)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_LIGHT
    p2.alignment = PP_ALIGN.CENTER

    p3 = tf12.add_paragraph()
    p3.text = (
        "\n30-Second Elevator Pitch for Faculty & Team:\n"
        "\"We built a unified multi-agent platform that solves recruitment's greatest failure — Blind Rejections. "
        "Our system semantically compares Resume to JD (Agent 1 & 2), tests qualified candidates via adaptive mock interviews (Agent 4), "
        "re-evaluates technical & communication gaps (Agent 2 Phase 2), and generates a personalized, 100% free 30-day learning roadmap (Agent 3 & 5). "
        "Every module communicates via strict JSON contracts with zero hallucination.\""
    )
    p3.font.size = Pt(13.5)
    p3.font.color.rgb = ACCENT_BLUE
    p3.alignment = PP_ALIGN.CENTER

    p4 = tf12.add_paragraph()
    p4.text = "\nThank You! Open for Questions & Discussion."
    p4.font.size = Pt(16)
    p4.font.bold = True
    p4.font.color.rgb = TEXT_LIGHT
    p4.alignment = PP_ALIGN.CENTER

    filename_primary = "AI_Career_Guidance_Full_Project.pptx"
    output_path = os.path.abspath(filename_primary)
    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")

    # Also attempt to save to default name if not locked
    filename_secondary = "AI_Career_Guidance_Platform.pptx"
    try:
        prs.save(os.path.abspath(filename_secondary))
        print(f"Also updated: {filename_secondary}")
    except PermissionError:
        print(f"Note: {filename_secondary} is currently open in PowerPoint. Saved as {filename_primary}")

if __name__ == "__main__":
    build_presentation()
