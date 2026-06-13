import React, { useEffect, useRef, useState } from "react";
import Uploader from "./components/Uploader.jsx";
import Results from "./components/Results.jsx";
import Interview from "./components/Interview.jsx";
import { uploadResume, ping } from "./api.js";

const FEATURES = [
  {
    icon: "🧠",
    title: "AI Resume Parsing",
    desc: "Upload a PDF and instantly extract clean text and a structured skill profile using on-device NLP.",
  },
  {
    icon: "📊",
    title: "ATS Scoring",
    desc: "Get a recruiter-style ATS readiness score measuring how well your resume covers in-demand skills.",
  },
  {
    icon: "🎯",
    title: "Job Match",
    desc: "Paste any job description and see your fit percentage, matched skills, and what’s missing.",
  },
  {
    icon: "🪜",
    title: "Skill Gap Analysis",
    desc: "Discover the highest-value skills to learn next to climb the hiring shortlist faster.",
  },
  {
    icon: "💬",
    title: "Interview Prep",
    desc: "Generate tailored technical & behavioral interview questions from your resume and a target role.",
    tab: "interview",
  },
  {
    icon: "🚀",
    title: "Career Roadmap",
    desc: "A personalized growth path from where you are to the role you want. (Coming soon)",
  },
];

export default function App() {
  const [tab, setTab] = useState("home");
  const [online, setOnline] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const [fileName, setFileName] = useState("");

  const analyzeRef = useRef(null);

  useEffect(() => {
    ping().then(setOnline);
  }, []);

  async function handleFile(file) {
    setError("");
    setBusy(true);
    setFileName(file.name);
    setResult(null);
    try {
      const data = await uploadResume(file);
      setResult(data);
      setTab("analyze");
      // scroll results into view shortly after render
      setTimeout(
        () => analyzeRef.current?.scrollIntoView({ behavior: "smooth" }),
        60
      );
    } catch (e) {
      setError(
        e.message +
          (online === false
            ? " — is the backend running on http://127.0.0.1:8000?"
            : "")
      );
    } finally {
      setBusy(false);
    }
  }

  function goAnalyze() {
    setTab("analyze");
    setTimeout(
      () => analyzeRef.current?.scrollIntoView({ behavior: "smooth" }),
      30
    );
  }

  function goInterview() {
    setTab("interview");
    setTimeout(() => window.scrollTo({ top: 0, behavior: "smooth" }), 30);
  }

  return (
    <>
      {/* NAV */}
      <nav className="nav">
        <div className="container nav-inner">
          <div className="brand">
            <img src="/logo.svg" alt="" />
            <span>
              Hire<b>Genius</b> AI
            </span>
          </div>
          <div className="nav-links">
            <button
              className={tab === "home" ? "active" : ""}
              onClick={() => setTab("home")}
            >
              Home
            </button>
            <button
              className={tab === "analyze" ? "active" : ""}
              onClick={goAnalyze}
            >
              Analyze
            </button>
            <button
              className={tab === "interview" ? "active" : ""}
              onClick={goInterview}
            >
              Interview Q&amp;A
            </button>
            <span
              className={`status-dot ${
                online === null ? "" : online ? "online" : "offline"
              }`}
            >
              <i />
              {online === null
                ? "Checking…"
                : online
                ? "API online"
                : "API offline"}
            </span>
          </div>
        </div>
      </nav>

      {/* HERO */}
      {tab === "home" && (
        <header className="hero">
          <div className="container">
            <span className="pill">⚡ AI-powered campus hiring</span>
            <h1>
              Turn your resume into an <em>interview-winning</em> profile
            </h1>
            <p>
              HireGenius AI parses your resume, scores it like an ATS, matches it to
              jobs, and shows you exactly which skills to learn next.
            </p>
            <div className="hero-cta">
              <button className="btn btn-primary" onClick={goAnalyze}>
                Analyze my resume →
              </button>
              <button
                className="btn btn-ghost"
                onClick={() =>
                  document
                    .getElementById("features")
                    ?.scrollIntoView({ behavior: "smooth" })
                }
              >
                See features
              </button>
            </div>

            <div className="stats">
              <div className="stat">
                <b>21+</b>
                <span>Skills detected</span>
              </div>
              <div className="stat">
                <b>&lt;2s</b>
                <span>Avg. analysis time</span>
              </div>
              <div className="stat">
                <b>100%</b>
                <span>Runs on your data</span>
              </div>
            </div>
          </div>
        </header>
      )}

      {/* FEATURES */}
      {tab === "home" && (
        <section className="section" id="features">
          <div className="container">
            <div className="section-head">
              <h2>Everything you need to get hired</h2>
              <p>From raw PDF to a ranked, recruiter-ready profile.</p>
            </div>
            <div className="grid grid-3">
              {FEATURES.map((f) => (
                <div
                  className={`card hover ${f.tab ? "clickable" : ""}`}
                  key={f.title}
                  onClick={f.tab === "interview" ? goInterview : undefined}
                  role={f.tab ? "button" : undefined}
                  tabIndex={f.tab ? 0 : undefined}
                  onKeyDown={(e) => {
                    if (f.tab === "interview" && (e.key === "Enter" || e.key === " ")) {
                      e.preventDefault();
                      goInterview();
                    }
                  }}
                >
                  <div className="ic">{f.icon}</div>
                  <h3>{f.title}</h3>
                  <p>{f.desc}</p>
                  {f.tab && <span className="card-link">Open →</span>}
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* ANALYZE */}
      {tab !== "interview" && (
        <section className="section" ref={analyzeRef}>
          <div className="container">
            {tab === "home" ? (
              <div className="section-head">
                <h2>Try it now</h2>
                <p>Upload a PDF resume and watch the analysis appear live.</p>
              </div>
            ) : (
              <div className="section-head">
                <h2>Analyze your resume</h2>
                <p>Upload a PDF — we’ll do the rest in seconds.</p>
              </div>
            )}

            <div className="card">
              <Uploader onFile={handleFile} busy={busy} fileName={fileName} />
              {error && <div className="error">⚠️ {error}</div>}
            </div>

            {result && (
              <div className="mt-24">
                <Results data={result} />
              </div>
            )}
          </div>
        </section>
      )}

      {/* INTERVIEW Q&A PAGE */}
      {tab === "interview" && (
        <section className="section">
          <div className="container">
            <div className="section-head">
              <h2>Interview Question Generator</h2>
              <p>
                Paste your resume (or skills) and an optional job description to get
                tailored technical &amp; behavioral questions — with answer tips.
              </p>
            </div>
            <Interview standalone resumeText={result?.extracted_text || ""} />
          </div>
        </section>
      )}

      <footer className="footer">
        <div className="container">
          HireGenius AI · Built with FastAPI + React · {new Date().getFullYear()}
        </div>
      </footer>
    </>
  );
}
