// Carrega dinamicamente o Chart.js via CDN
(function() {
    var script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
    script.onload = function() {
        console.log('Chart.js carregado');
    };
    document.head.appendChild(script);
})();