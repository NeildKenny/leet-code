const apiUrl = 'http://localhost:8000';

function log(message) {
  const out = document.getElementById('output');
  out.textContent += message + '\n';
}

async function createUser() {
  const username = document.getElementById('user-name').value;
  const password = document.getElementById('user-password').value;
  const picture = document.getElementById('user-picture').value;
  const params = new URLSearchParams({username, password});
  if (picture) params.append('profile_picture_url', picture);
  const response = await fetch(`${apiUrl}/users`, {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: params
  });
  const data = await response.json();
  log(JSON.stringify(data, null, 2));
}

async function createCampaign() {
  const name = document.getElementById('campaign-name').value;
  const description = document.getElementById('campaign-description').value;
  const params = new URLSearchParams({name});
  if (description) params.append('description', description);
  const response = await fetch(`${apiUrl}/campaigns`, {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: params
  });
  const data = await response.json();
  log(JSON.stringify(data, null, 2));
}

async function createNote() {
  const campaign_id = document.getElementById('note-campaign').value;
  const author_id = document.getElementById('note-author').value;
  const title = document.getElementById('note-title').value;
  const body = document.getElementById('note-body').value;
  const image_url = document.getElementById('note-image').value;
  const session_name = document.getElementById('note-session-name').value;
  const session_date = document.getElementById('note-session-date').value;
  const session_number = document.getElementById('note-session-number').value;
  const category = document.getElementById('note-category').value;
  const is_private = document.getElementById('note-private').checked;
  const params = new URLSearchParams({campaign_id, author_id, title, body});
  if (image_url) params.append('image_url', image_url);
  if (session_name) params.append('session_name', session_name);
  if (session_date) params.append('session_date', session_date);
  if (session_number) params.append('session_number', session_number);
  if (category) params.append('category', category);
  if (is_private) params.append('is_private', 'true');
  const response = await fetch(`${apiUrl}/notes`, {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: params
  });
  const data = await response.json();
  log(JSON.stringify(data, null, 2));
}

async function loadNotes() {
  const response = await fetch(`${apiUrl}/notes`);
  const notes = await response.json();
  const list = document.getElementById('notes-list');
  list.innerHTML = '';
  notes.forEach(n => {
    const item = document.createElement('li');
    const parts = [n.title];
    if (n.session_name) parts.push(`session: ${n.session_name}`);
    if (n.session_number) parts.push(`#${n.session_number}`);
    if (n.category) parts.push(`[${n.category}]`);
    item.textContent = parts.join(' ') + ': ' + n.body;
    list.appendChild(item);
  });
}

document.getElementById('create-user').addEventListener('click', createUser);
document.getElementById('create-campaign').addEventListener('click', createCampaign);
document.getElementById('create-note').addEventListener('click', createNote);
document.getElementById('load-notes').addEventListener('click', loadNotes);
