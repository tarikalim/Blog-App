document.addEventListener('DOMContentLoaded', function () {
    const queryParams = new URLSearchParams(window.location.search);
    const userId = queryParams.get('user_id');
    const username = queryParams.get('username');
    const postsContainer = document.getElementById('posts');
    const usernameContainer = document.getElementById('username');

    if (username) {
        usernameContainer.textContent = username;
    } else {
        usernameContainer.textContent = 'Unknown User';
    }

    if (userId) {
        fetch(`/post/user/${userId}`)
            .then(response => response.json())
            .then(posts => {
                if (posts.length > 0) {
                    posts.forEach(post => {
                        const postItem = document.createElement('div');
                        postItem.className = 'post-item';
                        postItem.innerHTML = `
                            <h3>${post.title}</h3>
                            <p><strong>Category:</strong> ${post.category_name}</p>
                            <p><em>${new Date(post.publish_date).toLocaleString()}</em></p>
                            <p>${post.content}</p>
                        `;
                        postItem.addEventListener('click', function () {
                            window.location.href = `/static/post_detail.html?post_id=${post.id}`;
                        });
                        postsContainer.appendChild(postItem);
                    });
                } else {
                    postsContainer.innerHTML += '<p>No posts found</p>';
                }
            })
            .catch(error => {
                console.error('Error fetching posts:', error);
                postsContainer.innerHTML = '<p>Error fetching posts</p>';
            });
    } else {
        postsContainer.innerHTML = '<p>No user ID provided</p>';
    }
});
