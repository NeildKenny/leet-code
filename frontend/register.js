const apiUrl = 'http://localhost:8001';

function toggleTheme() {
  const body = document.body;
  body.classList.toggle('dark');
  body.classList.toggle('light');
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.createElement('button');
  btn.textContent = 'Toggle Theme';
  btn.addEventListener('click', toggleTheme);
  document.body.prepend(btn);
});

async function register() {
  const username = document.getElementById('reg-username').value;
  const password = document.getElementById('reg-password').value;
  const picture = document.getElementById('reg-picture').value;
  const params = new URLSearchParams({username, password});
  if (picture) params.append('profile_picture_url', picture);
  const response = await fetch(`${apiUrl}/register`, {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: params
  });
  if (response.ok) {
    alert('User registered');
    window.location.href = 'login.html';
  } else {
    const data = await response.json();
    alert('Registration failed: ' + (data.detail || response.status));
  }
}

document.getElementById('register-button').addEventListener('click', register);
