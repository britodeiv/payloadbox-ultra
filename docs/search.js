// docs/search.js — Lunr-based client search + safe preview
(async function(){
  const resp = await fetch('data/payloads.json');
  const data = await resp.json();
  const idx = lunr(function(){
    this.ref('id');
    this.field('payload');
    this.field('tags');
    this.field('notes');
    data.forEach(d=> this.add({id:d.id, payload:d.payload, tags:(d.tags||[]).join(' '), notes:d.notes||''}));
  });
  const q=document.getElementById('q'), results=document.getElementById('results');
  const vector=document.getElementById('vector'), context=document.getElementById('context'), minscore=document.getElementById('minscore');
  function populateFilters(){
    [...new Set(data.map(d=>d.vector))].sort().forEach(v=>vector.appendChild(new Option(v,v)));
    [...new Set(data.map(d=>d.context))].sort().forEach(c=>context.appendChild(new Option(c,c)));
  }
  function render(list){
    results.innerHTML = list.map(i=>{
      const safe = i.payload.replace(/</g,'&lt;').replace(/>/g,'&gt;');
      return `<div class="item"><h3>${i.id} <small>${i.vector}/${i.context} • score:${i.score}</small></h3>
        <pre>${safe}</pre>
        <div><button data-copy="${i.payload}">Copy</button> <button data-preview="${i.payload}">Preview (sandbox)</button></div>
        <p>${i.notes||''}</p></div>`;
    }).join('');
    document.querySelectorAll('button[data-copy]').forEach(b=> b.onclick = ()=> navigator.clipboard.writeText(b.getAttribute('data-copy')));
    document.querySelectorAll('button[data-preview]').forEach(b=> b.onclick = ()=>{
      const w = window.open('about:blank','preview','noopener');
      w.document.write('<meta charset="utf-8"><h3>Sandbox preview (escaped)</h3><pre>'+b.getAttribute('data-preview').replace(/</g,'&lt;')+'</pre>');
    });
  }
  function filter(){
    const term = q.value.trim();
    const v = vector.value, c = context.value, minS = Number(minscore.value);
    let ids = term ? idx.search(term).map(r=>r.ref) : data.map(d=>d.id);
    let out = data.filter(d=> ids.includes(d.id));
    if(v) out = out.filter(d=>d.vector===v);
    if(c) out = out.filter(d=>d.context===c);
    out = out.filter(d => (d.score||0) >= minS);
    render(out);
  }
  q.addEventListener('input', filter); vector.addEventListener('change', filter); context.addEventListener('change', filter); minscore.addEventListener('input', filter);
  populateFilters(); render(data);
})();
