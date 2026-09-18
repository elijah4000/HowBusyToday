import { useEffect, useState } from "react";
import { fetchParks } from "../api";
import ParkCard from "../components/ParkCard";

const FILTERS = [
  { id: "all", label: "All", category: "" },
  { id: "waterpark", label: "Waterparks", category: "waterpark" },
  { id: "theme_park", label: "Theme Parks", category: "theme_park" },
  { id: "zoo", label: "Zoos", category: "zoo" },
];

export default function HomePage() {
  const [filter, setFilter] = useState("all");
  const [search, setSearch] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [parks, setParks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedSearch(search.trim()), 250);
    return () => clearTimeout(timer);
  }, [search]);

  useEffect(() => {
    let cancelled = false;
    const active = FILTERS.find((f) => f.id === filter);

    async function load() {
      setLoading(true);
      setError(null);
      try {
        const data = await fetchParks({
          category: active?.category || "",
          search: debouncedSearch,
        });
        if (!cancelled) {
          setParks(Array.isArray(data) ? data : data.results || []);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message || "Failed to load parks");
          setParks([]);
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [filter, debouncedSearch]);

  return (
    <div className="space-y-8">
      <section className="animate-fade space-y-3">
        <p className="text-sm font-medium uppercase tracking-[0.14em] text-brand">
          Find quieter days
        </p>
        <h1 className="font-display max-w-2xl text-4xl font-semibold tracking-tight text-ink sm:text-5xl">
          How busy is your park today?
        </h1>
        <p className="max-w-xl text-lg text-ink-muted">
          Browse regional waterparks, theme parks, and zoos — then open a
          seven-day crowd and weather forecast.
        </p>
      </section>

      <section className="animate-rise space-y-4">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div
            className="flex flex-wrap gap-2"
            role="tablist"
            aria-label="Park category"
          >
            {FILTERS.map((item) => {
              const selected = filter === item.id;
              return (
                <button
                  key={item.id}
                  type="button"
                  role="tab"
                  aria-selected={selected}
                  onClick={() => setFilter(item.id)}
                  className={`rounded-lg px-3.5 py-2 text-sm font-medium transition ${
                    selected
                      ? "bg-brand text-white shadow-sm"
                      : "bg-surface-elevated text-ink-muted hover:bg-line/70 hover:text-ink"
                  }`}
                >
                  {item.label}
                </button>
              );
            })}
          </div>

          <label className="relative block w-full sm:max-w-xs">
            <span className="sr-only">Search parks</span>
            <input
              type="search"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search parks…"
              className="w-full rounded-xl border border-line bg-surface-elevated px-4 py-2.5 text-sm text-ink outline-none transition placeholder:text-ink-muted/70 focus:border-brand focus:ring-2 focus:ring-brand/20"
            />
          </label>
        </div>

        {loading && (
          <p className="text-sm text-ink-muted">Loading parks…</p>
        )}

        {error && (
          <div className="rounded-xl border border-packed/30 bg-packed/10 px-4 py-3 text-sm text-packed">
            {error}
          </div>
        )}

        {!loading && !error && parks.length === 0 && (
          <p className="text-ink-muted">No parks match that filter.</p>
        )}

        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {parks.map((park, index) => (
            <ParkCard key={park.id} park={park} index={index} />
          ))}
        </div>
      </section>
    </div>
  );
}
