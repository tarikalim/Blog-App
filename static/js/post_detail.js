let isLiked = false;
let isFavorite = false;
let favoriteId = null;
// Event listener for when the DOM content is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    const queryParams = new URLSearchParams(window.location.search);
    const postId = queryParams.get('post_id');
    if (!postId) {
        console.error('No post id provided!');
        return;
    }
    fetchPostDetails(postId);
    setupEventListeners(postId);
    setupLikeButton(postId);
    setupFavoriteButton(postId);
});
// Function to set up event listeners for various interactive elements
function setupEventListeners(postId) {
    const commentButton = document.getElementById('commentButton');
    commentButton.addEventListener('click', () => {
        const commentInput = document.getElementById('commentInput');
        const commentContent = commentInput.value.trim();
        if (commentContent) {
            postComment(postId, commentContent);
        } else {
            alert("Please write a comment before posting.");
        }
    });

    document.querySelectorAll('.dropbtn').forEach(button => {
        button.addEventListener('click', function (event) {
            event.stopPropagation();
            const dropdownContent = this.nextElementSibling;
            if (dropdownContent.style.display === 'block') {
                dropdownContent.style.display = 'none';
            } else {
                dropdownContent.style.display = 'block';
            }
        });
    });

    const commentList = document.getElementById('commentList');
    commentList.addEventListener('click', event => {
        const target = event.target;
        if (target.tagName === 'A' && target.closest('.dropdown-content')) {
            const action = target.dataset.action;
            const commentId = target.closest('li').dataset.commentId;
            if (action === 'delete') {
                deleteComment(commentId, postId);
            } else if (action === 'update') {
                updateComment(commentId, postId);
            }
        }
    });
}
// Function to fetch and display the details of the post
function fetchPostDetails(postId) {
    fetch(`/post/${postId}`, { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            const { title, content, publish_date, category_name } = data;
            document.getElementById('postTitle').textContent = title;
            document.getElementById('postContent').textContent = content;
            document.getElementById('publishDate').textContent = new Date(publish_date).toLocaleDateString();
            document.getElementById('categoryName').textContent = category_name;
            updateComments(postId);
            updateLikes(postId);
        })
        .catch(error => console.error('Error fetching post details:', error));
}
// Function to fetch and display the like count for the post
function updateLikes(postId) {
    const token = localStorage.getItem('token');
    fetch(`/like/${postId}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch like count');
            }
            return response.json();
        })
        .then(data => {
            const likeCountElement = document.getElementById('likeCount');
            likeCountElement.textContent = data.like_count;
        })
        .catch(error => {
            console.error('Error fetching like count:', error);
        });
}
// Function to fetch and display comments for the post
function updateComments(postId) {
    fetch(`/comment/${postId}`, { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Fetch Comments Error:', data.error);
                return;
            }
            const commentList = document.getElementById('commentList');
            commentList.innerHTML = '';
            data.forEach(comment => {
                const li = document.createElement('li');
                li.dataset.commentId = comment.id;

                const commentContainer = document.createElement('div');
                commentContainer.className = 'comment-container';

                const commentInfo = document.createElement('p');
                commentInfo.textContent = `Commented by: ${comment.username}`;
                commentInfo.className = 'comment-info';
                commentContainer.appendChild(commentInfo);

                const content = document.createElement('p');
                content.className = 'comment-content';
                content.textContent = comment.content;
                commentContainer.appendChild(content);

                const commentDate = document.createElement('p');
                commentDate.className = 'comment-date';
                commentDate.textContent = new Date(comment.comment_date).toLocaleString();

                const actions = document.createElement('div');
                actions.className = 'dropdown';
                actions.innerHTML = `
                    <div class="dropbtn">⋮</div>
                    <div class="dropdown-content">
                        <a href="#" data-action="update">Update</a>
                        <a href="#" data-action="delete">Delete</a>
                    </div>
                `;

                li.appendChild(commentContainer);
                li.appendChild(commentDate);
                li.appendChild(actions);

                commentList.appendChild(li);
            });
        })
        .catch(error => console.error('Error updating comments:', error));
}
// Function to post a new comment to the server
function postComment(postId, content) {
    const token = localStorage.getItem('token');
    fetch(`/comment/${postId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ content: content })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to post comment');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('commentInput').value = '';
            updateComments(postId);
        })
        .catch(error => {
            console.error('Error posting comment:', error);
            alert('Failed to post comment. Please try again.');
        });
}
// Function to delete a comment from the server
function deleteComment(commentId, postId) {
    const token = localStorage.getItem('token');
    fetch(`/comment/${commentId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('You can only delete your own comments.');
            }
            updateComments(postId);
        })
        .catch(error => {
            console.error('Error deleting comment:', error);
            alert(error.message);
        });
}
// Function to set up the like button with the current like status
function setupLikeButton(postId) {
    fetchLikeStatus(postId).then(likedStatus => {
        isLiked = likedStatus;
        updateLikeButton(postId);
    });
}
// Function to update the like button text and functionality
function updateLikeButton(postId) {
    const likeButton = document.getElementById('likeButton');

    likeButton.onclick = function () {
        if (isLiked) {
            unlikePost(postId);
        } else {
            likePost(postId);
        }
    };

    if (isLiked) {
        likeButton.textContent = 'Unlike Post';
    } else {
        likeButton.textContent = 'Like Post';
    }
}
// Function to like the post on the server
function likePost(postId) {
    const token = localStorage.getItem('token');
    fetch(`/like/${postId}`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to like post');
            }
            isLiked = true;
            updateLikeButton(postId);
            updateLikes(postId);
        })
        .catch(error => {
            console.error('Error liking post:', error);
            alert('Failed to like post. Please try again.');
        });
}
// Function to unlike the post on the server
function unlikePost(postId) {
    const token = localStorage.getItem('token');
    fetch(`/like/${postId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to unlike post');
            }
            isLiked = false;
            updateLikeButton(postId);
            updateLikes(postId);
        })
        .catch(error => {
            console.error('Error unliking post:', error);
            alert('Failed to unlike post. Please try again.');
        });
}
// Function to fetch the current like status for the post
function fetchLikeStatus(postId) {
    const token = localStorage.getItem('token');
    return fetch(`/like/status/${postId}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch like status');
            }
            return response.json();
        })
        .then(data => {
            return data.status;
        })
        .catch(error => {
            console.error('Error fetching like status:', error);
        });
}
// Function to set up the favorite button with the current favorite status
function setupFavoriteButton(postId) {
    fetchFavoriteStatus(postId).then(favoriteStatus => {
        isFavorite = favoriteStatus.status;
        favoriteId = favoriteStatus.favorite_id;
        updateFavoriteButton();
    });
}
// Function to update the favorite button text and functionality
function updateFavoriteButton() {
    const favoriteButton = document.getElementById('favoriteButton');

    favoriteButton.onclick = function () {
        const queryParams = new URLSearchParams(window.location.search);
        const postId = queryParams.get('post_id');

        if (isFavorite) {
            unfavoritePost(postId);
        } else {
            favoritePost(postId);
        }
    };

    if (isFavorite) {
        favoriteButton.textContent = 'Unfavorite Post';
    } else {
        favoriteButton.textContent = 'Favorite Post';
    }
}
// Function to favorite the post on the server
function favoritePost(postId) {
    const token = localStorage.getItem('token');
    fetch(`/favorite/${postId}`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to favorite post');
            }
            return response.json();
        })
        .then(data => {
            isFavorite = true;
            favoriteId = data.id;
            updateFavoriteButton();
        })
        .catch(error => {
            console.error('Error favoriting post:', error);
            alert('Failed to favorite post. Please try again.');
        });
}
// Function to unfavorite the post on the server
function unfavoritePost(postId) {
    const token = localStorage.getItem('token');
    fetch(`/favorite/${favoriteId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to unfavorite post');
            }
            isFavorite = false;
            favoriteId = null;
            updateFavoriteButton();
        })
        .catch(error => {
            console.error('Error unfavoriting post:', error);
            alert('Failed to unfavorite post. Please try again.');
        });
}
// Function to fetch the current favorite status for the post
function fetchFavoriteStatus(postId) {
    const token = localStorage.getItem('token');
    return fetch(`/favorite/status/${postId}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch favorite status');
            }
            return response.json();
        })
        .then(data => {
            return { status: data.status, favorite_id: data.favorite_id };
        })
        .catch(error => {
            console.error('Error fetching favorite status:', error);
        });
}