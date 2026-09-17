import { useState } from "react";
import CommentList from "./CommentList";

export default function PostCard({ post, onToggleLike, onAddComment }) {
  const [showComments, setShowComments] = useState(false);

  return (
    <article className="post-card">
      <header className="post-card-header">
        <div className="post-avatar" style={{ background: post.avatarGradient }} />
        <div>
          <p className="post-author">{post.author}</p>
          <p className="post-meta">
            {post.handle} &middot; {post.timestamp}
          </p>
        </div>
      </header>

      <p className="post-text">{post.text}</p>

      {post.imageGradient && (
        <div className="post-image" style={{ background: post.imageGradient }} />
      )}

      <div className="post-actions">
        <button
          type="button"
          className={`like-button ${post.liked ? "like-button--active" : ""}`}
          onClick={() => onToggleLike(post.id)}
        >
          {post.liked ? "♥" : "♡"} {post.likes}
        </button>
        <button
          type="button"
          className="comment-toggle"
          onClick={() => setShowComments((prev) => !prev)}
        >
          💬 {post.comments.length}
        </button>
      </div>

      {showComments && (
        <CommentList
          comments={post.comments}
          onAddComment={(text) => onAddComment(post.id, text)}
        />
      )}
    </article>
  );
}
