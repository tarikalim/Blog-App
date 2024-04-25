document.addEventListener('DOMContentLoaded', function () {
    var loginForm = document.getElementById('loginForm');
    loginForm.onsubmit = function (e) {
        e.preventDefault();

        var username = document.getElementById('username').value;
        var password = document.getElementById('password').value;

        fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({username, password})
        })
            .then(response => {
                if (!response.ok) throw new Error('Login failed');
                return response.json();
            })
            .then(data => {
                localStorage.setItem('token', data.token);
                window.location.href = 'main.html';
            })
            .catch(error => {
                console.error('Login Error:', error);
                alert('Wrong Credentials.');
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
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({username, email, password})
            })
                .then(response => {
                    if (!response.ok) throw new Error('Registration failed');
                    return response.json();
                })
                .then(data => {
                    window.location.href = 'login.html';
                })
                .catch(error => {
                    console.error('Registration Error:', error);
                    alert('Registration failed.');
                });
        };
    }
});
