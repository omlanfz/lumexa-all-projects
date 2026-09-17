import { notFound } from "next/navigation";
import Link from "next/link";
import { projects, getProjectBySlug } from "@/data/projects";

// Pre-render every project detail page at build time.
export function generateStaticParams() {
  return projects.map((project) => ({ slug: project.slug }));
}

export function generateMetadata({ params }) {
  const project = getProjectBySlug(params.slug);
  if (!project) return { title: "Project not found" };
  return { title: `${project.title} — Alex Rivera` };
}

export default function ProjectDetailPage({ params }) {
  const project = getProjectBySlug(params.slug);

  if (!project) {
    notFound();
  }

  return (
    <div className="mx-auto max-w-3xl px-6 py-16">
      <Link href="/projects" className="text-sm text-sky-400 hover:underline">
        &larr; Back to projects
      </Link>

      <div className={`mt-6 h-40 rounded-xl bg-gradient-to-br ${project.gradient}`} />

      <h1 className="mt-6 text-3xl font-bold text-white">{project.title}</h1>
      <p className="mt-1 text-slate-400">{project.tagline}</p>

      <div className="mt-4 flex flex-wrap gap-2">
        {project.stack.map((tech) => (
          <span
            key={tech}
            className="text-xs rounded-full bg-slate-800 px-2 py-1 text-slate-300"
          >
            {tech}
          </span>
        ))}
        <span className="text-xs rounded-full bg-slate-800 px-2 py-1 text-slate-300">
          {project.year}
        </span>
      </div>

      <p className="mt-6 leading-relaxed text-slate-300">{project.description}</p>
    </div>
  );
}
