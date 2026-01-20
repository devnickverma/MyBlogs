const API_URL = "https://myblogs-skti.onrender.com";

// DOM Elements
const authSection = document.getElementById("auth-section");
const tabLogin = document.getElementById("tab-login");
const tabSignup = document.getElementById("tab-signup");
const loginForm = document.getElementById("login-form");
const signupForm = document.getElementById("signup-form");
const logoutBtn = document.getElementById("logout-btn");
const welcomeMsg = document.getElementById("welcome-msg");
const createPostSection = document.getElementById("create-post-section");
const createPostForm = document.getElementById("create-post-form");
const postsContainer = document.getElementById("posts-container");
const refreshBtn = document.getElementById("refresh-btn");
const messageContainer = document.getElementById("message-container");

// State
let token = localStorage.getItem("access_token");

// --- Initialization ---
function init() {
    setupTabs();
    updateAuthUI();
    fetchPosts();
}

function setupTabs() {
    tabLogin.addEventListener("click", () => {
        switchTab("login");
    });
    tabSignup.addEventListener("click", () => {
        switchTab("signup");
    });
}

function switchTab(mode) {
    if (mode === "login") {
        tabLogin.classList.add("active");
        tabSignup.classList.remove("active");
        loginForm.classList.remove("hidden");
        signupForm.classList.add("hidden");
    } else {
        tabLogin.classList.remove("active");
        tabSignup.classList.add("active");
        loginForm.classList.add("hidden");
        signupForm.classList.remove("hidden");
    }
}

function updateAuthUI() {
    if (token) {
        authSection.classList.add("hidden");
        logoutBtn.classList.remove("hidden");
        welcomeMsg.classList.remove("hidden");
        welcomeMsg.textContent = "Welcome back!";
        createPostSection.classList.remove("hidden");
    } else {
        authSection.classList.remove("hidden");
        logoutBtn.classList.add("hidden");
        welcomeMsg.classList.add("hidden");
        createPostSection.classList.add("hidden");
        // Reset to login tab
        switchTab("login");
    }
}

function showMessage(msg, type = "success") {
    messageContainer.innerHTML = `<div class="message message-${type}">${msg}</div>`;
    setTimeout(() => {
        messageContainer.innerHTML = "";
    }, 5000);
}

function setLoading(btn, isLoading, text) {
    if (isLoading) {
        btn.disabled = true;
        btn.textContent = "Processing...";
    } else {
        btn.disabled = false;
        btn.textContent = text;
    }
}

// --- API Calls ---

async function login(email, password, btn) {
    setLoading(btn, true);
    
    // CRITICAL FIX: Use URLSearchParams for application/x-www-form-urlencoded
    const params = new URLSearchParams();
    params.append("username", email);
    params.append("password", password);

    try {
        const response = await fetch(`${API_URL}/token`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: params,
        });

        if (!response.ok) {
             const data = await response.json();
             throw new Error(data.detail || "Login failed");
        }

        const data = await response.json();
        token = data.access_token;
        localStorage.setItem("access_token", token);
        updateAuthUI();
        showMessage("Logged in successfully!");
    } catch (err) {
        showMessage(err.message, "error");
    } finally {
        setLoading(btn, false, "Log In");
    }
}

async function signup(email, password, btn) {
    setLoading(btn, true);
    try {
        const response = await fetch(`${API_URL}/users/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            showMessage("Account created! Please login.");
            switchTab("login");
            // Pre-fill login email
            document.getElementById("email").value = email;
            // Clear signup form
            document.getElementById("signup-email").value = "";
            document.getElementById("signup-password").value = "";
        } else {
            const data = await response.json();
            throw new Error(data.detail || "Signup failed");
        }
    } catch (err) {
        showMessage(err.message, "error");
    } finally {
        setLoading(btn, false, "Create Account");
    }
}

function logout() {
    token = null;
    localStorage.removeItem("access_token");
    updateAuthUI();
    showMessage("Logged out.");
}

async function fetchPosts() {
    postsContainer.innerHTML = '<div class="loading-spinner">Loading posts...</div>';
    try {
        const response = await fetch(`${API_URL}/posts/`);
        if (!response.ok) throw new Error("Failed to fetch posts");
        
        const posts = await response.json();
        renderPosts(posts);
    } catch (err) {
        postsContainer.innerHTML = '<div class="message message-error">Failed to load posts.</div>';
    }
}

async function createPost(title, content, btn) {
    if (!token) return;
    setLoading(btn, true);

    try {
        const response = await fetch(`${API_URL}/posts/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ title, content })
        });

        if (!response.ok) throw new Error("Failed to create post");

        showMessage("Post published!");
        createPostForm.reset();
        fetchPosts(); 
    } catch (err) {
        showMessage("Error creating post. Try again.", "error");
    } finally {
        setLoading(btn, false, "Publish Post");
    }
}

async function toggleLike(postId, isLiked) {
    if (!token) {
        showMessage("Please login to like posts", "error");
        return;
    }

    const method = isLiked ? "DELETE" : "POST";
    
    try {
        const response = await fetch(`${API_URL}/likes/`, {
            method: method,
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ post_id: postId })
        });
        
        if (response.ok) {
            fetchPosts(); 
        } else {
            const data = await response.json();
            if (response.status === 400 && data.detail) {
                 showMessage(data.detail, "error");
            }
        }
    } catch (err) {
        console.error(err);
    }
}

// --- Rendering ---

function renderPosts(posts) {
    postsContainer.innerHTML = "";
    posts.forEach(post => {
        const date = new Date(post.created_at).toLocaleDateString();
        
        const card = document.createElement("div");
        card.className = "post-card";
        card.innerHTML = `
            <div class="post-header">
                <div class="post-title">${escapeHtml(post.title)}</div>
                <div class="post-date">${date}</div>
            </div>
            <div class="post-body">${escapeHtml(post.content)}</div>
            <div class="post-footer">
                <button class="btn-icon" onclick="toggleLike(${post.id}, false)" title="Like">
                    ❤ Like
                </button>
            </div>
        `;
        postsContainer.appendChild(card);
    });
}

function escapeHtml(text) {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// --- Event Listeners ---

loginForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const btn = e.submitter;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    login(email, password, btn);
});

signupForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const btn = e.submitter;
    const email = document.getElementById("signup-email").value;
    const password = document.getElementById("signup-password").value;
    signup(email, password, btn);
});

logoutBtn.addEventListener("click", logout);

createPostForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const btn = e.submitter;
    const title = document.getElementById("post-title").value;
    const content = document.getElementById("post-content").value;
    createPost(title, content, btn);
});

refreshBtn.addEventListener("click", fetchPosts);

window.toggleLike = toggleLike; 

// Start
init();
