(function(){
 const root=document.documentElement;
 const saved=localStorage.getItem('focusboard-theme');
 if(saved==='dark'||saved==='light')root.setAttribute('data-bs-theme',saved);
 function updateTheme(){const b=document.getElementById('themeToggle');if(!b)return;const dark=root.getAttribute('data-bs-theme')==='dark';b.innerHTML=dark?'<i class="bi bi-sun-fill"></i>':'<i class="bi bi-moon-stars-fill"></i>';b.title=dark?'Ativar modo claro':'Ativar modo escuro'}
 const theme=document.getElementById('themeToggle');if(theme){theme.addEventListener('click',()=>{const next=root.getAttribute('data-bs-theme')==='dark'?'light':'dark';root.setAttribute('data-bs-theme',next);localStorage.setItem('focusboard-theme',next);updateTheme()});updateTheme()}
 const menu=document.getElementById('mobileMenu');const sidebar=document.getElementById('appSidebar');if(menu&&sidebar)menu.addEventListener('click',()=>sidebar.classList.toggle('open'));
 async function carregarFrase(){const target=document.getElementById('fraseMotivacional');if(!target)return;target.textContent='Carregando...';try{const r=await fetch('/api/frase');const d=await r.json();target.textContent='“'+d.frase+'”'}catch(e){target.textContent='“Continue aprendendo: pequenos passos constroem grandes resultados.”'}}
 const q=document.getElementById('novaFrase');if(q){q.addEventListener('click',carregarFrase);carregarFrase()}
})();
