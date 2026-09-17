import Link from "next/link";

const links = [
  { href: "/", label: "Home" },
  { href: "/projects", label: "Projects" },
  { href: "/about", label: "About" },
  { href: "/contact", label: "Contact" },
];

export default function NavBar() {
  return (
    <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-10">
      <nav className="mx-auto max-w-4xl flex items-center justify-between px-6 py-4">
        <Link href="/" className="font-semibold text-lg tracking-tight text-white">
          Alex Rivera
        </Link>
        <ul className="flex gap-6 text-sm text-slate-300">
          {links.map((link) => (
            <li key={link.href}>
              <Link href={link.href} className="hover:text-white transition-colors">
                {link.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
}
