document.getElementById('profileButton').addEventListener('click', function () {
    var token = localStorage.getItem('token');
    fetch('/user', {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + token
        }
    })
        .then(response => response.json())
        .then(data => {
            alert(JSON.stringify(data));
        })
        .catch(error => console.error('Error:', error));
});

document.getElementById('createPostButton').addEventListener('click', function () {
    window.location.href = '/create-post.html';
});

document.getElementById('searchButton').addEventListener('click', function () {
    var searchQuery = document.getElementById('searchInput').value;
    loadPosts(searchQuery);
});

function loadCategories() {
    return fetch('/category')
        .then(response => response.json())
        .then(categories => {
            const categoryMap = {};
            categories.forEach(category => {
                categoryMap[category.id] = category.name;
            });
            return categoryMap;
        });
}

function loadPosts(searchQuery = '') {
    let url = '/post';
    if (searchQuery) {
        url += `?title=${encodeURIComponent(searchQuery)}`;
    }

    loadCategories().then(categoryMap => {
        fetch(url)
            .then(response => response.json())
            .then(posts => {
                const postsContainer = document.getElementById('posts');
                postsContainer.innerHTML = '';
                posts.forEach(post => {
                    const postElement = document.createElement('div');
                    const categoryName = categoryMap[post.category_id] || 'No Category';
                    postElement.innerHTML = `<h2>${post.title}</h2><p>${post.content}</p><p>Category: ${categoryName}</p>`;

                    postElement.addEventListener('click', function () {
                        window.location.href = `/static/post_detail.html?post_id=${post.id}`;
                    });

                    postsContainer.appendChild(postElement);
                });
            })
            .catch(error => console.error('Error:', error));
    });
}

window.onload = function () {
    loadPosts();
}
