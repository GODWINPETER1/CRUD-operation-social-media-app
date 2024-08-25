// This file handle all the api requests
import axios from "axios";

// set the base URL for the API
const api = axios.create({
    baseURL: 'http://127.0.0.1:8000' // from the backend
})

// Get all posts
export const fetchPosts = async () => {
    const response = await api.get('/posts');
    return response.data.data
}

// create the data
export const createPosts = async (post: {name: string ; price: number ; inventory: number}) => {
    const response = await api.post("/posts" , post);
    console.log(response.data.data)
    return response.data.data
}

// get a single data
export const getData = async (id: number) => {
    const response = await api.get(`/posts/${id}`)
    return response.data.data
}

// update a post by ID
export const updatePost = async (id: number , post: {name: string ; price: number ; inventory: number}) => {
    const response = await api.put(`/posts/${id}` , post)
    return response.data.data 
}

// delete the post by id
export const deletePost = async (id: number) => {
    const response = await api.delete(`/posts/${id}`)
    return response.data.data 
}