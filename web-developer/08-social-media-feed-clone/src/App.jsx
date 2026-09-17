import { useState } from "react";
import ComposePost from "./components/ComposePost";
import PostCard from "./components/PostCard";
import { initialPosts } from "./data/posts";
import "./index.css";

export default function App() {
  const [posts, setPosts] = useState(initialPosts);

  function handlePublish(newPost) {
    setPosts((prev) => [newPost, ...prev]);
  }

  function handleToggleLike(postId) {
    setPosts((prev) =>
      prev.map((post) =>
        post.id === postId
          ? {
              ...post,
              liked: !post.liked,
              likes: post.liked ? post.likes - 1 : post.likes + 1,
            }
          : post
      )
    );
  }

  function handleAddComment(postId, text) {
    setPosts((prev) =>
      prev.map((post) =>
        post.id === postId
          ? {
              ...post,
              comments: [
                ...post.comments,
                { id: `c-${Date.now()}`, author: "You", text },
              ],
            }
          : post
      )
    );
  }

  return (
    <div className="feed-page">
      <header className="feed-header">
        <h1>Lumexa Orbit</h1>
        <p>See what the crew is building today.</p>
      </header>

      <ComposePost onPublish={handlePublish} />

      <div className="feed-list">
        {posts.map((post) => (
          <PostCard
            key={post.id}
            post={post}
            onToggleLike={handleToggleLike}
            onAddComment={handleAddComment}
          />
        ))}
      </div>
    </div>
  );
}
