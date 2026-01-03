 // Configuration
        const API_BASE_URL = 'http://localhost:8000'; // Change this to your backend URL
        let currentUser = null;
        let token = null;

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            checkAuth();
            setupEventListeners();
        });

        function setupEventListeners() {
            document.getElementById('registerForm').addEventListener('submit', handleRegister);
            document.getElementById('loginForm').addEventListener('submit', handleLogin);
            document.getElementById('createPostForm').addEventListener('submit', handleCreatePost);
            document.getElementById('postimage').addEventListener('change', handleFileSelect);
        }

        // Authentication Check
        function checkAuth() {
            token = localStorage.getItem('token');
            if (token) {
                showDashboard();
                loadPosts();
            }
        }

        // Registration
        async function handleRegister(e) {
            e.preventDefault();
            
            const email = document.getElementById('regEmail').value.trim();
            const username = document.getElementById('regUsername').value.trim();
            const gender = document.getElementById('regGender').value;
            const contact_no = document.getElementById('regContact').value.trim();
            const password = document.getElementById('regPassword').value;

            // Validation
            if (!validateRegistration(email, username, gender, contact_no, password)) {
                return;
            }

            showLoading();

            try {
                const response = await fetch(`${API_BASE_URL}/auth/register`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, username, gender, contact_no, password })
                });

                const data = await response.json();

                if (response.ok) {
                    alert('Registration successful! Please login.');
                    showLogin();
                } else {
                    alert(data.detail || 'Registration failed');
                }
            } catch (error) {
                alert('Error connecting to server: ' + error.message);
            } finally {
                hideLoading();
            }
        }

        // Login
        async function handleLogin(e) {
            e.preventDefault();
            
            const username = document.getElementById('loginUsername').value.trim();
            const password = document.getElementById('loginPassword').value;

            showLoading();

            try {
                const formData = new URLSearchParams();
                formData.append('username', username);
                formData.append('password', password);

                const response = await fetch(`${API_BASE_URL}/auth/token/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: formData
                });

                const data = await response.json();

                if (response.ok) {
                    token = data.access_token;
                    localStorage.setItem('token', token);
                    currentUser = data.user;
                    showDashboard();
                    loadPosts();
                } else {
                    alert(data.detail || 'Login failed');
                }
            } catch (error) {
                alert('Error connecting to server: ' + error.message);
            } finally {
                hideLoading();
            }
        }

        // Create Post
        async function handleCreatePost(e) {
            e.preventDefault();
            
            const content = document.getElementById('postContent').value.trim();
            const imageFile = document.getElementById('postimage').files[0];

            if (!content) {
                alert('Please enter post content');
                return;
            }

            showLoading();

            try {
                const formData = new FormData();
                formData.append('content', content);
                if (imageFile) {
                    formData.append('image', imageFile);
                }

                const response = await fetch(`${API_BASE_URL}/posts/create`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    body: formData
                });

                const data = await response.json();

                if (response.ok) {
                    document.getElementById('createPostForm').reset();
                    document.getElementById('filePreview').textContent = '';
                    loadPosts();
                } else {
                    alert(data.detail || 'Failed to create post');
                }
            } catch (error) {
                alert('Error creating post: ' + error.message);
            } finally {
                hideLoading();
            }
        }

        // Load Posts
        async function loadPosts() {
            showLoading();

            try {
                const response = await fetch(`${API_BASE_URL}/posts/feed/posts`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                const posts = await response.json();

                if (response.ok) {
                    displayPosts(posts, 'postsFeed');
                } else {
                    alert('Failed to load posts');
                }
            } catch (error) {
                alert('Error loading posts: ' + error.message);
            } finally {
                hideLoading();
            }
        }

        // Display Posts
        function displayPosts(posts, containerId) {
            const container = document.getElementById(containerId);
            container.innerHTML = '';

            if (posts.length === 0) {
                container.innerHTML = '<p style="text-align: center; color: #999;">No posts yet</p>';
                return;
            }

            posts.forEach(post => {
                const postCard = document.createElement('div');
                postCard.className = 'post-card';
                
                let ImageHtml = '';
                if (post.Image_url) {
                    ImageHtml = `<img src="${API_BASE_URL}${post.image_url}" alt="Post image" class="post-image">`;
                }

                postCard.innerHTML = `
                    <div class="post-header">
                        <div class="post-author">${post.author_name || 'Anonymous'}</div>
                    </div>
                    <div class="post-content">${post.content}</div>
                    ${ImageHtml}
                    <div class="post-meta">${new Date(post.created_at).toLocaleString()}</div>
                `;

                container.appendChild(postCard);
            });
        }

        // Search Users
        async function searchUsers() {
            const query = document.getElementById('searchInput').value.trim();

            if (!query) {
                alert('Please enter a search term');
                return;
            }

            showLoading();

            try {
                const response = await fetch(`${API_BASE_URL}/users/search?name=${encodeURIComponent(query)}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                const users = await response.json();

                if (response.ok) {
                    displaySearchResults(users);
                } else {
                    alert('Search failed');
                }
            } catch (error) {
                alert('Error searching users: ' + error.message);
            } finally {
                hideLoading();
            }
        }

        // Display Search Results
        function displaySearchResults(users) {
            const resultsContainer = document.getElementById('userResults');
            resultsContainer.innerHTML = '';

            document.getElementById('searchResults').classList.remove('hidden');

            if (users.length === 0) {
                resultsContainer.innerHTML = '<p style="text-align: center; color: #999;">No users found</p>';
                return;
            }

            users.forEach(user => {
                const userDiv = document.createElement('div');
                userDiv.className = 'user-result';
                userDiv.onclick = () => viewProfile(user.id);
                userDiv.innerHTML = `
                    <div class="user-name">${user.name}</div>
                    <div class="user-email">${user.email}</div>
                `;
                resultsContainer.appendChild(userDiv);
            });
        }

        // View Profile
        async function viewProfile(userId) {
            showLoading();

            try {
                const [userResponse, postsResponse] = await Promise.all([
                    fetch(`${API_BASE_URL}/users/${userId}`, {
                        headers: { 'Authorization': `Bearer ${token}` }
                    }),
                    fetch(`${API_BASE_URL}/users/${userId}/posts`, {
                        headers: { 'Authorization': `Bearer ${token}` }
                    })
                ]);

                const user = await userResponse.json();
                const posts = await postsResponse.json();

                if (userResponse.ok) {
                    document.getElementById('profileName').textContent = user.name;
                    document.getElementById('profileEmail').textContent = user.email;
                    displayPosts(posts, 'profilePosts');
                    
                    document.getElementById('searchResults').classList.add('hidden');
                    document.getElementById('profileView').style.display = 'block';
                } else {
                    alert('Failed to load profile');
                }
            } catch (error) {
                alert('Error loading profile: ' + error.message);
            } finally {
                hideLoading();
            }
        }

        // File Selection
        function handleFileSelect(e) {
            const file = e.target.files[0];
            const preview = document.getElementById('filePreview');
            
            if (file) {
                preview.textContent = `Selected: ${file.name}`;
            } else {
                preview.textContent = '';
            }
        }

        // Validation
        function validateRegistration(email, username, gender, contact_no, password) {
            let isValid = true;

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                document.getElementById('emailError').style.display = 'block';
                isValid = false;
            } else {
                document.getElementById('emailError').style.display = 'none';
            }

            if (username.length < 3) {
                document.getElementById('usernameError').style.display = 'block';
                isValid = false;
            } else {
                document.getElementById('usernameError').style.display = 'none';
            }

            if (!gender) {
                document.getElementById('genderError').style.display = 'block';
                isValid = false;
            } else {
                document.getElementById('genderError').style.display = 'none';
            }

            const contactRegex = /^[0-9]{10,15}$/;
            if (!contactRegex.test(contact_no)) {
                document.getElementById('contactError').style.display = 'block';
                isValid = false;
            } else {
                document.getElementById('contactError').style.display = 'none';
            }

            if (password.length < 6) {
                document.getElementById('passwordError').style.display = 'block';
                isValid = false;
            } else {
                document.getElementById('passwordError').style.display = 'none';
            }

            return isValid;
        }

        // UI Functions
        function showRegister() {
            document.getElementById('registerContainer').classList.remove('hidden');
            document.getElementById('loginContainer').classList.add('hidden');
        }

        function showLogin() {
            document.getElementById('loginContainer').classList.remove('hidden');
            document.getElementById('registerContainer').classList.add('hidden');
        }

        function showDashboard() {
            document.getElementById('registerContainer').classList.add('hidden');
            document.getElementById('loginContainer').classList.add('hidden');
            document.getElementById('dashboard').style.display = 'block';
            document.getElementById('navbar').classList.remove('hidden');
        }

        function hideSearchResults() {
            document.getElementById('searchResults').classList.add('hidden');
            document.getElementById('searchInput').value = '';
        }

        function hideProfile() {
            document.getElementById('profileView').style.display = 'none';
        }

        function showLoading() {
            document.getElementById('loading').style.display = 'block';
        }

        function hideLoading() {
            document.getElementById('loading').style.display = 'none';
        }

        function logout() {
            localStorage.removeItem('token');
            token = null;
            currentUser = null;
            document.getElementById('dashboard').style.display = 'none';
            document.getElementById('navbar').classList.add('hidden');
            showLogin();
        }