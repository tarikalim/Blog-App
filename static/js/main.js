document.getElementById('profileButton').addEventListener('click', function () {
    window.location.href = 'profile.html';
});

document.getElementById('searchButton').addEventListener('click', function () {
    var searchQuery = document.getElementById('searchInput').value;
    var selectedCategory = document.getElementById('categorySelect').value;
    loadPosts(searchQuery, selectedCategory);
});

document.getElementById('categorySelect').addEventListener('change', function () {
    var searchQuery = document.getElementById('searchInput').value;
    var selectedCategory = document.getElementById('categorySelect').value;
    loadPosts(searchQuery, selectedCategory);
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

function loadPosts(searchQuery = '', categoryId = '') {
    let url = '/post/search';
    let params = [];

    if (searchQuery) {
        params.push(`title=${encodeURIComponent(searchQuery)}`);
    }
    if (categoryId) {
        params.push(`category_id=${encodeURIComponent(categoryId)}`);
    }
    if (params.length > 0) {
        url += '?' + params.join('&');
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


window.onload = function () {
    loadCategories();
    loadPosts();
}
