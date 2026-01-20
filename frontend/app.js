const API_URL = "https://myblogs-skti.onrender.com";

// DOM Elements
const authModal = new bootstrap.Modal(document.getElementById('authModal'));
const loginTriggerBtn = document.getElementById('login-trigger-btn');
const signupTriggerBtn = document.getElementById('signup-trigger-btn');
const heroSection = document.getElementById('hero-section');

const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');
const loginTab = document.getElementById('login-tab');
const signupTab = document.getElementById('signup-tab');

const logoutBtn = document.getElementById('logout-btn');
const welcomeMsg = document.getElementById('welcome-msg');

const createPostSection = document.getElementById('create-post-section');
const createPostForm = document.getElementById('create-post-form');

const postsContainer = document.getElementById('posts-container');
const refreshBtn = document.getElementById('refresh-btn');
const toastContainer = document.querySelector('.toast-container');

// State
let token = localStorage.getItem("access_token");

// --- Initialization ---
function init() {
    setupAuthTriggers();
    updateAuthUI();
    fetchPosts();
}

// --- Auth Modal Triggers ---
function setupAuthTriggers() {
    loginTriggerBtn.addEventListener('click', () => {
        loginTab.click(); // Switch to login tab
        authModal.show();
    });
    
    signupTriggerBtn.addEventListener('click', () => {
        signupTab.click(); // Switch to signup tab
        authModal.show();
    });
}

// Password toggle
window.togglePassword = (fieldId) => {
    const field = document.getElementById(fieldId);
    const icon = document.getElementById(`${fieldId}-icon`);
    
    if (field.type === 'password') {
        field.type = 'text';
        icon.classList.remove('bi-eye');
        icon.classList.add('bi-eye-slash');
    } else {
        field.type = 'password';
        icon.classList.remove('bi-eye-slash');
        icon.classList.add('bi-eye');
    }
};

// --- UI State ---
function updateAuthUI() {
    if (token) {
        // Logged in
        heroSection.classList.add('d-none');
        loginTriggerBtn.classList.add('d-none');
        signupTriggerBtn.classList.add('d-none');
        
        logoutBtn.classList.remove('d-none');
        welcomeMsg.classList.remove('d-none');
        welcomeMsg.textContent = 'Welcome back';
        
        createPostSection.classList.remove('d-none');
    } else {
        // Logged out
        heroSection.classList.remove('d-none');
        loginTriggerBtn.classList.remove('d-none');
        signupTriggerBtn.classList.remove('d-none');
        
        logoutBtn.classList.add('d-none');
        welcomeMsg.classList.add('d-none');
        
        createPostSection.classList.add('d-none');
    }
}

// --- Toast Notifications ---
function showToast(message, type = "success") {
    const bgClass = type === "success" ? "text-bg-success" : "text-bg-danger";
    
    const toastHtml = `
        <div class="toast align-items-center ${bgClass} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">${escapeHtml(message)}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    const div = document.createElement('div');
    div.innerHTML = toastHtml;
    const toastEl = div.firstElementChild;
    toastContainer.appendChild(toastEl);
    
    const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
    toast.show();
    
    toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
}

function toggleLoading(btn, isLoading) {
    const spinner = btn.querySelector('.spinner-border');
    const text = btn.querySelector('.btn-text');
    
    if (isLoading) {
        btn.disabled = true;
        spinner.classList.remove('d-none');
        text.classList.add('invisible');
    } else {
        btn.disabled = false;
        spinner.classList.add('d-none');
        text.classList.remove('invisible');
    }
}

// --- API Calls ---
async function login(email, password, btn) {
    toggleLoading(btn, true);
    
    const params = new URLSearchParams();
    params.append("username", email);
    params.append("password", password);

    try {
        const response = await fetch(`${API_URL}/token`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: params,
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || "Login failed");
        }

        const data = await response.json();
        token = data.access_token;
        localStorage.setItem("access_token", token);
        
        authModal.hide();
        updateAuthUI();
        showToast("Logged in successfully");
        
        loginForm.reset();
    } catch (err) {
        showToast(err.message, "error");
    } finally {
        toggleLoading(btn, false);
    }
}

async function signup(email, password, btn) {
    toggleLoading(btn, true);
    
    try {
        const response = await fetch(`${API_URL}/users/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            showToast("Account created! Please log in.");
            loginTab.click();
            document.getElementById('email').value = email;
            signupForm.reset();
        } else {
            const data = await response.json();
            throw new Error(data.detail || "Signup failed");
        }
    } catch (err) {
        showToast(err.message, "error");
    } finally {
        toggleLoading(btn, false);
    }
}

