import { Link } from "react-router-dom";

export default function Layout({ children }) {
  return (
    <div className="relative min-h-screen overflow-x-hidden">
      <div
        className="pointer-events-none absolute inset-0 -z-10"
        aria-hidden="true"
      >
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_#dcefe4_0%,_#f3f7f4_45%,_#eaf2ec_100%)]" />
        <div className="absolute -left-24 top-24 h-72 w-72 rounded-full bg-brand/10 blur-3xl" />
        <div className="absolute -right-16 top-80 h-80 w-80 rounded-full bg-accent/10 blur-3xl" />
      </div>

      <header className="border-b border-line/80 bg-surface-elevated/70 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6">
          <Link to="/" className="group flex items-baseline gap-2">
            <span className="font-display text-2xl font-semibold tracking-tight text-brand-deep transition group-hover:text-brand">
              HowBusyToday
            </span>
            <span className="hidden text-sm text-ink-muted sm:inline">
              Regional park crowd forecasts
            </span>
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6 sm:py-10">
        {children}
      </main>
    </div>
  );
}
