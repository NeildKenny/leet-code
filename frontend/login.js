const apiUrl = 'http://localhost:8000';

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

async function login() {
  const username = document.getElementById('login-username').value;
  const password = document.getElementById('login-password').value;
  const params = new URLSearchParams({username, password});
  const response = await fetch(`${apiUrl}/login`, {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: params
  });
  if (response.ok) {
    const data = await response.json();
    sessionStorage.setItem('user_id', data.id);
    window.location.href = 'notes.html';
  } else {
    alert('Login failed');
  }
}

document.getElementById('login-button').addEventListener('click', login);
