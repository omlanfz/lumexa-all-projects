// Real project data used by the projects listing page and the dynamic
// project detail route ([slug]). Add a new object here and a new page is
// generated automatically — no extra routing code needed.

export const projects = [
  {
    slug: "mission-tracker",
    title: "Mission Tracker",
    tagline: "A dashboard for tracking multi-step coding missions.",
    description:
      "Mission Tracker is a React + Node app that lets students break a big project into smaller missions, check them off, and see their progress on a live progress bar. I built the drag-and-drop reordering with the native HTML5 drag events and persisted state with localStorage.",
    stack: ["React", "Node.js", "Express", "SQLite"],
    year: 2026,
    gradient: "from-indigo-500 via-purple-500 to-pink-500",
  },
  {
    slug: "orbit-weather",
    title: "Orbit Weather",
    tagline: "A weather app themed around planets in the solar system.",
    description:
      "Orbit Weather fetches live weather data from a public REST API and maps each condition (clear, cloudy, storm) to a matching planet illustration. It taught me how to handle loading and error states cleanly with useEffect and AbortController.",
    stack: ["React", "REST API", "CSS Modules"],
    year: 2025,
    gradient: "from-sky-500 via-blue-500 to-cyan-400",
  },
  {
    slug: "study-buddy",
    title: "Study Buddy",
    tagline: "A flashcard app with spaced repetition scheduling.",
    description:
      "Study Buddy schedules flashcard reviews using a simplified spaced-repetition algorithm. The whole app is client-side, storing decks in localStorage, and uses Next.js dynamic routes so each deck has its own shareable URL.",
    stack: ["Next.js", "Tailwind CSS", "localStorage"],
    year: 2026,
    gradient: "from-emerald-500 via-teal-500 to-green-400",
  },
  {
    slug: "pixel-garden",
    title: "Pixel Garden",
    tagline: "A collaborative pixel-art canvas built with WebSockets.",
    description:
      "Pixel Garden lets multiple people draw on the same shared grid in real time. I used a WebSocket server to broadcast pixel updates instantly, and built the color palette and grid renderer entirely with React state and the Canvas API.",
    stack: ["React", "WebSockets", "Canvas API"],
    year: 2025,
    gradient: "from-amber-500 via-orange-500 to-rose-500",
  },
];

export function getProjectBySlug(slug) {
  return projects.find((project) => project.slug === slug);
}
