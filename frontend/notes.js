const apiUrl = 'http://localhost:8001';

function log(message) {
  const out = document.getElementById('output');
  out.textContent += message + '\n';
}

function ensureLogin() {
  const userId = sessionStorage.getItem('user_id');
  if (!userId) {
    window.location.href = 'login.html';
  }
  return userId;
}

function getCampaignId() {
  const params = new URLSearchParams(window.location.search);
  const cid = params.get('campaign_id') || sessionStorage.getItem('campaign_id');
  if (cid) {
    sessionStorage.setItem('campaign_id', cid);
  } else {
    window.location.href = 'campaigns.html';
  }
  return cid;
}


let editingNoteId = null;

function setTodayDefault() {
  const dateInput = document.getElementById('note-session-date');
  dateInput.value = new Date().toISOString().split('T')[0];
}

function fillForm(note) {
  editingNoteId = note.id;
  document.getElementById('note-title').value = note.title;
  document.getElementById('note-body').value = note.body || '';
  document.getElementById('note-image').value = note.image_url || '';
  document.getElementById('note-session-name').value = note.session_name || '';
  document.getElementById('note-session-date').value = note.session_date || '';
  document.getElementById('note-session-number').value = note.session_number || '';
  document.getElementById('note-category').value = note.category || '';
  document.getElementById('note-private').checked = note.is_private;
  document.getElementById('create-note').textContent = 'Update Note';
}

function clearForm() {
  editingNoteId = null;
  document.getElementById('note-title').value = '';
  document.getElementById('note-body').value = '';
  document.getElementById('note-image').value = '';
  document.getElementById('note-session-name').value = '';
  setTodayDefault();
  document.getElementById('note-session-number').value = '';
  document.getElementById('note-category').value = '';
  document.getElementById('note-private').checked = false;
  document.getElementById('create-note').textContent = 'Create Note';
}

async function createNote() {
  const campaign_id = getCampaignId();
  const author_id = ensureLogin();
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
  await loadNotes();
  clearForm();
}

async function updateNote() {
  if (!editingNoteId) return;
  const title = document.getElementById('note-title').value;
  const body = document.getElementById('note-body').value;
  const image_url = document.getElementById('note-image').value;
  const session_name = document.getElementById('note-session-name').value;
  const session_date = document.getElementById('note-session-date').value;
  const session_number = document.getElementById('note-session-number').value;
  const category = document.getElementById('note-category').value;
  const is_private = document.getElementById('note-private').checked;
  const params = new URLSearchParams();
  if (title) params.append('title', title);
  if (body) params.append('body', body);
  if (image_url) params.append('image_url', image_url);
  if (session_name) params.append('session_name', session_name);
  if (session_date) params.append('session_date', session_date);
  if (session_number) params.append('session_number', session_number);
  if (category) params.append('category', category);
  if (is_private) params.append('is_private', 'true');
  const response = await fetch(`${apiUrl}/notes/${editingNoteId}`, {
    method: 'PUT',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: params
  });
  const data = await response.json();
  log(JSON.stringify(data, null, 2));
  await loadNotes();
  clearForm();
}

async function loadNotes() {
  const campaignId = getCampaignId();
  const response = await fetch(`${apiUrl}/notes?campaign_id=${campaignId}`);
  const notes = await response.json();
  const list = document.getElementById('notes-list');
  list.innerHTML = '';
  notes.forEach(n => {
    const item = document.createElement('li');
    const titleLink = document.createElement('a');
    titleLink.href = '#';
    titleLink.textContent = n.title;
    titleLink.addEventListener('click', () => {
      fillForm(n);
    });
    item.appendChild(titleLink);
    const meta = [];
    if (n.session_name) meta.push(`session: ${n.session_name}`);
    if (n.session_number) meta.push(`#${n.session_number}`);
    if (n.category) meta.push(`[${n.category}]`);
    const span = document.createElement('span');
    span.textContent = ' - ' + meta.join(' ') + ': ' + n.body;
    item.appendChild(span);
    list.appendChild(item);
  });
}

ensureLogin();
setTodayDefault();

document.getElementById('create-note').addEventListener('click', () => {
  if (editingNoteId) {
    updateNote();
  } else {
    createNote();
  }
});
document.getElementById('load-notes').addEventListener('click', loadNotes);
loadNotes();
