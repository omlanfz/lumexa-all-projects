import { useState } from "react";

export default function CommentList({ comments, onAddComment }) {
  const [draft, setDraft] = useState("");

  function handleSubmit(event) {
    event.preventDefault();
    const trimmed = draft.trim();
    if (trimmed === "") return;
    onAddComment(trimmed);
    setDraft("");
  }

  return (
    <div className="comment-list">
      {comments.length > 0 && (
        <ul>
          {comments.map((comment) => (
            <li key={comment.id}>
              <strong>{comment.author}</strong> {comment.text}
            </li>
          ))}
        </ul>
      )}
      <form className="comment-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          placeholder="Write a comment..."
        />
        <button type="submit" disabled={draft.trim() === ""}>
          Reply
        </button>
      </form>
    </div>
  );
}
