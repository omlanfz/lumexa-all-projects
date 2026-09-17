import Link from "next/link";
import { projects } from "@/data/projects";
import ProjectCard from "@/components/ProjectCard";

export default function HomePage() {
  const featured = projects.slice(0, 2);

  return (
    <div className="mx-auto max-w-4xl px-6 py-16">
      <section>
        <p className="text-sky-400 font-medium">Hi, I'm</p>
        <h1 className="mt-1 text-4xl sm:text-5xl font-bold tracking-tight text-white">
          Alex Rivera
        </h1>
        <p className="mt-4 max-w-xl text-slate-300 leading-relaxed">
          I'm a student developer who builds web apps with React and Next.js.
          I like turning ideas into working software fast, then polishing the
          details once the core flow works.
        </p>
        <div className="mt-6 flex gap-4">
          <Link
            href="/projects"
            className="rounded-lg bg-sky-500 px-4 py-2 font-medium text-slate-950 hover:bg-sky-400 transition-colors"
          >
            View my projects
          </Link>
          <Link
            href="/contact"
            className="rounded-lg border border-slate-700 px-4 py-2 font-medium text-slate-100 hover:border-slate-500 transition-colors"
          >
            Get in touch
          </Link>
        </div>
      </section>

      <section className="mt-16">
        <h2 className="text-xl font-semibold text-white">Featured Projects</h2>
        <div className="mt-4 grid gap-5 sm:grid-cols-2">
          {featured.map((project) => (
            <ProjectCard key={project.slug} project={project} />
          ))}
        </div>
      </section>
    </div>
  );
}
