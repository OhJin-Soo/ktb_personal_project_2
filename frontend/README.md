# Frontend Application

This is a vanilla JavaScript frontend application for the Community Web backend.

## Features

The application includes 8 pages:

1. **Login Page** - User authentication
2. **Sign Up Page** - User registration
3. **Posts List Page** - Display all posts
4. **Post Detail Page** - View single post with comments
5. **Make Post Page** - Create new posts
6. **Edit Post Page** - Edit existing posts
7. **Edit Profile Page** - Update user profile
8. **Edit Password Page** - Change password

## Setup

1. Make sure the FastAPI backend is running on `http://localhost:8000`
2. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
3. Open your browser and navigate to `http://localhost:8000/`
   - Or open `http://localhost:8000/static/index.html` if the root route doesn't work

## File Structure

```
frontend/
├── index.html          # Main HTML file with all pages
├── css/
│   └── style.css      # Main stylesheet
├── js/
│   ├── auth.js        # Authentication utilities
│   ├── api.js         # API communication utilities
│   ├── navigation.js  # Navigation/routing utilities
│   └── app.js         # Main application logic
└── README.md          # This file
```

## Usage

1. **Sign Up**: Click "Sign Up" to create a new account
2. **Login**: Use your credentials to login
3. **View Posts**: After logging in, you'll see the posts list
4. **Create Post**: Click "New Post" to create a post
5. **View Post**: Click on any post card to view details
6. **Edit Profile**: Access your profile settings from the navigation
7. **Change Password**: Use the profile page to change your password

## Authentication

The application uses localStorage to store user authentication state. When you log in or sign up, your user information is stored in the browser's localStorage.

## API Integration

All API calls are made to the FastAPI backend endpoints. Make sure CORS is properly configured in the backend if you encounter any cross-origin issues.

