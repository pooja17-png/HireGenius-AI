import React, { useState } from "react";
import ScoreRing from "./ScoreRing.jsx";
import Interview from "./Interview.jsx";
import { matchAgainstJD } from "../api.js";

export default function Results({ data }) {
  const [jd, setJd] = useState("");
  const [match, setMatch] = useState(null);

  const skills = data.skills || [];
  const missing = data.missing_skills || [];
  const catalogue = data.all_skills || [];

  function runMatch() {
    setMatch(matchAgainstJD(skills, catalogue, jd));
  }

  return (
    <div className="fade-in">
      {/* Top summary */}
      <div className="grid grid-2">
        <div className="card">
          <div className="label">Resume Analysis</div>
          <div className="row-between" style={{ alignItems: "flex-start" }}>
            <div style={{ flex: 1 }}>
              <h3 style={{ fontSize: 20 }}>{data.file_name}</h3>
              <p className="muted" style={{ marginTop: 8 }}>
                We detected <b style={{ color: "var(--text)" }}>{skills.length}</b> known
                skills in this resume.
              </p>

              <div className="label mt-24">Matched skills</div>
              {skills.length ? (
                <div className="tags">
                  {skills.map((s) => (
                    <span key={s} className="tag good">
                      ✓ {s}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="muted">No catalogue skills detected.</p>
              )}
            </div>
          </div>
        </div>

        <div className="card center">
          <div className="label">ATS Readiness</div>
          <ScoreRing value={data.ats_score ?? 0} />
          <p className="muted mt-16">
            Based on coverage of {catalogue.length} in-demand skills.
          </p>
        </div>
      </div>

      {/* Skill gap */}
      <div className="card mt-24">
        <div className="label">Skill Gap — grow your score</div>
        <p className="muted" style={{ marginTop: -4, marginBottom: 16 }}>
          High-value skills not yet found in your resume. Learning these lifts your ATS
          score.
        </p>
        <div className="tags">
          {missing.length ? (
            missing.map((s) => (
              <span key={s} className="tag bad">
                + {s}
              </span>
            ))
          ) : (
            <span className="muted">🎉 You cover the entire skill catalogue!</span>
          )}
        </div>
      </div>

      {/* JD matcher */}
      <div className="card mt-24">
        <div className="label">Job Match — paste a job description</div>
        <textarea
          placeholder="Paste a job description here to see how well your resume matches…"
          value={jd}
          onChange={(e) => setJd(e.target.value)}
        />
        <div className="mt-16">
          <button
            className="btn btn-primary"
            onClick={runMatch}
            disabled={!jd.trim()}
          >
            Calculate match
          </button>
        </div>

        {match && (
          <div className="fade-in mt-24">
            {match.required.length === 0 ? (
              <p className="muted">
                No catalogue skills were found in that job description — try a more
                detailed posting.
              </p>
            ) : (
              <>
                <div className="row-between">
                  <b style={{ fontFamily: "Sora", fontSize: 22 }}>
                    {match.score}% match
                  </b>
                  <span className="muted">
                    {match.have.length}/{match.required.length} required skills
                  </span>
                </div>
                <div className="bar mt-16">
                  <i style={{ width: `${match.score}%` }} />
                </div>

                <div className="grid grid-2 mt-24">
                  <div>
                    <div className="label">You have</div>
                    <div className="tags">
                      {match.have.length ? (
                        match.have.map((s) => (
                          <span key={s} className="tag good">
                            ✓ {s}
                          </span>
                        ))
                      ) : (
                        <span className="muted">None yet</span>
                      )}
                    </div>
                  </div>
                  <div>
                    <div className="label">Missing for this role</div>
                    <div className="tags">
                      {match.missing.length ? (
                        match.missing.map((s) => (
                          <span key={s} className="tag bad">
                            + {s}
                          </span>
                        ))
                      ) : (
                        <span className="muted">Nothing — perfect fit! 🎯</span>
                      )}
                    </div>
                  </div>
                </div>
              </>
            )}
          </div>
        )}
      </div>

      {/* Interview question generator (backend: /generate_questions) */}
      <Interview resumeText={data.extracted_text || ""} jobDescription={jd} />

      {/* Extracted text */}
      <div className="card mt-24">
        <div className="label">Extracted Resume Text</div>
        <div className="resume-text">
          {data.extracted_text?.trim() || "No text could be extracted."}
        </div>
      </div>
    </div>
  );
}
