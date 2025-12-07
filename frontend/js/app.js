// Main application logic

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    Navigation.init();
    setupEventListeners();
    updateNavigationVisibility();
});

// Setup all event listeners
function setupEventListeners() {
    // Login form
    document.getElementById('login-form').addEventListener('submit', handleLogin);
    
    // Signin form
    document.getElementById('signin-form').addEventListener('submit', handleSignin);
    document.getElementById('signin-image').addEventListener('change', (e) => {
        previewImage(e.target, 'signin-image-preview');
    });
    
    // Make post form
    document.getElementById('makepost-form').addEventListener('submit', handleMakePost);
    document.getElementById('makepost-image').addEventListener('change', (e) => {
        previewImage(e.target, 'makepost-image-preview');
    });
    
    // Edit post form
    document.getElementById('editpost-form').addEventListener('submit', handleEditPost);
    document.getElementById('editpost-image').addEventListener('change', (e) => {
        previewImage(e.target, 'editpost-image-preview');
    });
    
    // Edit profile form
    document.getElementById('editprofile-form').addEventListener('submit', handleEditProfile);
    document.getElementById('editprofile-image').addEventListener('change', (e) => {
        previewImage(e.target, 'profile-image-preview');
    });
    
    // Edit password form
    document.getElementById('editpassword-form').addEventListener('submit', handleEditPassword);
}

// Handle login
async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const alertDiv = document.getElementById('login-alert');
    
    try {
        const result = await API.login(email, password);
        // Store user info - result contains user object
        if (result && result.user) {
            Auth.setCurrentUser(result.user);
            showAlert(alertDiv, result.message || 'Login successful!', 'success');
            updateNavigationVisibility();
            setTimeout(() => {
                Navigation.redirectTo('posts');
            }, 1000);
        } else {
            showAlert(alertDiv, 'Login failed: Invalid response', 'error');
        }
    } catch (error) {
        showAlert(alertDiv, error.message || 'Login failed', 'error');
    }
}

// Handle signin/register
async function handleSignin(e) {
    e.preventDefault();
    const formData = new FormData();
    const email = document.getElementById('signin-email').value;
    const password = document.getElementById('signin-password').value;
    const passwordConfirm = document.getElementById('signin-password-confirm').value;
    const nickname = document.getElementById('signin-nickname').value;
    const imageFile = document.getElementById('signin-image').files[0];
    
    const alertDiv = document.getElementById('signin-alert');
    
    formData.append('email', email);
    formData.append('password', password);
    formData.append('password_confirm', passwordConfirm);
    formData.append('nickname', nickname);
    if (imageFile) {
        formData.append('image', imageFile);
    }
    
    try {
        const result = await API.signin(formData);
        if (result && result.success) {
            Auth.setCurrentUser({ email, nickname, ...(result.data || {}) });
            showAlert(alertDiv, result.message || 'Sign up successful!', 'success');
            updateNavigationVisibility();
            setTimeout(() => {
                Navigation.redirectTo('posts');
            }, 1000);
        } else {
            const errorMsg = result?.message || 'Sign up failed. Please check your input.';
            showAlert(alertDiv, errorMsg, 'error');
        }
    } catch (error) {
        console.error('Signup error:', error);
        const errorMsg = error.message || 'Sign up failed. Please try again.';
        showAlert(alertDiv, errorMsg, 'error');
    }
}

// Handle logout
function handleLogout() {
    Auth.clearCurrentUser();
    updateNavigationVisibility();
    Navigation.redirectTo('login');
}

