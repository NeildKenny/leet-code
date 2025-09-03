function updateThemeIcon() {
  const btn = document.getElementById('toggle-theme');
  if (!btn) return;
  if (document.body.classList.contains('dark')) {
    btn.textContent = '☀️';
  } else {
    btn.textContent = '🌙';
  }
}

function toggleTheme() {
  document.body.classList.toggle('dark');
  document.body.classList.toggle('light');
  updateThemeIcon();
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-theme');
  if (btn) {
    btn.addEventListener('click', toggleTheme);
    updateThemeIcon();
  }
});
