document.addEventListener('DOMContentLoaded', function () {
    var loginForm = document.getElementById('loginForm');
    loginForm.onsubmit = function (e) {
        e.preventDefault();
        var username = document.getElementById('username').value;
        var password = document.getElementById('password').value;

        fetch('/auth/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        })
            .then(response => response.json().then(data => ({status: response.status, body: data})))
            .then(result => {
                if (result.status >= 400) throw new Error(result.body.message || 'Login failed');
                localStorage.setItem('token', result.body.token);
                window.location.href = 'main.html';
            })
            .catch(error => {
                console.error('Login Error:', error);
                alert(error.message);
            });
    };
});

document.addEventListener('DOMContentLoaded', function () {
    var registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.onsubmit = function (e) {
            e.preventDefault();

            var username = document.getElementById('username').value;
            var email = document.getElementById('email').value;
            var password = document.getElementById('password').value;

            fetch('/auth/register', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, email, password})
            })
                .then(response => response.json().then(data => ({status: response.status, body: data})))
                .then(result => {
                    if (result.status >= 400) throw new Error(result.body.message || 'Registration failed');
                    window.location.href = 'login.html';
                })
                .catch(error => {
                    console.error('Registration Error:', error);
                    alert(error.message);
                });
        };
    }
});


document.addEventListener('DOMContentLoaded', function () {
    var forgotPasswordBtn = document.getElementById('forgot-password-btn');
    var forgotPasswordForm = document.getElementById('forgot-password-form');

    if (forgotPasswordBtn && forgotPasswordForm) {
        forgotPasswordBtn.addEventListener('click', function () {
            forgotPasswordForm.style.display = 'block';
        });
    }

    window.sendResetLink = function () {
        var email = document.getElementById('reset-email').value;
        fetch('/auth/change-password-request', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email: email})
        })
            .then(response => response.json())
            .then(data => {
                if (data.message) alert(data.message);
                forgotPasswordForm.style.display = 'none';
            })
            .catch(error => {
                console.error('Error sending reset link:', error);
                alert('Failed to send reset link.');
            });
    };
});


document.getElementById('reset-password-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const newPassword = document.getElementById('new-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    if (newPassword !== confirmPassword) {
        alert('Passwords do not match!');
        return;
    }

    const params = new URLSearchParams(window.location.search);
    const token = params.get('token');

    fetch(`/auth/reset-password/${token}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({new_password: newPassword})
    })
        .then(response => response.json())
        .then(data => {
            if (data.message !== "Success: Password has been changed.") throw new Error(data.message);
            alert('Your password has been successfully reset. You can now login with your new password.');
            window.location.href = 'login.html';
        })
        .catch(error => {
            console.error('Error:', error);
            alert(error.message);
        });
});


