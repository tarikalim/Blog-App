document.addEventListener('DOMContentLoaded', function () {
    const token = localStorage.getItem('token');
    if (!token) {
        console.error('Please Login to System.');
        window.location.href = 'login.html';
        return;
    }

    getUserProfile(token);
    getUserPosts(token);

    document.getElementById('editProfileButton').addEventListener('click', function () {
        document.getElementById('updateProfileForm').style.display = 'block';
    });

    document.getElementById('profileForm').addEventListener('submit', function (e) {
        e.preventDefault();
        updateUserProfile(token);
    });

    document.querySelector('button[type="button"]').addEventListener('click', function () {
        document.getElementById('updateProfileForm').style.display = 'none';
    });

    // Modal close functionality
    var updatePostModal = document.getElementById('updatePostModal');
    var span = document.getElementsByClassName('close')[0];
    span.onclick = function () {
        updatePostModal.style.display = 'none';
    }
    window.onclick = function (event) {
        if (event.target === updatePostModal) {
            updatePostModal.style.display = 'none';
        }
    }
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
            document.getElementById('username').value = user.username;
            document.getElementById('email').value = user.email;

            const joinDate = new Date(user.join_date);
            const formattedJoinDate = joinDate.toLocaleDateString();
            document.getElementById('join_date').textContent = formattedJoinDate;
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
                postElement.className = 'post-container';
                postElement.innerHTML = `
                <h3>${post.title}</h3>
                <p>Category: ${post.category_name}</p>
                <p>${post.content}</p>
                <div class="dropdown">
                    <button class="dropbtn">⋮</button>
                    <div class="dropdown-content">
                        <a href="#" data-action="update" data-post-id="${post.id}" data-post-title="${post.title}" data-post-content="${post.content}">Update</a>
                        <a href="#" data-action="delete" data-post-id="${post.id}">Delete</a>
                    </div>
                </div>
            `;
                postElement.addEventListener('click', function () {
                    window.location.href = `/static/post_detail.html?post_id=${post.id}`;
                });
                postsContainer.appendChild(postElement);
            });

            document.querySelectorAll('.dropdown-content a').forEach(link => {
                link.addEventListener('click', function (event) {
                    event.preventDefault();
                    event.stopPropagation();
                    const action = this.dataset.action;
                    const postId = this.dataset.postId;
                    if (action === 'update') {
                        const postTitle = this.dataset.postTitle;
                        const postContent = this.dataset.postContent;
                        showUpdatePostModal(postId, postTitle, postContent);
                    } else if (action === 'delete') {
                        deletePost(postId);
                    }
                });
            });
        })
        .catch(error => {
            console.error('Error:', error);
            alert(error.message);
        });
}

function updateUserProfile(token) {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;

    fetch(`/user/`, {
        method: 'PUT',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({username, email})
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update profile');
            }
            return response.json();
        })
        .then(updatedUser => {
            document.getElementById('userName').textContent = updatedUser.username;
            document.getElementById('userEmail').textContent = updatedUser.email;
            document.getElementById('updateProfileForm').style.display = 'none';
            alert('Profile updated successfully!');
        })
        .catch(error => {
            console.error('Update Error:', error);
            alert(error.message);
        });
}

function showUpdatePostModal(postId, postTitle, postContent) {
    const modal = document.getElementById('updatePostModal');
    document.getElementById('updateTitle').value = postTitle;
    document.getElementById('updateContent').value = postContent;
    modal.style.display = 'block';

    const updateForm = document.getElementById('updatePostForm');
    updateForm.onsubmit = function (e) {
        e.preventDefault();
        const updatedTitle = document.getElementById('updateTitle').value;
        const updatedContent = document.getElementById('updateContent').value;
        updatePost(postId, updatedTitle, updatedContent);
    };
}

function updatePost(postId, title, content) {
    fetch(`/post/${postId}`, {
        method: 'PUT',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({title, content})
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update post');
            }
            return response.json();
        })
        .then(updatedPost => {
            alert('Post updated successfully!');
            getUserPosts(localStorage.getItem('token'));
            document.getElementById('updatePostModal').style.display = 'none';
        })
        .catch(error => {
            console.error('Error updating post:', error);
            alert(error.message);
        });
}

function deletePost(postId) {
    if (confirm('Are you sure you want to delete this post?')) {
        fetch(`/post/${postId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to delete post');
                }
                alert('Post deleted successfully!');
                getUserPosts(localStorage.getItem('token'));
            })
            .catch(error => {
                console.error('Error deleting post:', error);
                alert(error.message);
            });
    }
}
