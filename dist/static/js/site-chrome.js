/* AAKAAR — shared header behaviour (mobile menu + active link) */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var burger = document.querySelector('[data-aa-burger]');
    var panel = document.querySelector('[data-aa-mobile]');

    if (burger && panel) {
      burger.addEventListener('click', function () {
        var open = panel.classList.toggle('is-open');
        burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
      panel.querySelectorAll('a').forEach(function (a) {
        a.addEventListener('click', function () {
          panel.classList.remove('is-open');
          burger.setAttribute('aria-expanded', 'false');
        });
      });
    }

    var path = (window.location.pathname || '/').replace(/\/+$/, '') || '/';
    var hash = window.location.hash;
    var best = null;
    var bestLen = 0;

    document.querySelectorAll('.aa-nav a[data-nav]').forEach(function (a) {
      var href = a.getAttribute('href') || '';
      if (href.charAt(0) !== '/') { return; }
      var target = href.split('#')[0].replace(/\/+$/, '') || '/';
      if (target === '/') { return; }
      if (path === target || path.indexOf(target + '/') === 0) {
        if (target.length > bestLen) {
          best = a;
          bestLen = target.length;
        }
      }
    });

    if (!best && path === '/') {
      best = document.querySelector('.aa-nav a[data-nav="home"]');
    }

    if (best) {
      best.classList.add('is-active');
    } else if (path === '/' && hash === '#about') {
      var about = document.querySelector('.aa-nav a[data-nav="about"]');
      if (about) { about.classList.add('is-active'); }
    }
  });
})();
