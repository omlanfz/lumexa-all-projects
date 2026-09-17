import ContactForm from "@/components/ContactForm";

export const metadata = {
  title: "Contact — Alex Rivera",
};

export default function ContactPage() {
  return (
    <div className="mx-auto max-w-2xl px-6 py-16">
      <h1 className="text-3xl font-bold text-white">Contact</h1>
      <p className="mt-2 text-slate-400">
        Have a question about one of my projects, or want to collaborate?
        Send a message below.
      </p>
      <ContactForm />
    </div>
  );
}
