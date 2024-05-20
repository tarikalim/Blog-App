document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('profileButton').addEventListener('click', function () {
        window.location.href = 'profile.html';
    });

    document.getElementById('searchButton').addEventListener('click', function () {
        var searchQuery = document.getElementById('searchInput').value;
        searchPosts(searchQuery);
    });

    document.getElementById('categorySelect').addEventListener('change', function () {
        var selectedCategory = document.getElementById('categorySelect').value;
        if (selectedCategory) {
            loadPostsByCategory(selectedCategory);
        } else {
            searchPosts();
        }
    });

    document.getElementById('searchUserButton').addEventListener('click', function () {
        var username = document.getElementById('usernameInput').value;
        searchUsers(username);
    });

    loadCategories();
    searchPosts();

    // Modal functionality
    var postFormModal = document.getElementById('postFormModal');
    var btn = document.getElementById('createPostButton');
    var span = document.getElementsByClassName('close')[0];

    btn.onclick = function () {
        postFormModal.style.display = 'block';
        loadPostFormCategories();
    }

    span.onclick = function () {
        postFormModal.style.display = 'none';
    }

    window.onclick = function (event) {
        if (event.target == postFormModal) {
            postFormModal.style.display = 'none';
        }
    }

    document.getElementById('postForm').addEventListener('submit', function (event) {
        event.preventDefault();
        createPost();
    });

    // User search modal functionality
    var userSearchModal = document.getElementById('userSearchModal');
    var closeUserSearchModal = document.getElementById('closeUserSearchModal');

    closeUserSearchModal.onclick = function () {
        userSearchModal.style.display = 'none';
    }

    window.onclick = function (event) {
        if (event.target == userSearchModal) {
            userSearchModal.style.display = 'none';
        }
    }
});

function loadCategories() {
    return fetch('/category')
        .then(response => response.json())
        .then(categories => {
            const categorySelect = document.getElementById('categorySelect');
            categorySelect.innerHTML = '<option value="">All Categories</option>';
            categories.forEach(category => {
                categorySelect.innerHTML += `<option value="${category.id}">${category.name}</option>`;
            });
        });
}

function searchPosts(searchQuery = '') {
    let url = '/post/search';
    if (searchQuery) {
        url += `?title=${encodeURIComponent(searchQuery)}`;
    }

    fetch(url)
        .then(response => response.json())
        .then(posts => {
            const postsContainer = document.getElementById('posts');
            postsContainer.innerHTML = '';
            posts.forEach(post => {
                const postElement = document.createElement('div');
                postElement.innerHTML = `<h2>${post.title}</h2><p>Category: ${post.category_name}</p><p>${post.content}</p>`;
                postElement.addEventListener('click', function () {
                    window.location.href = `/static/post_detail.html?post_id=${post.id}`;
                });
                postsContainer.appendChild(postElement);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to load posts. Please try again.');
        });
}

function loadPostsByCategory(categoryId) {
    let url = `/post/category/${encodeURIComponent(categoryId)}`;

    fetch(url)
        .then(response => response.json())
        .then(posts => {
            const postsContainer = document.getElementById('posts');
            postsContainer.innerHTML = '';
            posts.forEach(post => {
                const postElement = document.createElement('div');
                postElement.innerHTML = `<h2>${post.title}</h2><p>Category: ${post.category_name}</p><p>${post.content}</p>`;
                postElement.addEventListener('click', function () {
                    window.location.href = `/static/post_detail.html?post_id=${post.id}`;
                });
                postsContainer.appendChild(postElement);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to load posts. Please try again.');
        });
}

function searchUsers(username) {
    if (!username) {
        alert('Please enter a username');
        return;
    }

    fetch(`/user/search?username=${encodeURIComponent(username)}`)
        .then(response => response.json())
        .then(users => {
            const userResults = document.getElementById('userResults');
            userResults.innerHTML = '';
            if (users.length > 0) {
                users.forEach(user => {
                    const userElement = document.createElement('a');
                    userElement.href = `/static/user_posts.html?user_id=${user.id}&username=${encodeURIComponent(user.username)}`;
                    userElement.textContent = `${user.username} `;
                    userElement.classList.add('user-results');
                    userResults.appendChild(userElement);
                });
                userResults.classList.add('show');
            } else {
                userResults.innerHTML = '<p>No users found</p>';
                userResults.classList.add('show');
            }
            document.getElementById('userSearchModal').style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to load users. Please try again.');
        });
}

function loadPostFormCategories() {
    fetch('/category')
        .then(response => response.json())
        .then(categories => {
            const categorySelect = document.getElementById('category');
            categorySelect.innerHTML = '<option value="">Select a category</option>';
            categories.forEach(category => {
                categorySelect.innerHTML += `<option value="${category.id}">${category.name}</option>`;
            });
        })
        .catch(error => console.error('Error fetching categories:', error));
}

function createPost() {
    const title = document.getElementById('title').value;
    const category = document.getElementById('category').value;
    const content = document.getElementById('content').value;

    const payload = {
        title: title,
        category_id: parseInt(category),
        content: content
    };

    const token = localStorage.getItem('token');

    fetch('/post', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(errorData.message || 'Failed to create post.');
            });
        }
        return response.json();
    })
    .then(data => {
        console.log('Post created:', data);
        postFormModal.style.display = 'none';
        searchPosts();
    })
    .catch(error => {
        console.error('Error creating post:', error);
        alert(error.message);
    });
}