// Load posts
async function loadPosts() {
    const container = document.getElementById('posts-container');
    try {
        // Try the makepost router endpoint first (DB posts)
        const posts = await API.get('/posts/');
        if (!posts || posts.length === 0) {
            container.innerHTML = '<div class="empty-state"><h3>No posts yet</h3><p>Be the first to create a post!</p></div>';
            return;
        }
        
        container.innerHTML = posts.map(post => {
            const content = post.content || '';
            const imageUrl = post.image_filename || post.image_url || null;
            return `
                <div class="post-card">
                    <div onclick="viewPost(${post.id})" style="cursor: pointer;">
                        <h3>${escapeHtml(post.title || 'Untitled')}</h3>
                        <div class="post-meta">
                            <span>Created: ${formatDate(post.created_at)}</span>
                        </div>
                        ${imageUrl ? `<img src="http://localhost:8000/uploaded_images/${imageUrl}" class="post-image" alt="Post image">` : ''}
                        <p style="margin-top: 1rem; color: #666;">${escapeHtml(content.substring(0, 150))}${content.length > 150 ? '...' : ''}</p>
                    </div>
                    <div class="post-actions" style="margin-top: 0.5rem; display: flex; gap: 0.5rem;">
                        <button class="btn btn-secondary" onclick="event.stopPropagation(); loadEditPostPage(${post.id})">Edit</button>
                    </div>
                </div>
            `;
        }).join('');
    } catch (error) {
        console.error('Error loading posts from makepost router:', error);
        // Fallback to posts_router endpoint
        try {
            const posts = await API.getPosts();
            if (!posts || posts.length === 0) {
                container.innerHTML = '<div class="empty-state"><h3>No posts yet</h3><p>Be the first to create a post!</p></div>';
                return;
            }
            
            container.innerHTML = posts.map(post => `
                <div class="post-card" onclick="viewPost(${post.id})">
                    <h3>${escapeHtml(post.title || 'Untitled')}</h3>
                    <div class="post-meta">
                        <span>Comments: ${post.comments_count || 0}</span>
                        <span>Views: ${post.views_count || 0}</span>
                        <span>Created: ${formatDate(post.created_at)}</span>
                    </div>
                </div>
            `).join('');
        } catch (err) {
            console.error('Error loading posts from posts_router:', err);
            const errorMsg = err.message || 'Unknown error';
            container.innerHTML = `<div class="alert alert-error">Failed to load posts: ${errorMsg}<br><small>Check console for details</small></div>`;
        }
    }
}

// View single post
async function viewPost(postId) {
    Navigation.redirectTo('post');
    const container = document.getElementById('post-detail');
    
    // Store postId in sessionStorage for page reload
    sessionStorage.setItem('currentPostId', postId);
    
    try {
        const post = await API.getPost(postId);
        const imageUrl = post.image_filename || post.image_url || null;
        container.innerHTML = `
            <h1>${escapeHtml(post.title)}</h1>
            <div class="post-stats">
                <span>Views: ${post.views || 0}</span>
                <span>Likes: ${post.likes || 0}</span>
            </div>
            ${imageUrl ? `<img src="http://localhost:8000/uploaded_images/${imageUrl}" class="post-image" alt="Post image">` : ''}
            <div class="post-content">${escapeHtml(post.content || '')}</div>
            <div class="post-actions">
                <button class="like-btn ${post.liked ? 'liked' : ''}" onclick="toggleLike(${post.id})">
                    ${post.liked ? '❤️ Liked' : '🤍 Like'} (${post.likes || 0})
                </button>
                <button class="btn btn-secondary" onclick="Navigation.redirectTo('posts')">Back to Posts</button>
            </div>
            <div class="comments-section">
                <h3>Comments</h3>
                <form class="comment-form" onsubmit="addComment(event, ${post.id})">
                    <textarea name="content" required placeholder="Write a comment..."></textarea>
                    <button type="submit" class="btn btn-primary" style="margin-top: 0.5rem;">Add Comment</button>
                </form>
                <div class="comments-list" id="comments-${post.id}">
                    ${post.comments && post.comments.length > 0 ? post.comments.map(comment => `
                        <div class="comment">
                            <div class="comment-header">
                                <span>${formatDate(comment.created_at)}</span>
                                <div class="comment-actions">
                                    <button onclick="editComment(${comment.id}, '${escapeHtml(comment.content)}')">Edit</button>
                                    <button onclick="deleteComment(${comment.id}, ${post.id})">Delete</button>
                                </div>
                            </div>
                            <div class="comment-content" id="comment-content-${comment.id}">${escapeHtml(comment.content)}</div>
                        </div>
                    `).join('') : '<p>No comments yet</p>'}
                </div>
            </div>
        `;
    } catch (error) {
        container.innerHTML = `<div class="alert alert-error">Failed to load post: ${error.message}</div>`;
    }
}

