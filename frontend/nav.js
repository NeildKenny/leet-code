function addNav() {
  const nav = document.createElement('nav');
  nav.className = 'nav';
  nav.innerHTML = `
    <ul>
      <li><a href="login.html">Login</a></li>
      <li><a href="register.html">Register</a></li>
      <li><a href="campaigns.html">Campaigns</a></li>
      <li><a href="notes.html">Notes</a></li>
    </ul>`;
  document.body.appendChild(nav);
  document.body.classList.add('with-nav');
}

document.addEventListener('DOMContentLoaded', addNav);
