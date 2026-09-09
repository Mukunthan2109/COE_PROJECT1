if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/static/sw.js')
      .then((reg) => {
        console.log('CropTriage PWA Service Worker registered:', reg.scope);
      })
      .catch((err) => {
        console.log('PWA Service Worker registration failed:', err);
      });
  });
}
