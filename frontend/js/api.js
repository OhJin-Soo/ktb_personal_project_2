// API utility for backend communication
const API = {
    baseURL: 'http://localhost:8000', // FastAPI default port

    // Generic request method
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            ...options,
            headers: {
                'Accept': 'application/json',
                ...options.headers
            }
        };

        try {
            const response = await fetch(url, config);
            
            // Check if response is JSON
            const contentType = response.headers.get("content-type");
            if (!contentType || !contentType.includes("application/json")) {
                const text = await response.text();
                console.error('Non-JSON response:', text);
                // For 404 errors, provide more helpful message
                if (response.status === 404) {
                    throw new Error('요청한 리소스를 찾을 수 없습니다. (404)');
                }
                throw new Error('서버에서 JSON이 아닌 응답을 받았습니다. 서버 오류일 수 있습니다.');
            }
            
            const data = await response.json();
            
            if (!response.ok) {
                // Handle error response
                const errorMessage = data.detail || data.message || data.error || `Request failed (${response.status})`;
                throw new Error(errorMessage);
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            // If it's already an Error with a message, re-throw it
            if (error instanceof Error) {
                throw error;
            }
            // Otherwise, wrap it
            throw new Error(error.message || '요청 처리 중 오류가 발생했습니다.');
        }
    },

    // GET request
    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    },

    // POST request with FormData
    async postForm(endpoint, formData) {
        return this.request(endpoint, {
            method: 'POST',
            body: formData
        });
    },

    // PUT request with FormData
    async putForm(endpoint, formData) {
        return this.request(endpoint, {
            method: 'PUT',
            body: formData
        });
    },

    // POST request with JSON
    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
    },

    // PUT request with FormData
    async putForm(endpoint, formData) {
        return this.request(endpoint, {
            method: 'PUT',
            body: formData
        });
    },

    // DELETE request
    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    },

    // Auth endpoints
    async login(email, password) {
        const formData = new FormData();
        formData.append('email', email);
        formData.append('password', password);
        return this.postForm('/auth/login', formData);
    },

    async signin(formData) {
        return this.postForm('/user/edit', formData);
    },

    // Post endpoints
    async getPosts(skip = 0, limit = 10) {
        return this.get(`/posts/?skip=${skip}&limit=${limit}`);
    },

    async getPost(postId) {
        return this.get(`/posts/${postId}`);
    },

    async createPost(title, content, imageFile = null) {
        const formData = new FormData();
        formData.append('title', title);
        formData.append('content', content);
        if (imageFile) {
            formData.append('image', imageFile);
        }
        return this.postForm('/posts/', formData);
    },

    async updatePost(postId, title, content) {
        const formData = new FormData();
        formData.append('title', title);
        formData.append('content', content);
        return this.putForm(`/posts/${postId}`, formData);
    },

    async deletePost(postId) {
        return this.delete(`/posts/${postId}`);
    },

    async toggleLike(postId) {
        // POST request without body
        return this.request(`/posts/${postId}/like`, { method: 'POST' });
    },

    async addComment(postId, content) {
        const formData = new FormData();
        formData.append('content', content);
        return this.postForm(`/posts/${postId}/comments`, formData);
    },

    async updateComment(commentId, content) {
        const formData = new FormData();
        formData.append('content', content);
        return this.putForm(`/posts/comments/${commentId}`, formData);
    },

    async deleteComment(commentId) {
        return this.delete(`/posts/comments/${commentId}`);
    },

    // User endpoints
    async updateProfile(formData) {
        return this.postForm('/user/edit', formData);
    },

    async changeProfileImage(username, imageUrl) {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('image_url', imageUrl);
        return this.postForm('/user/profile-image', formData);
    },

    async updateNickname(username, newNickname) {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('new_nickname', newNickname);
        return this.postForm('/user/nickname', formData);
    },

    async deleteUser(email) {
        const formData = new FormData();
        formData.append('email', email);
        formData.append('confirm', 'true');
        return this.postForm('/user/delete', formData);
    },

    async changePassword(email, password, passwordConfirm) {
        // Validate email is provided and is a string
        if (!email || typeof email !== 'string' || email.trim() === '') {
            throw new Error('Email is required to change password');
        }
        
        const formData = new FormData();
        formData.append('email', String(email).trim());
        formData.append('password', password || '');
        formData.append('password_confirm', passwordConfirm || '');
        
        return this.postForm('/user/change', formData);
    },

    // Edit post endpoint
    async updatePost(postId, title, content, imageFile = null) {
        const formData = new FormData();
        formData.append('title', title);
        formData.append('content', content);
        if (imageFile) {
            formData.append('image', imageFile);
        }
        return this.putForm(`/posts/${postId}`, formData);
    },
    
    async editPost(fileName, title, content, version, imageFile = null) {
        // Legacy method - kept for backward compatibility
        const formData = new FormData();
        formData.append('file_name', fileName);
        formData.append('title', title);
        formData.append('content', content);
        formData.append('version', version);
        if (imageFile) {
            formData.append('image', imageFile);
        }
        return this.postForm('/posts/edit', formData);
    }
};

