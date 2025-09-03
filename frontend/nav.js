function addNav() {
  const toggle = document.createElement('button');
  toggle.id = 'nav-toggle';
  toggle.className = 'nav-toggle';
  toggle.textContent = '«';

  const nav = document.createElement('nav');
  nav.className = 'nav';
  nav.innerHTML = `
    <ul>
      <li><a href="login.html">Login</a></li>
      <li><a href="register.html">Register</a></li>
      <li><a href="campaigns.html">Campaigns</a></li>
      <li><a href="notes.html">Notes</a></li>
    </ul>`;

  document.body.appendChild(toggle);
  document.body.appendChild(nav);
  document.body.classList.add('with-nav');

  toggle.addEventListener('click', () => {
    nav.classList.toggle('collapsed');
    document.body.classList.toggle('nav-collapsed');
    toggle.textContent = nav.classList.contains('collapsed') ? '☰' : '«';
  });
}

document.addEventListener('DOMContentLoaded', addNav);
