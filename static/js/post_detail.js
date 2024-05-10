let isLiked = false;

document.addEventListener('DOMContentLoaded', function () {
    const queryParams = new URLSearchParams(window.location.search);
    const postId = queryParams.get('post_id');
    if (!postId) {
        console.error('No post id provided!');
        return;
    }
    fetchPostDetails(postId);
    setupEventListeners(postId);
});

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


function fetchPostDetails(postId) {
    fetch(`/post/${postId}`, {method: 'GET'})
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            const {title, content, publish_date, category_name} = data;
            document.getElementById('postTitle').textContent = title;
            document.getElementById('postContent').textContent = content;
            document.getElementById('publishDate').textContent = new Date(publish_date).toLocaleDateString();
            document.getElementById('categoryName').textContent = category_name;
            updateComments(postId);
            updateLikes(postId);
        })
        .catch(error => console.error('Error fetching post details:', error));
}

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


function updateComments(postId) {
    fetch(`/comment/${postId}`, {method: 'GET'})
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


function postComment(postId, content) {
    const token = localStorage.getItem('token');
    fetch(`/comment/${postId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({content: content})
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
            alert('You can only delete your own comments.');
        });
}

function setupLikeButton(postId) {
    fetchLikeStatus(postId).then(likedStatus => {
        isLiked = likedStatus;
        updateLikeButton(postId);
    });
}

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
});

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