// Toggle like
async function toggleLike(postId) {
    try {
        const result = await API.toggleLike(postId);
        // Reload post to update UI
        viewPost(postId);
    } catch (error) {
        alert('Failed to toggle like: ' + error.message);
    }
}

// Add comment
async function addComment(e, postId) {
    e.preventDefault();
    const form = e.target;
    const content = form.content.value;
    
    try {
        await API.addComment(postId, content);
        form.reset();
        viewPost(postId); // Reload post to show new comment
    } catch (error) {
        alert('Failed to add comment: ' + error.message);
    }
}

// Edit comment
async function editComment(commentId, currentContent) {
    const newContent = prompt('Edit comment:', currentContent);
    if (newContent && newContent !== currentContent) {
        try {
            await API.updateComment(commentId, newContent);
            const postId = sessionStorage.getItem('currentPostId');
            if (postId) {
                viewPost(parseInt(postId));
            }
        } catch (error) {
            alert('Failed to update comment: ' + error.message);
        }
    }
}

// Delete comment
async function deleteComment(commentId, postId) {
    if (!confirm('Are you sure you want to delete this comment?')) {
        return;
    }
    
    try {
        await API.deleteComment(commentId);
        viewPost(postId);
    } catch (error) {
        alert('Failed to delete comment: ' + error.message);
    }
}

// Handle make post
async function handleMakePost(e) {
    e.preventDefault();
    const title = document.getElementById('makepost-title').value;
    const content = document.getElementById('makepost-content').value;
    const imageFile = document.getElementById('makepost-image').files[0];
    const alertDiv = document.getElementById('makepost-alert');
    
    try {
        await API.createPost(title, content, imageFile);
        showAlert(alertDiv, 'Post created successfully!', 'success');
        setTimeout(() => {
            Navigation.redirectTo('posts');
        }, 1000);
    } catch (error) {
        showAlert(alertDiv, error.message || 'Failed to create post', 'error');
    }
}

// Load edit post page with existing post data
async function loadEditPostPage(postId) {
    // Store postId for after navigation
    window._pendingEditPostId = postId;
    sessionStorage.setItem('editingPostId', postId);
    
    // Navigate to editpost page
    Navigation.redirectTo('editpost');
    
    // Wait for navigation, then load data
    // Use hashchange event to know when navigation is complete
    const loadDataAfterNavigation = async () => {
        // Wait a bit more for DOM to be ready
        await new Promise(resolve => setTimeout(resolve, 200));
        
        try {
            const postIdToLoad = window._pendingEditPostId || sessionStorage.getItem('editingPostId');
            if (!postIdToLoad) {
                console.error('No post ID found to load');
                return;
            }
            
            const post = await API.getPost(postIdToLoad);
            
            // Get form fields - query the page element directly first
            const pageEl = document.getElementById('editpost-page');
            let postIdField = null;
            
            if (pageEl) {
                // Try to find the element within the page
                postIdField = pageEl.querySelector('#editpost-post-id') || 
                             pageEl.querySelector('input[id="editpost-post-id"]');
            }
            
            // If not found in page, try global query
            if (!postIdField) {
                postIdField = document.getElementById('editpost-post-id');
            }
            
            // Poll a few more times if still not found
            let attempts = 0;
            while (!postIdField && attempts < 20) {
                await new Promise(resolve => setTimeout(resolve, 100));
                const page = document.getElementById('editpost-page');
                if (page) {
                    postIdField = page.querySelector('#editpost-post-id');
                }
                if (!postIdField) {
                    postIdField = document.getElementById('editpost-post-id');
                }
                attempts++;
            }
            
            const titleField = document.getElementById('editpost-title');
            const contentField = document.getElementById('editpost-content');
            const imagePreview = document.getElementById('editpost-image-preview');
            
            // Verify elements exist with detailed debugging
            if (!postIdField) {
                const pageEl = document.getElementById('editpost-page');
                const formEl = document.getElementById('editpost-form');
                const allInputs = pageEl ? Array.from(pageEl.querySelectorAll('input')).map(i => ({id: i.id, type: i.type, name: i.name})) : [];
                
                console.error('editpost-post-id not found after', attempts, 'attempts. Detailed debug:', {
                    pageExists: !!pageEl,
                    pageVisible: pageEl ? window.getComputedStyle(pageEl).display : 'N/A',
                    pageHasActiveClass: pageEl ? pageEl.classList.contains('active') : false,
                    formExists: !!formEl,
                    allInputs: allInputs,
                    hash: window.location.hash,
                    currentPage: Navigation.currentPage
                });
                
                const alertDiv = document.getElementById('editpost-alert');
                if (alertDiv) {
                    showAlert(alertDiv, 'Failed to load edit form. Please refresh the page.', 'error');
                } else {
                    alert('Failed to load edit form. Please refresh the page.');
                }
                return;
            }
            if (!titleField) {
                throw new Error('Title field not found');
            }
            if (!contentField) {
                throw new Error('Content field not found');
            }
            
            // Set form values
            postIdField.value = post.id || postIdToLoad;
            titleField.value = post.title || '';
            contentField.value = post.content || '';
            
            // Show existing image if any
            const imageUrl = post.image_filename || post.image_url || null;
            if (imagePreview) {
                if (imageUrl) {
                    imagePreview.src = `http://localhost:8000/uploaded_images/${imageUrl}`;
                    imagePreview.style.display = 'block';
                } else {
                    imagePreview.style.display = 'none';
                }
            }
            
            delete window._pendingEditPostId;
        } catch (error) {
            console.error('Error loading edit post:', error);
            const alertDiv = document.getElementById('editpost-alert');
            if (alertDiv) {
                showAlert(alertDiv, error.message || 'Failed to load post data', 'error');
            }
        }
    };
    
    // Set up hashchange listener to load data when navigation completes
    const hashHandler = () => {
        if (window.location.hash === '#editpost') {
            window.removeEventListener('hashchange', hashHandler);
            loadDataAfterNavigation();
        }
    };
    window.addEventListener('hashchange', hashHandler);
    
    // Also try loading immediately in case we're already on the page
    setTimeout(loadDataAfterNavigation, 300);
}

