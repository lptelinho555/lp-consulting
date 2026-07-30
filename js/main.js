/* Luiz Paulo Consulting — scripts do site */
(function () {
    'use strict';

    // Ano corrente no rodape
    var yearEl = document.getElementById('year');
    if (yearEl) {
        yearEl.textContent = new Date().getFullYear();
    }

    // Menu mobile
    var toggle = document.querySelector('.nav-toggle');
    var menu = document.querySelector('.nav-menu');
    if (!toggle || !menu) {
        return;
    }

    function setOpen(open) {
        menu.classList.toggle('is-open', open);
        toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    }

    toggle.addEventListener('click', function () {
        setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });

    // Fecha ao clicar num link do menu
    menu.addEventListener('click', function (event) {
        if (event.target.closest('a')) {
            setOpen(false);
        }
    });

    // Fecha com ESC e devolve o foco ao botao
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
            setOpen(false);
            toggle.focus();
        }
    });

    // Se voltar para desktop com o menu aberto, limpa o estado.
    // 1024px deve acompanhar o breakpoint do menu em css/style.css
    window.addEventListener('resize', function () {
        if (window.innerWidth > 1024) {
            setOpen(false);
        }
    });
})();
