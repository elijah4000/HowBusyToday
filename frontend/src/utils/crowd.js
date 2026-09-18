export function crowdTone(score) {
  if (score == null) return "unknown";
  if (score <= 3) return "calm";
  if (score <= 6) return "busy";
  return "packed";
}

export function crowdLabel(score) {
  const tone = crowdTone(score);
  if (tone === "calm") return "Low crowds";
  if (tone === "busy") return "Moderate";
  if (tone === "packed") return "Busy";
  return "No data";
}

export function crowdClasses(score) {
  const tone = crowdTone(score);
  if (tone === "calm") {
    return "bg-calm/15 text-calm border-calm/30";
  }
  if (tone === "busy") {
    return "bg-busy/15 text-[#8a6a00] border-busy/30";
  }
  if (tone === "packed") {
    return "bg-packed/15 text-packed border-packed/30";
  }
  return "bg-line/60 text-ink-muted border-line";
}

export function crowdBarColor(score) {
  const tone = crowdTone(score);
  if (tone === "calm") return "bg-calm";
  if (tone === "busy") return "bg-busy";
  if (tone === "packed") return "bg-packed";
  return "bg-line";
}

export function categoryLabel(category) {
  switch (category) {
    case "waterpark":
      return "Waterpark";
    case "theme_park":
      return "Theme Park";
    case "zoo":
      return "Zoo";
    default:
      return category;
  }
}

export function formatDay(dateString) {
  const date = new Date(`${dateString}T12:00:00`);
  return date.toLocaleDateString(undefined, {
    weekday: "short",
    month: "short",
    day: "numeric",
  });
}

export function weatherKind({ rain_chance_percent: rain, predicted_temp_c: temp }) {
  if (rain == null && temp == null) return "unknown";
  if (rain >= 55) return "rain";
  if (rain >= 30) return "cloud";
  if (temp != null && temp >= 27) return "sun-hot";
  return "sun";
}