// Handle edit post
async function handleEditPost(e) {
    e.preventDefault();
    const postId = document.getElementById('editpost-post-id').value;
    const title = document.getElementById('editpost-title').value;
    const content = document.getElementById('editpost-content').value;
    const imageFile = document.getElementById('editpost-image').files[0];
    const alertDiv = document.getElementById('editpost-alert');
    
    if (!postId) {
        showAlert(alertDiv, 'Post ID is missing', 'error');
        return;
    }
    
    try {
        await API.updatePost(postId, title, content, imageFile);
        showAlert(alertDiv, 'Post updated successfully!', 'success');
        setTimeout(() => {
            Navigation.redirectTo('posts');
        }, 1000);
    } catch (error) {
        showAlert(alertDiv, error.message || 'Failed to update post', 'error');
    }
}

// Handle edit profile
async function handleEditProfile(e) {
    e.preventDefault();
    const nickname = document.getElementById('editprofile-nickname').value;
    const imageFile = document.getElementById('editprofile-image').files[0];
    const alertDiv = document.getElementById('editprofile-alert');
    const user = Auth.getCurrentUser();
    
    if (!user || !user.email) {
        showAlert(alertDiv, 'Please login first', 'error');
        return;
    }
    
    try {
        // Use the /user/edit endpoint which handles both signup and profile updates
        const formData = new FormData();
        formData.append('email', user.email);
        // Don't send password for profile updates - it's optional
        formData.append('nickname', nickname);
        if (imageFile) {
            formData.append('image', imageFile);
        }
        
        const result = await API.updateProfile(formData);
        if (result && result.success) {
            // Update stored user data
            Auth.setCurrentUser({ ...user, nickname: nickname, ...(result.data || {}) });
            showAlert(alertDiv, result.message || 'Profile updated successfully!', 'success');
            updateNavigationVisibility();
        } else {
            showAlert(alertDiv, result?.message || 'Failed to update profile', 'error');
        }
    } catch (error) {
        console.error('Profile update error:', error);
        const errorMsg = error.message || 'Failed to update profile';
        showAlert(alertDiv, errorMsg, 'error');
    }
}

