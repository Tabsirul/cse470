// A still picture of the product: the five parts of StudyBuddy meeting in the middle.
const TILES = ["Verify", "Match", "Book", "Pay", "Review"];
const CENTER = 200;
const RADIUS = 150;

function position(index) {
  const angle = ((-90 + index * 72) * Math.PI) / 180;
  return {
    x: CENTER + RADIUS * Math.cos(angle),
    y: CENTER + RADIUS * Math.sin(angle),
  };
}

export default function ProductDiagram() {
  return (
    <svg
      viewBox="0 0 400 400"
      role="img"
      aria-label="StudyBuddy brings together tutor verification, matching, booking, payment and reviews"
    >
      <defs>
        <radialGradient id="centerGlow" cx="35%" cy="30%" r="80%">
          <stop offset="0%" stopColor="#3d78f0" />
          <stop offset="55%" stopColor="#074ce0" />
          <stop offset="100%" stopColor="#0538a8" />
        </radialGradient>
        <filter id="tileShadow" x="-20%" y="-30%" width="140%" height="190%">
          <feDropShadow dx="0" dy="3" stdDeviation="4" floodColor="#16191f" floodOpacity="0.14" />
        </filter>
      </defs>

      <circle cx={CENTER} cy={CENTER} r="108" fill="none" stroke="#dde0e6" strokeWidth="1.5" />
      <circle cx={CENTER} cy={CENTER} r={RADIUS} fill="none" stroke="#dde0e6" strokeWidth="1.5" />

      {TILES.map((label, index) => {
        const { x, y } = position(index);
        return (
          <line
            key={label}
            x1={CENTER}
            y1={CENTER}
            x2={x}
            y2={y}
            stroke="#c3c8d2"
            strokeWidth="1.5"
          />
        );
      })}

      <circle cx={CENTER} cy={CENTER} r="62" fill="url(#centerGlow)" />
      <text x={CENTER} y={CENTER + 5} textAnchor="middle" className="diagram-center">
        StudyBuddy
      </text>

      {TILES.map((label, index) => {
        const { x, y } = position(index);
        return (
          <g key={label} filter="url(#tileShadow)">
            <rect
              x={x - 46}
              y={y - 18}
              width="92"
              height="36"
              rx="10"
              fill="#ffffff"
              stroke="#dde0e6"
            />
            <circle cx={x - 28} cy={y} r="4.5" fill="#074ce0" />
            <text x={x - 16} y={y + 4.5} className="diagram-text">
              {label}
            </text>
          </g>
        );
      })}
    </svg>
  );
}
