import json
from pathlib import Path

import fitz
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

MAX_PDF_BYTES = 5 * 1024 * 1024
MAX_JOB_DESCRIPTION_CHARS = 8000

SKILLS = [
    "python", "django", "django rest framework", "react", "react.js",
    "javascript", "typescript", "html", "css", "sql", "postgresql",
    "mysql", "git", "rest api", "docker", "aws", "machine learning",
    "generative ai", "communication", "problem solving", "java", "pytest",
    "api", "responsive web applications", "debugging"
]

def home(request):
    return render(request, "index.html")

@require_GET
def health(request):
    return JsonResponse({"status": "ok", "service": "HirePilot AI Fresh"})

def build_report(resume_text, job_description):
    resume_lower = resume_text.lower()
    job_lower = job_description.lower()
    detected = [skill for skill in SKILLS if skill in job_lower]
    # Keep only one of overlapping variants where possible.
    detected = list(dict.fromkeys(detected))
    matched = [skill for skill in detected if skill in resume_lower]
    missing = [skill for skill in detected if skill not in resume_lower]
    score = round(len(matched) / len(detected) * 100) if detected else 0
    strengths = [f"Resume contains the keyword '{skill}'." for skill in matched[:5]]
    improvements = [f"If you have this skill, consider adding truthful evidence for '{skill}'." for skill in missing[:6]]
    if not strengths:
        strengths = ["Resume text was extracted successfully. Review the role-specific skills below."]
    if not improvements:
        improvements = ["Good keyword coverage for the skills detected in this job description. Check that your project achievements are clear and truthful."]
    return {
        "summary": f"Your resume matches {score}% of the {len(detected)} detected job-description keywords. This is a basic keyword estimate, not an official ATS score.",
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "job_skills_detected": detected,
        "strengths": strengths,
        "improvements": improvements,
        "interview_questions": [
            "Explain one project you built and the problem it solves.",
            "Describe a bug you fixed and how you tested the solution.",
            "Which skill in this job description are you currently improving?"
        ],
        "score_note": "Keyword coverage estimate only; not an official ATS score or hiring prediction."
    }

@csrf_exempt
@require_POST
def analyze(request):
    uploaded = request.FILES.get("file")
    job_description = (request.POST.get("job_description") or "").strip()

    if not uploaded:
        return JsonResponse({"detail": "Please upload a PDF resume."}, status=400)
    if Path(uploaded.name).suffix.lower() != ".pdf":
        return JsonResponse({"detail": "Only PDF files are accepted."}, status=400)
    if uploaded.size > MAX_PDF_BYTES:
        return JsonResponse({"detail": "PDF must be 5 MB or smaller."}, status=400)
    if len(job_description) < 30:
        return JsonResponse({"detail": "Please enter a job description of at least 30 characters."}, status=400)
    if len(job_description) > MAX_JOB_DESCRIPTION_CHARS:
        return JsonResponse({"detail": "Job description is too long (maximum 8,000 characters)."}, status=400)

    try:
        raw = uploaded.read()
        if not raw.startswith(b"%PDF"):
            return JsonResponse({"detail": "This file does not appear to be a valid PDF."}, status=400)
        with fitz.open(stream=raw, filetype="pdf") as document:
            if document.page_count > 20:
                return JsonResponse({"detail": "PDF must contain 20 pages or fewer."}, status=400)
            resume_text = "\n".join(page.get_text() for page in document).strip()
    except Exception:
        return JsonResponse({"detail": "Could not read this PDF. Please export it as a text-based PDF."}, status=400)

    if len(resume_text) < 40:
        return JsonResponse({"detail": "No readable text found. Scanned/image-only PDFs are not supported yet."}, status=400)

    return JsonResponse(build_report(resume_text, job_description))
