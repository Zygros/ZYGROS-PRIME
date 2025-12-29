self.addEventListener('install',e=>{
  e.waitUntil(caches.open('cis-assess-v1').then(c=>c.addAll([
    './','./index.html','./styles.css','./app.js','./manifest.json','./config.json'
  ])))
})
self.addEventListener('fetch',e=>{
  e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request)))
})