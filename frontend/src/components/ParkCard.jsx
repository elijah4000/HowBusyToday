import { Link } from "react-router-dom";
import { categoryLabel } from "../utils/crowd";

const categoryAccent = {
  waterpark: "from-sky-400/20 to-teal-500/10",
  theme_park: "from-amber-400/20 to-orange-500/10",
  zoo: "from-emerald-400/20 to-lime-500/10",
};

export default function ParkCard({ park, index = 0 }) {
  const accent = categoryAccent[park.category] || "from-brand/10 to-brand/5";
  const stagger = `stagger-${Math.min(index + 1, 7)}`;

  return (
    <Link
      to={`/park/${park.slug}`}
      className={`animate-rise ${stagger} group block overflow-hidden rounded-2xl border border-line bg-surface-elevated shadow-[0_10px_30px_-18px_rgba(16,35,28,0.45)] transition duration-300 hover:-translate-y-1 hover:border-brand/30 hover:shadow-[0_18px_40px_-18px_rgba(13,107,76,0.35)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand`}
    >
      <div className={`h-28 bg-gradient-to-br ${accent}`}>
        <div className="flex h-full items-end p-4">
          <span className="rounded-md bg-surface-elevated/90 px-2 py-1 text-xs font-medium uppercase tracking-wide text-ink-muted">
            {categoryLabel(park.category)}
          </span>
        </div>
      </div>
      <div className="space-y-2 p-4">
        <h2 className="font-display text-xl font-semibold text-ink transition group-hover:text-brand-deep">
          {park.name}
        </h2>
        <p className="text-sm text-ink-muted">{park.timezone.replace(/_/g, " ")}</p>
        <p className="text-sm font-medium text-brand">
          View 7-day forecast →
        </p>
      </div>
    </Link>
  );
}
