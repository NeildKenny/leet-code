const apiUrl = 'http://localhost:8001';

function toggleTheme() {
  const body = document.body;
  body.classList.toggle('dark');
  body.classList.toggle('light');
}

document.getElementById('toggle-theme').addEventListener('click', toggleTheme);

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
    const data = await response.json();
    sessionStorage.setItem('user_id', data.id);
    window.location.href = 'campaigns.html';
  } else {
    const data = await response.json();
    alert('Registration failed: ' + (data.detail || response.status));
  }
}

document.getElementById('register-button').addEventListener('click', register);
