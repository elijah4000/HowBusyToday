import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { fetchParkForecast } from "../api";
import WeatherIcon from "../components/WeatherIcon";
import {
  categoryLabel,
  crowdBarColor,
  crowdClasses,
  crowdLabel,
  formatDay,
  weatherKind,
} from "../utils/crowd";

export default function ParkDetailPage() {
  const { slug } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      setLoading(true);
      setError(null);
      try {
        const payload = await fetchParkForecast(slug);
        if (!cancelled) setData(payload);
      } catch (err) {
        if (!cancelled) {
          setError(err.message || "Failed to load forecast");
          setData(null);
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [slug]);

  if (loading) {
    return <p className="text-ink-muted">Loading forecast…</p>;
  }

  if (error) {
    return (
      <div className="space-y-4">
        <Link to="/" className="text-sm font-medium text-brand hover:underline">
          ← Back to parks
        </Link>
        <div className="rounded-xl border border-packed/30 bg-packed/10 px-4 py-3 text-sm text-packed">
          {error}
        </div>
      </div>
    );
  }

  const { park, forecast } = data;

  return (
    <div className="space-y-8">
      <div className="animate-fade space-y-4">
        <Link to="/" className="text-sm font-medium text-brand hover:underline">
          ← Back to parks
        </Link>

        <div className="space-y-3">
          <p className="text-sm font-medium uppercase tracking-[0.14em] text-brand">
            {categoryLabel(park.category)}
          </p>
          <h1 className="font-display text-4xl font-semibold tracking-tight text-ink sm:text-5xl">
            {park.name}
          </h1>
          <p className="max-w-2xl text-ink-muted">
            Seven-day crowd outlook with local weather. Scores run from 1 (quiet)
            to 10 (packed).
          </p>
        </div>
      </div>

      <section className="space-y-3" aria-label="Seven day forecast">
        {forecast.map((day, index) => {
          const score = day.crowd_score;
          const width = score != null ? `${score * 10}%` : "0%";
          const kind = weatherKind(day);
          const stagger = `stagger-${Math.min(index + 1, 7)}`;

          return (
            <article
              key={day.date}
              className={`animate-rise ${stagger} grid gap-4 rounded-2xl border border-line bg-surface-elevated/90 p-4 sm:grid-cols-[1fr_auto] sm:items-center sm:p-5`}
            >
              <div className="space-y-3">
                <div className="flex flex-wrap items-center gap-2">
                  <h2 className="font-display text-xl font-semibold text-ink">
                    {formatDay(day.date)}
                  </h2>
                  {day.is_stat_holiday && (
                    <span className="rounded-md bg-accent/15 px-2 py-0.5 text-xs font-semibold uppercase tracking-wide text-accent">
                      Holiday
                    </span>
                  )}
                  {day.is_weekend && !day.is_stat_holiday && (
                    <span className="rounded-md bg-brand/10 px-2 py-0.5 text-xs font-semibold uppercase tracking-wide text-brand">
                      Weekend
                    </span>
                  )}
                </div>

                <div className="flex flex-wrap items-center gap-3">
                  <span
                    className={`inline-flex items-center rounded-lg border px-2.5 py-1 text-sm font-semibold ${crowdClasses(score)}`}
                  >
                    {score != null ? `${score}/10` : "—"} · {crowdLabel(score)}
                  </span>
                  {day.confidence_score != null && (
                    <span className="text-xs text-ink-muted">
                      Confidence {Math.round(day.confidence_score * 100)}%
                    </span>
                  )}
                </div>

                <div className="h-2.5 overflow-hidden rounded-full bg-line/80">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${crowdBarColor(score)}`}
                    style={{ width }}
                  />
                </div>
              </div>

              <div className="flex items-center gap-3 sm:min-w-[9.5rem] sm:justify-end">
                <WeatherIcon kind={kind} />
                <div className="text-sm">
                  <p className="font-semibold text-ink">
                    {day.predicted_temp_c != null
                      ? `${Math.round(day.predicted_temp_c)}°C`
                      : "—"}
                  </p>
                  <p className="text-ink-muted">
                    {day.rain_chance_percent != null
                      ? `${day.rain_chance_percent}% rain`
                      : "No weather"}
                  </p>
                </div>
              </div>
            </article>
          );
        })}
      </section>
    </div>
  );
}