// Handle edit password
async function handleEditPassword(e) {
    e.preventDefault();
    const password = document.getElementById('editpassword-password').value;
    const passwordConfirm = document.getElementById('editpassword-password-confirm').value;
    const alertDiv = document.getElementById('editpassword-alert');
    const user = Auth.getCurrentUser();
    
    // Check if user is logged in and has email
    if (!user) {
        showAlert(alertDiv, 'Please login first', 'error');
        return;
    }
    
    // Get email from user object - check multiple possible locations
    const email = user.email || (user.user && user.user.email);
    
    console.log('User object:', user);
    console.log('Email extracted:', email);
    
    if (!email || typeof email !== 'string' || email.trim() === '') {
        console.error('Email validation failed. User object:', user);
        showAlert(alertDiv, 'User email not found. Please login again.', 'error');
        return;
    }
    
    try {
        console.log('Calling API.changePassword with email:', email);
        const result = await API.changePassword(email.trim(), password, passwordConfirm);
        if (result.success) {
            showAlert(alertDiv, result.message || 'Password changed successfully!', 'success');
            setTimeout(() => {
                Navigation.redirectTo('editprofile');
            }, 1000);
        } else {
            showAlert(alertDiv, result.message || 'Failed to change password', 'error');
        }
    } catch (error) {
        console.error('Password change error:', error);
        showAlert(alertDiv, error.message || 'Failed to change password', 'error');
    }
}

// Handle delete user
async function handleDeleteUser() {
    if (!confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
        return;
    }
    
    const user = Auth.getCurrentUser();
    if (!user || !user.email) {
        alert('Please login first');
        return;
    }
    
    try {
        const result = await API.deleteUser(user.email);
        if (result && result.success) {
            alert('Account deleted successfully');
            handleLogout();
        } else {
            alert(result?.message || 'Failed to delete account');
        }
    } catch (error) {
        alert('Failed to delete account: ' + error.message);
    }
}

// Update navigation visibility based on auth status
function updateNavigationVisibility() {
    const isAuth = Auth.isAuthenticated();
    const user = Auth.getCurrentUser();
    
    // Show/hide nav links
    document.getElementById('nav-login').style.display = isAuth ? 'none' : 'inline-block';
    document.getElementById('nav-signin').style.display = isAuth ? 'none' : 'inline-block';
    document.getElementById('nav-posts').style.display = isAuth ? 'inline-block' : 'none';
    document.getElementById('nav-makepost').style.display = isAuth ? 'inline-block' : 'none';
    document.getElementById('nav-profile').style.display = isAuth ? 'inline-block' : 'none';
    
    // Show/hide user info
    const userInfo = document.getElementById('user-info');
    if (isAuth && user) {
        userInfo.style.display = 'flex';
        document.getElementById('user-name').textContent = user.nickname || user.email || 'User';
    } else {
        userInfo.style.display = 'none';
    }
}

// Show alert
function showAlert(container, message, type) {
    container.innerHTML = `<div class="alert alert-${type}">${escapeHtml(message)}</div>`;
    setTimeout(() => {
        container.innerHTML = '';
    }, 5000);
}

// Preview image
function previewImage(input, previewId) {
    const file = input.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const preview = document.getElementById(previewId);
            preview.src = e.target.result;
            preview.classList.add('show');
        };
        reader.readAsDataURL(file);
    }
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Override Navigation.showPage to load data when needed
const originalShowPage = Navigation.showPage;
Navigation.showPage = function(page) {
    originalShowPage.call(this, page);
    
    // Load data when page is shown
    if (page === 'posts') {
        loadPosts();
    } else if (page === 'editprofile') {
        loadProfile();
    } else if (page === 'post') {
        const postId = sessionStorage.getItem('currentPostId');
        if (postId) {
            viewPost(parseInt(postId));
        }
    }
};

// Load profile data
function loadProfile() {
    const user = Auth.getCurrentUser();
    if (user) {
        document.getElementById('editprofile-nickname').value = user.nickname || '';
        if (user.profile_image) {
            const img = document.getElementById('profile-image-preview');
            img.src = `http://localhost:8000/uploaded_images/${user.profile_image}`;
            img.style.display = 'block';
        }
    }
}

