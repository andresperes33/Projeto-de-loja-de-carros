function toggleMenu() {
  const menu = document.getElementById('navMenu');
  menu.classList.toggle('active');
}

// Fecha menu ao clicar em um link (mobile)
document.querySelectorAll('#navMenu a').forEach(link => {
  link.addEventListener('click', () => {
    if (window.innerWidth <= 968) {
      document.getElementById('navMenu').classList.remove('active');
    }
  });
});

// Fecha menu ao clicar fora (mobile)
document.addEventListener('click', (e) => {
  const nav = document.querySelector('nav');
  const menu = document.getElementById('navMenu');

  if (window.innerWidth <= 968 &&
    !nav.contains(e.target) &&
    menu.classList.contains('active')) {
    menu.classList.remove('active');
  }
});
