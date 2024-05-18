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

        loadPosts();
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

window.onload = function () {
    loadCategories();
    searchPosts();
}

// Modal functionality
var modal = document.getElementById('postFormModal');
var btn = document.getElementById('createPostButton');
var span = document.getElementsByClassName('close')[0];

btn.onclick = function () {
    modal.style.display = 'block';
    loadPostFormCategories();
}

span.onclick = function () {
    modal.style.display = 'none';
}

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

document.getElementById('postForm').addEventListener('submit', function (event) {
    event.preventDefault();
    createPost();
});

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
        .then(response => response.json())
        .then(data => {
            console.log('Post created:', data);
            modal.style.display = 'none';
            addPostToMainContent(data);
        })
        .catch(error => {
            console.error('Error creating post:', error);
            alert('Failed to create post. Please try again.');
        });
}

function addPostToMainContent(post) {
    const postsDiv = document.getElementById('posts');
    const postDiv = document.createElement('div');
    postDiv.classList.add('post');
    postDiv.innerHTML = `
        <h2>${post.title}</h2>
        <p>Category: ${post.category_name}</p>
        <p>${post.content}</p>
    `;
    postsDiv.appendChild(postDiv);
}
