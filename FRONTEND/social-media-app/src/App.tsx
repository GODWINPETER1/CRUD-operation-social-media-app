// App.tsx
import React, { useState, useEffect } from 'react';
import { fetchPosts, createPosts, updatePost, deletePost } from './service';
import { Post } from './types';

const App: React.FC = () => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [editingPost, setEditingPost] = useState<Post | null>(null);
  const [newPost, setNewPost] = useState<Omit<Post, 'id'>>({ name: '', price: 0, inventory: 0 });
  console.log(newPost)

  useEffect(() => {
    loadPosts();
  }, []);

  const loadPosts = async () => {
    const fetchedPosts = await fetchPosts();
    setPosts(fetchedPosts);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setNewPost((prevPost) => ({
      ...prevPost,
      [name]: value,
    }));
  };

  const handleCreate = async () => {
    try {
      const createdPost = await createPosts(newPost as Post);
      setPosts([...posts, createdPost]);
      setNewPost({ name: '', price: 0, inventory: 0 });
    } catch (error) {
      console.error("Error creating post:", error);
    }
  };
  

  const handleUpdate = async (id: number) => {
    if (editingPost) {
      const updatedPost = await updatePost(id, editingPost);
      setPosts(posts.map(post => (post.id === id ? updatedPost : post)));
      setEditingPost(null);
    }
  };

  const handleDelete = async (id: number) => {
    await deletePost(id);
    setPosts(posts.filter(post => post.id !== id));
  };

  return (
    <div className="container">
      <h1>CRUD Table</h1>
      <button onClick={() => setEditingPost({ id: 0, name: '', price: 0, inventory: 0 })}>
        Create New Post
      </button>
      {editingPost && (
        <div className="modal">
          <input
            type="text"
            placeholder="Name"
            value={editingPost.name}
            onChange={handleInputChange}
          />
          <input
            type="number"
            placeholder="Price"
            value={editingPost.price}
            onChange={handleInputChange}
          />
          <input
            type="number"
            placeholder="Inventory"
            value={editingPost.inventory}
            onChange={handleInputChange}
          />
          <button onClick={() => (editingPost.id === 0 ? handleCreate() : handleUpdate(editingPost.id))}>
            {editingPost.id === 0 ? 'Create' : 'Update'}
          </button>
          <button onClick={() => setEditingPost(null)}>Cancel</button>
        </div>
      )}
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Price</th>
            <th>Inventory</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {posts.map(post => (
            <tr key={post.id}>
              <td>{post.name}</td>
              <td>{post.price}</td>
              <td>{post.inventory}</td>
              <td>
                <button onClick={() => setEditingPost(post)}>Edit</button>
                <button onClick={() => handleDelete(post.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default App;
