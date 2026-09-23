(() => {
  'use strict';
  const root = document.documentElement;
  const themeButton = document.querySelector('.theme-toggle');
  const preference = window.matchMedia('(prefers-color-scheme: light)');
  let explicitTheme = false;
  try { explicitTheme = ['light', 'dark'].includes(localStorage.getItem('rupok-theme')); } catch (_) {}
  function updateTheme(theme) {
    root.dataset.theme = theme;
    themeButton.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`);
    document.querySelector('meta[name="theme-color"]').content = theme === 'dark' ? '#101413' : '#f5f5ee';
  }
  updateTheme(root.dataset.theme);
  themeButton.addEventListener('click', () => {
    const theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    explicitTheme = true;
    updateTheme(theme);
    try { localStorage.setItem('rupok-theme', theme); } catch (_) {}
  });
  preference.addEventListener('change', e => { if (!explicitTheme) updateTheme(e.matches ? 'light' : 'dark'); });
  const menuButton = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#navigation');
  function closeMenu() {
    navigation.classList.remove('is-open');
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.querySelector('span').textContent = '+';
  }
  menuButton.addEventListener('click', () => {
    const open = navigation.classList.toggle('is-open');
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.querySelector('span').textContent = open ? '−' : '+';
  });
  navigation.addEventListener('click', e => { if (e.target.closest('a')) closeMenu(); });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && navigation.classList.contains('is-open')) { closeMenu(); menuButton.focus(); }
  });
  document.addEventListener('click', e => { if (!e.target.closest('.site-header')) closeMenu(); });
  window.matchMedia('(min-width: 761px)').addEventListener('change', closeMenu);
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        const link = navigation.querySelector(`a[href="#${entry.target.id}"]`);
        if (link) {
          if (entry.isIntersecting) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        }
      });
    }, { rootMargin: '-15% 0px -50% 0px' });
    document.querySelectorAll('section[id]').forEach(section => observer.observe(section));

    if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      root.classList.add('reveal-ready');
      const revealItems = document.querySelectorAll('.section-heading, .work-card, .capabilities > div, .experience-row, .portrait-wrap, .about-copy, .public-outreach, .publication-list > a, .contact-inner');
      revealItems.forEach(item => item.classList.add('reveal-item'));
      const revealObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-visible');
          revealObserver.unobserve(entry.target);
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
      revealItems.forEach(item => revealObserver.observe(item));
    }
  }
  document.querySelector('#copy-email').addEventListener('click', async () => {
    const status = document.querySelector('#copy-status');
    try { await navigator.clipboard.writeText('contact@rupokri.ca'); status.textContent = 'Email copied. Let’s connect!'; }
    catch (_) { status.textContent = 'You can email me at contact@rupokri.ca.'; }
  });
  document.querySelector('#year').textContent = new Date().getFullYear();
})();
