const apiUrl = 'http://localhost:8001';

function ensureLogin() {
  const userId = sessionStorage.getItem('user_id');
  if (!userId) {
    window.location.href = 'login.html';
  }
  return userId;
}

function toggleTheme() {
  document.body.classList.toggle('dark');
  document.body.classList.toggle('light');
}

document.getElementById('toggle-theme').addEventListener('click', toggleTheme);

async function loadCampaigns() {
  const userId = ensureLogin();
  const response = await fetch(`${apiUrl}/campaigns?user_id=${userId}`);
  const campaigns = await response.json();
  const list = document.getElementById('campaign-list');
  list.innerHTML = '';
  campaigns.forEach(c => {
    const item = document.createElement('li');
    const link = document.createElement('a');
    link.textContent = c.name;
    link.href = `notes.html?campaign_id=${c.id}`;
    item.appendChild(link);
    list.appendChild(item);
  });
}

async function createCampaign() {
  const name = document.getElementById('campaign-name').value;
  const description = document.getElementById('campaign-description').value;
  const userId = ensureLogin();
  const params = new URLSearchParams({ name, dm_id: userId });
  if (description) params.append('description', description);
  const response = await fetch(`${apiUrl}/campaigns`, {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: params
  });
  if (response.ok) {
    await loadCampaigns();
  } else {
    alert('Failed to create campaign');
  }
}

document.getElementById('create-campaign').addEventListener('click', createCampaign);

loadCampaigns();
