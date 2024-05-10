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
                postElement.innerHTML = `<h3>${post.title}</h3><p>Category: ${post.category_name}</p><p>${post.content}</p>`;
                postElement.addEventListener('click', function () {
                    window.location.href = `/static/post_detail.html?post_id=${post.id}`;
                });
                postsContainer.appendChild(postElement);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error fetching posts');
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
            alert('Error updating profile');
        });
}
