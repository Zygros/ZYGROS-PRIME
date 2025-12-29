async function loadConfig(){
  try{const r=await fetch('config.json');return await r.json()}catch(e){return {apiBase:'http://localhost:8011',defaultMinScore:97,defaultMaxRounds:5}}
}
function $(id){return document.getElementById(id)}
function show(el){el.hidden=false} function hide(el){el.hidden=true}
function logStatus(msg){$('status').textContent=msg}

async function postJSON(url, body){
  const r = await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body: JSON.stringify(body||{})})
  if(!r.ok) throw new Error('HTTP '+r.status); return await r.json()
}
async function getJSON(url){ const r=await fetch(url); if(!r.ok) throw new Error('HTTP '+r.status); return await r.json() }

async function main(){
  const cfg = await loadConfig()
  $('apiBase').value = cfg.apiBase || 'http://localhost:8011'
  $('minScore').value = cfg.defaultMinScore ?? 97
  $('maxRounds').value = cfg.defaultMaxRounds ?? 5

  $('btnRun').addEventListener('click', async ()=>{
    const base = $('apiBase').value.trim()
    const minScore = parseFloat($('minScore').value)||97
    const rounds = parseInt($('maxRounds').value)||5
    logStatus('Running until ≥ '+minScore+' ...')
    try{
      const data = await postJSON(base+'/self_assess/until?min_score='+minScore+'&max_rounds='+rounds,{})
      $('results').textContent = JSON.stringify(data,null,2)
      show($('resultsCard'))
      logStatus('Done.')
      localStorage.setItem('cisSelfAssessCfg', JSON.stringify({apiBase:base,defaultMinScore:minScore,defaultMaxRounds:rounds}))
    }catch(e){
      logStatus('Error: '+e.message+'\nTip: open the kernel server (port 8011) or update URL.')
    }
  })

  $('btnOnce').addEventListener('click', async ()=>{
    const base = $('apiBase').value.trim()
    logStatus('Running once...')
    try{
      const data = await postJSON(base+'/self_assess/once',{})
      $('results').textContent = JSON.stringify(data,null,2)
      show($('resultsCard'))
      logStatus('Done.')
    }catch(e){ logStatus('Error: '+e.message) }
  })

  $('btnStatus').addEventListener('click', async ()=>{
    const base = $('apiBase').value.trim()
    logStatus('Checking status...')
    try{
      const data = await getJSON(base+'/self_assess/status')
      $('results').textContent = JSON.stringify(data,null,2)
      show($('resultsCard'))
      logStatus('Done.')
    }catch(e){ logStatus('Error: '+e.message) }
  })

  // PWA install
  if('serviceWorker' in navigator){ try{ await navigator.serviceWorker.register('sw.js') }catch(e){ /* ignore */ } }
}
main()
