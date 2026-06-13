import React, { useState } from "react";
import { generateQuestions } from "../api.js";

export default function Interview({ resumeText, jobDescription, standalone = false }) {
  // In standalone mode the user types their resume text here; otherwise it
  // comes from the uploaded resume (resumeText prop).
  const [resume, setResume] = useState(resumeText || "");
  const [jd, setJd] = useState(jobDescription || "");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [questions, setQuestions] = useState(null);
  const [open, setOpen] = useState({}); // which answers are revealed

  const effectiveResume = standalone ? resume : resumeText;

  async function run() {
    setError("");
    if (!effectiveResume || !effectiveResume.trim()) {
      setError("Please paste your resume text (or skills) first.");
      return;
    }
    setBusy(true);
    setQuestions(null);
    try {
      const data = await generateQuestions(effectiveResume, jd, 10);
      setQuestions(data.questions || []);
      setOpen({});
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="card mt-24">
      <div className="label">Interview Question Generator</div>
      <p className="muted" style={{ marginTop: -4, marginBottom: 16 }}>
        Generates tailored technical &amp; behavioral questions from your resume skills.
        Optionally paste a target job description to focus the technical ones.
      </p>

      {standalone && (
        <div style={{ marginBottom: 16 }}>
          <label className="label" style={{ display: "block" }}>
            Your resume / skills
          </label>
          <textarea
            placeholder="Paste your resume text or list your skills (e.g. Python, React, SQL, AWS)…"
            value={resume}
            onChange={(e) => setResume(e.target.value)}
          />
        </div>
      )}

      {standalone && (
        <label className="label" style={{ display: "block" }}>
          Target job description (optional)
        </label>
      )}
      <textarea
        placeholder="(Optional) Paste the job description to tailor questions to a specific role…"
        value={jd}
        onChange={(e) => setJd(e.target.value)}
      />

      <div className="mt-16">
        <button className="btn btn-primary" onClick={run} disabled={busy}>
          {busy ? (
            <>
              <span className="spinner" />
              Generating…
            </>
          ) : (
            "Generate questions"
          )}
        </button>
      </div>

      {error && <div className="error">⚠️ {error}</div>}

      {questions && (
        <div className="fade-in mt-24">
          {questions.length === 0 ? (
            <p className="muted">
              No questions generated — try adding more skills or a richer resume.
            </p>
          ) : (
            <>
              <div className="row-between" style={{ marginBottom: 14 }}>
                <span className="muted" style={{ fontSize: 14 }}>
                  {questions.length} questions generated
                </span>
                <button
                  className="q-toggle"
                  onClick={() => {
                    const allOpen = questions.every((_, i) => open[i]);
                    if (allOpen) {
                      setOpen({});
                    } else {
                      const next = {};
                      questions.forEach((_, i) => (next[i] = true));
                      setOpen(next);
                    }
                  }}
                >
                  {questions.every((_, i) => open[i])
                    ? "Hide all answers"
                    : "Show all answers"}
                </button>
              </div>
              <ol className="q-list">
                {questions.map((q, i) => (
                <li key={i} className="q-item">
                  <div className="q-top">
                    <span
                      className={`q-badge ${
                        q.type === "behavioral" ? "beh" : "tech"
                      }`}
                    >
                      {q.type === "behavioral" ? "Behavioral" : q.skill || "Technical"}
                    </span>
                    <button
                      className="q-toggle"
                      onClick={() => setOpen((o) => ({ ...o, [i]: !o[i] }))}
                    >
                      {open[i] ? "Hide answer" : "Show answer"}
                    </button>
                  </div>
                  <p className="q-text">{q.question}</p>
                  {open[i] && (
                    <div className="q-tip fade-in">
                      <span className="q-answer-label">Model answer</span>
                      <p style={{ margin: "6px 0 0" }}>{q.answer}</p>
                    </div>
                  )}
                  </li>
                ))}
              </ol>
            </>
          )}
        </div>
      )}
    </div>
  );
}
