// Central API client for the HireGenius AI backend.
// In dev, Vite proxies /api -> http://127.0.0.1:8000 (see vite.config.js).
const BASE = "/api";

/**
 * Upload a resume PDF to the backend.
 * Returns: { message, file_name, extracted_text, skills, all_skills, missing_skills, ats_score }
 */
export async function uploadResume(file) {
  const form = new FormData();
  form.append("file", file);

  const res = await fetch(`${BASE}/upload_resume`, {
    method: "POST",
    body: form,
  });

  if (!res.ok) {
    let detail = `Upload failed (${res.status})`;
    try {
      const body = await res.json();
      if (body?.detail) detail = body.detail;
    } catch (_) {
      /* ignore */
    }
    throw new Error(detail);
  }

  return res.json();
}

/**
 * Generate tailored interview questions from resume text + an optional JD.
 * Calls the backend's rule-based generator: POST /generate_questions
 * Returns: { count, questions: [{ type, skill, question }] }
 */
export async function generateQuestions(resumeText, jobDescription = "", limit = 10) {
  const res = await fetch(`${BASE}/generate_questions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      resume_text: resumeText,
      job_description: jobDescription,
      limit,
    }),
  });

  if (!res.ok) {
    throw new Error(`Could not generate questions (${res.status})`);
  }

  return res.json();
}

/**
 * Health check against the backend root.
 */
export async function ping() {
  try {
    const res = await fetch(`${BASE}/`, { method: "GET" });
    return res.ok;
  } catch (_) {
    return false;
  }
}

/**
 * Client-side keyword match between resume skills and a pasted job description.
 * The backend has no JD-matching route yet, so we compute it here from the
 * skills the backend already extracted from the resume.
 *
 * @param {string[]} resumeSkills  skills extracted from the resume
 * @param {string[]} catalogue     full known-skill catalogue (all_skills)
 * @param {string}   jdText        pasted job-description text
 */
export function matchAgainstJD(resumeSkills, catalogue, jdText) {
  const jd = (jdText || "").toLowerCase();

  // Which catalogue skills does the JD ask for?
  const required = catalogue.filter((s) => jd.includes(s.toLowerCase()));

  const have = required.filter((s) => resumeSkills.includes(s));
  const missing = required.filter((s) => !resumeSkills.includes(s));

  const score = required.length
    ? Math.round((have.length / required.length) * 100)
    : 0;

  return { score, required, have, missing };
}
