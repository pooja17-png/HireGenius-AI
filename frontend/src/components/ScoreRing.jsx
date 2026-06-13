import React, { useEffect, useState } from "react";

export default function ScoreRing({ value = 0, caption = "ATS Score" }) {
  // Animate from 0 up to value on mount / change.
  const [shown, setShown] = useState(0);
  useEffect(() => {
    let raf;
    const start = performance.now();
    const dur = 700;
    const tick = (now) => {
      const t = Math.min((now - start) / dur, 1);
      const eased = 1 - Math.pow(1 - t, 3);
      setShown(Math.round(eased * value));
      if (t < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [value]);

  return (
    <div className="score-ring" style={{ "--val": shown }}>
      <div className="val">
        <b>{shown}%</b>
        <span>{caption}</span>
      </div>
    </div>
  );
}
