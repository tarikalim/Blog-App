document.addEventListener('DOMContentLoaded', function () {
    const token = localStorage.getItem('token');
    if (!token) {
        console.error('Please Login to System.');
        return;
    }

    getUserProfile(token);
    getUserPosts(token);
});

function getUserProfile(token) {
    fetch(`/user`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('No Profile.');
            }
            return response.json();
        })
        .then(user => {
            document.getElementById('userName').textContent = user.username;
            document.getElementById('userEmail').textContent = user.email;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function getUserPosts(token) {
    fetch(`/post/user`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch posts');
            }
            return response.json();
        })
        .then(posts => {
            const postsContainer = document.getElementById('userPosts');
            postsContainer.innerHTML = '';
            posts.forEach(post => {
                const postElement = document.createElement('div');
                postElement.innerHTML = `<h3>${post.title}</h3><p>${post.content}</p>`;
                postsContainer.appendChild(postElement);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error fetching posts');
        });
}
