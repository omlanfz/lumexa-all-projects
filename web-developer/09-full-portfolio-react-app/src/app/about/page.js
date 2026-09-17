export const metadata = {
  title: "About — Alex Rivera",
};

const skills = [
  "JavaScript (ES6+)",
  "React",
  "Next.js",
  "Tailwind CSS",
  "REST APIs",
  "Git & GitHub",
];

export default function AboutPage() {
  return (
    <div className="mx-auto max-w-3xl px-6 py-16">
      <h1 className="text-3xl font-bold text-white">About Me</h1>
      <p className="mt-4 leading-relaxed text-slate-300">
        I started coding through a series of interactive online missions, and
        it turned into a genuine hobby. I like building small tools that solve
        a real problem I actually have — a flashcard app for studying, a
        tracker for side projects, a weather app themed around planets. I'm
        most interested in front-end work: making interfaces that feel fast,
        clear, and a little bit fun to use.
      </p>
      <p className="mt-4 leading-relaxed text-slate-300">
        This portfolio itself is built with Next.js and Tailwind CSS as my
        capstone project — it uses the App Router, a dynamic route for each
        project page, and is deployed on Vercel.
      </p>

      <h2 className="mt-10 text-xl font-semibold text-white">Skills</h2>
      <ul className="mt-3 grid grid-cols-2 gap-2 sm:grid-cols-3">
        {skills.map((skill) => (
          <li
            key={skill}
            className="rounded-lg border border-slate-800 bg-slate-900 px-3 py-2 text-sm text-slate-300"
          >
            {skill}
          </li>
        ))}
      </ul>
    </div>
  );
}
