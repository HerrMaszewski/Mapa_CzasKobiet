module.exports = {
  // Pliki HTML i szablony Django
  content: [
    './Mapa_CzasKobiet/mapa/templates/**/*.html', // wszystkie szablony
  ],
  // CSS do oczyszczenia
  css: [
    './Mapa_CzasKobiet/mapa/static/css/*.css',  // wszystkie pliki CSS w katalogu css
  ],
  // Folder wyjściowy z oczyszczonym CSS
  output: './Mapa_CzasKobiet/mapa/static/css/cleaned',
}