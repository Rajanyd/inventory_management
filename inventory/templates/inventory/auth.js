// auth.js

// Retrieve the token from localStorage
const token = localStorage.getItem('jwt_token');

// Check if the user is authenticated
function isAuthenticated() {
    if (!token) {
        redirectToLogin();
        return false;
    }
    return true;
}

// Redirect to login page if not authenticated
function redirectToLogin() {
    alert('You are not logged in. Redirecting to login page.');
    window.location.href = '/login/';
}

// Axios configuration to include the token in headers
axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

// Export functions if using a module system
// module.exports = { isAuthenticated, redirectToLogin };
