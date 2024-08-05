i18next
    .use(i18nextBrowserLanguageDetector)
    .use(i18nextHttpBackend)
    .init({
        debug: true,
        fallbackLng: 'en',
        backend: {
            loadPath: 'static/json/locales/{{lng}}.json'
        }
    }, function(err, t) {
        if (err) return console.error(err);
        updateContent();
    });

function updateContent() {
    document.querySelector('h1').innerHTML = i18next.t('title');
    document.querySelector('p').innerHTML = i18next.t('welcomeMessage');
}

function changeLanguage(lng) {
    i18next.changeLanguage(lng, updateContent);
}

document.addEventListener('DOMContentLoaded', function() {
    updateContent();
});
