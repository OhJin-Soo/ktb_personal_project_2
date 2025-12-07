// Authentication utility
const Auth = {
    // Get current user from localStorage
    getCurrentUser() {
        const userStr = localStorage.getItem('currentUser');
        return userStr ? JSON.parse(userStr) : null;
    },

    // Set current user in localStorage
    setCurrentUser(user) {
        localStorage.setItem('currentUser', JSON.stringify(user));
    },

    // Clear current user (logout)
    clearCurrentUser() {
        localStorage.removeItem('currentUser');
    },

    // Check if user is authenticated
    isAuthenticated() {
        return this.getCurrentUser() !== null;
    },

    // Get auth token (if using JWT in future)
    getToken() {
        const user = this.getCurrentUser();
        return user ? user.token : null;
    }
};

