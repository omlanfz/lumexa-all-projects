import Link from "next/link";

export default function ProjectCard({ project }) {
  return (
    <Link
      href={`/projects/${project.slug}`}
      className="group block rounded-xl border border-slate-800 bg-slate-900 overflow-hidden hover:border-slate-600 transition-colors"
    >
      <div className={`h-32 bg-gradient-to-br ${project.gradient}`} />
      <div className="p-5">
        <h3 className="text-lg font-semibold text-white group-hover:underline">
          {project.title}
        </h3>
        <p className="mt-1 text-sm text-slate-400">{project.tagline}</p>
        <div className="mt-3 flex flex-wrap gap-2">
          {project.stack.map((tech) => (
            <span
              key={tech}
              className="text-xs rounded-full bg-slate-800 px-2 py-1 text-slate-300"
            >
              {tech}
            </span>
          ))}
        </div>
      </div>
    </Link>
  );
}
