import { useState } from "react";

const GRADIENTS = [
  "linear-gradient(135deg, #f97316, #db2777)",
  "linear-gradient(135deg, #10b981, #0ea5e9)",
  "linear-gradient(135deg, #7c3aed, #db2777)",
  "linear-gradient(135deg, #f59e0b, #ef4444)",
];

function randomGradient() {
  return GRADIENTS[Math.floor(Math.random() * GRADIENTS.length)];
}

export default function ComposePost({ onPublish }) {
  const [text, setText] = useState("");

  function handleSubmit(event) {
    event.preventDefault();
    const trimmed = text.trim();
    if (trimmed === "") return;

    onPublish({
      id: `post-${Date.now()}`,
      author: "You",
      handle: "@you.orbit",
      avatarGradient: randomGradient(),
      timestamp: "just now",
      text: trimmed,
      imageGradient: null,
      likes: 0,
      liked: false,
      comments: [],
    });

    setText("");
  }

  return (
    <form className="compose-post" onSubmit={handleSubmit}>
      <textarea
        value={text}
        onChange={(event) => setText(event.target.value)}
        placeholder="Share a mission update with the crew..."
        rows={3}
      />
      <div className="compose-post-footer">
        <span className="compose-post-count">{text.length}/280</span>
        <button type="submit" disabled={text.trim() === ""}>
          Post
        </button>
      </div>
    </form>
  );
}
