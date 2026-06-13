import React, { useRef, useState } from "react";

export default function Uploader({ onFile, busy, fileName }) {
  const inputRef = useRef(null);
  const [drag, setDrag] = useState(false);

  function pick(files) {
    const f = files?.[0];
    if (f) onFile(f);
  }

  return (
    <div
      className={`dropzone ${drag ? "drag" : ""}`}
      onClick={() => inputRef.current?.click()}
      onDragOver={(e) => {
        e.preventDefault();
        setDrag(true);
      }}
      onDragLeave={() => setDrag(false)}
      onDrop={(e) => {
        e.preventDefault();
        setDrag(false);
        pick(e.dataTransfer.files);
      }}
    >
      <input
        ref={inputRef}
        type="file"
        accept="application/pdf,.pdf"
        hidden
        onChange={(e) => pick(e.target.files)}
      />
      <div className="big">📄</div>
      <h3>Drop your resume here</h3>
      <p>PDF only · we’ll extract your skills & ATS score instantly</p>
      <button className="btn btn-primary" disabled={busy} type="button">
        {busy ? (
          <>
            <span className="spinner" />
            Analyzing…
          </>
        ) : (
          "Choose PDF"
        )}
      </button>
      {fileName && (
        <div>
          <span className="filechip">📎 {fileName}</span>
        </div>
      )}
    </div>
  );
}
