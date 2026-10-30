/* Mobile menu toggle for the AAKAAR design header. */
(function () {
    function ready(fn) {
        if (document.readyState !== 'loading') { fn(); }
        else { document.addEventListener('DOMContentLoaded', fn); }
    }

    ready(function () {
        var toggles = document.querySelectorAll('[data-aa-menu-toggle]');
        var panels = document.querySelectorAll('[data-aa-menu-panel]');
        if (!toggles.length || !panels.length) { return; }

        function close() {
            Array.prototype.forEach.call(panels, function (p) { p.classList.add('hidden'); });
            Array.prototype.forEach.call(toggles, function (t) {
                t.setAttribute('aria-expanded', 'false');
            });
        }

        Array.prototype.forEach.call(toggles, function (btn) {
            btn.addEventListener('click', function () {
                var panel = document.querySelector('[data-aa-menu-panel]');
                if (!panel) { return; }
                var isOpen = !panel.classList.contains('hidden');
                close();
                if (!isOpen) {
                    panel.classList.remove('hidden');
                    btn.setAttribute('aria-expanded', 'true');
                }
            });
        });

        window.addEventListener('resize', function () {
            if (window.innerWidth >= 1024) { close(); }
        });
    });
})();
