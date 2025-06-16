const apiUrl = 'http://localhost:8001';


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
    window.location.href = 'campaigns.html';
  } else {
    alert('Login failed');
  }
}

document.getElementById('login-button').addEventListener('click', login);