function logout() {
    token = null;
    localStorage.removeItem("access_token");
    updateAuthUI();
    showToast("Logged out");
}

async function fetchPosts() {
    try {
        const response = await fetch(`${API_URL}/posts/`);
        if (!response.ok) throw new Error("Failed to fetch posts");
        
        const posts = await response.json();
        renderPosts(posts);
    } catch (err) {
        postsContainer.innerHTML = `
            <div class="alert alert-danger alert-sm">
                Failed to load posts. Please try again.
            </div>
        `;
    }
}

async function createPost(title, content, btn) {
    if (!token) return;
    toggleLoading(btn, true);

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

        showToast("Post published");
        createPostForm.reset();
        fetchPosts();
    } catch (err) {
        showToast("Error creating post", "error");
    } finally {
        toggleLoading(btn, false);
    }
}

// Like handler
window.handleLike = async (postId, btn) => {
    if (!token) {
        showToast("Please log in to like posts", "error");
        loginTriggerBtn.click();
        return;
    }
    
    const icon = btn.querySelector('i');
    const wasLiked = btn.classList.contains('liked');
    
    try {
        const method = wasLiked ? "DELETE" : "POST";
        const response = await fetch(`${API_URL}/likes/`, {
            method,
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ post_id: postId })
        });
        
        if (response.ok) {
            if (wasLiked) {
                btn.classList.remove('liked');
                icon.classList.remove('bi-heart-fill');
                icon.classList.add('bi-heart');
            } else {
                btn.classList.add('liked');
                icon.classList.remove('bi-heart');
                icon.classList.add('bi-heart-fill');
            }
        } else if (response.status === 400 && !wasLiked) {
            // Already liked, toggle to unlike
            btn.classList.add('liked');
            icon.classList.remove('bi-heart');
            icon.classList.add('bi-heart-fill');
        }
    } catch (err) {
        console.error(err);
    }
};

// --- Rendering ---
function renderPosts(posts) {
    postsContainer.innerHTML = "";
    
    if (posts.length === 0) {
        const emptyTemplate = document.getElementById('empty-state-template');
        postsContainer.innerHTML = emptyTemplate.innerHTML;
        return;
    }

    posts.forEach(post => {
        const dateObj = new Date(post.created_at);
        const dateStr = dateObj.toLocaleDateString(undefined, { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
        });
        
        const card = document.createElement('div');
        card.className = 'card border shadow-sm post-card';
        card.innerHTML = `
            <div class="card-body p-3">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <div>
                        <h6 class="post-title mb-1">${escapeHtml(post.title)}</h6>
                        <div class="post-meta">
                            <small class="text-muted">Posted ${dateStr}</small>
                        </div>
                    </div>
                </div>
                
                <p class="post-content mb-3">${escapeHtml(post.content)}</p>
                
                <div class="d-flex gap-2">
                    <button class="btn btn-sm btn-light like-btn" onclick="handleLike(${post.id}, this)">
                        <i class="bi bi-heart me-1"></i>Like
                    </button>
                </div>
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
loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    login(
        document.getElementById('email').value,
        document.getElementById('password').value,
        e.submitter
    );
});

signupForm.addEventListener('submit', (e) => {
    e.preventDefault();
    signup(
        document.getElementById('signup-email').value,
        document.getElementById('signup-password').value,
        e.submitter
    );
});

createPostForm.addEventListener('submit', (e) => {
    e.preventDefault();
    createPost(
        document.getElementById('post-title').value,
        document.getElementById('post-content').value,
        e.submitter
    );
});

logoutBtn.addEventListener('click', logout);
refreshBtn.addEventListener('click', fetchPosts);

// Start
init();
