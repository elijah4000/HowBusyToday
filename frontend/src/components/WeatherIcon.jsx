export default function WeatherIcon({ kind, className = "" }) {
  const common = `h-8 w-8 ${className}`;

  if (kind === "rain") {
    return (
      <svg viewBox="0 0 32 32" className={common} aria-hidden="true">
        <path
          d="M10 14a6 6 0 0 1 11.5-2.4A4.5 4.5 0 0 1 24 20H11a4 4 0 0 1-1-6z"
          fill="#7aa7c7"
        />
        <path
          d="M12 22v4M16 23v4M20 22v4"
          stroke="#4d7ea8"
          strokeWidth="2"
          strokeLinecap="round"
        />
      </svg>
    );
  }

  if (kind === "cloud") {
    return (
      <svg viewBox="0 0 32 32" className={common} aria-hidden="true">
        <circle cx="11" cy="12" r="4" fill="#f0c75e" opacity="0.85" />
        <path
          d="M10 16a5.5 5.5 0 0 1 10.6-2A4 4 0 0 1 23 21H11.5A4 4 0 0 1 10 16z"
          fill="#9eb6c9"
        />
      </svg>
    );
  }

  if (kind === "sun-hot") {
    return (
      <svg viewBox="0 0 32 32" className={common} aria-hidden="true">
        <circle cx="16" cy="16" r="6" fill="#f0a020" />
        <g stroke="#e07a3d" strokeWidth="2" strokeLinecap="round">
          <path d="M16 4v3M16 25v3M4 16h3M25 16h3M7.5 7.5l2.1 2.1M22.4 22.4l2.1 2.1M7.5 24.5l2.1-2.1M22.4 9.6l2.1-2.1" />
        </g>
      </svg>
    );
  }

  if (kind === "unknown") {
    return (
      <svg viewBox="0 0 32 32" className={common} aria-hidden="true">
        <circle cx="16" cy="16" r="8" fill="#d5e3db" />
      </svg>
    );
  }

  return (
    <svg viewBox="0 0 32 32" className={common} aria-hidden="true">
      <circle cx="16" cy="16" r="6" fill="#f0c75e" />
      <g stroke="#e6b84d" strokeWidth="2" strokeLinecap="round">
        <path d="M16 5v2.5M16 24.5V27M5 16h2.5M24.5 16H27M8 8l1.8 1.8M22.2 22.2 24 24M8 24l1.8-1.8M22.2 9.8 24 8" />
      </g>
    </svg>
  );
}
