// Seed data for the Lumexa Orbit feed. Avatars and post images are CSS
// gradients so the app never depends on external network requests.

export const initialPosts = [
  {
    id: "post-1",
    author: "Maya Chen",
    handle: "@maya.codes",
    avatarGradient: "linear-gradient(135deg, #f97316, #db2777)",
    timestamp: "2h ago",
    text: "Finally got my rover pathfinding algorithm to avoid every crater on the test map. Turns out the bug was a missing dependency in my useEffect the whole time!",
    imageGradient: "linear-gradient(135deg, #0f172a, #1e3a8a, #38bdf8)",
    likes: 42,
    liked: false,
    comments: [
      { id: "c1", author: "Devon Lee", text: "This is awesome, can you share the repo?" },
      { id: "c2", author: "Priya Nair", text: "The useEffect dependency array strikes again lol" },
    ],
  },
  {
    id: "post-2",
    author: "Jordan Ruiz",
    handle: "@jordan.builds",
    avatarGradient: "linear-gradient(135deg, #10b981, #0ea5e9)",
    timestamp: "4h ago",
    text: "Shipped my first React component library today! Six components, all documented, all tested. Small steps toward being a real engineer.",
    imageGradient: "linear-gradient(135deg, #052e16, #065f46, #34d399)",
    likes: 88,
    liked: true,
    comments: [
      { id: "c3", author: "Maya Chen", text: "Congrats! Which component was the hardest?" },
    ],
  },
  {
    id: "post-3",
    author: "Aisha Osei",
    handle: "@aisha.orbit",
    avatarGradient: "linear-gradient(135deg, #7c3aed, #db2777)",
    timestamp: "6h ago",
    text: "Reminder to everyone learning React: keys on list items aren't just to silence a warning, they help React figure out which items actually changed. Huge performance difference once your lists get long.",
    imageGradient: "linear-gradient(135deg, #1e1b4b, #4c1d95, #a78bfa)",
    likes: 156,
    liked: false,
    comments: [],
  },
  {
    id: "post-4",
    author: "Sam Okafor",
    handle: "@sam.dev",
    avatarGradient: "linear-gradient(135deg, #f59e0b, #ef4444)",
    timestamp: "9h ago",
    text: "Deployed my capstone portfolio to Vercel in under five minutes. Push to main, Vercel builds it, done. Wish I'd learned this workflow years ago.",
    imageGradient: "linear-gradient(135deg, #111827, #374151, #9ca3af)",
    likes: 61,
    liked: false,
    comments: [
      { id: "c4", author: "Aisha Osei", text: "Vercel really is that easy once your build command is right." },
    ],
  },
];
