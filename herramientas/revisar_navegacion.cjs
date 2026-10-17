// Ejecutar desde la raíz: node herramientas/revisar_navegacion.cjs
// Requiere Playwright y Chromium. TRIA_CHROMIUM permite usar un ejecutable ya instalado.
// Las llamadas a API están simuladas; no modifica servidores ni descarga mapas.
const {chromium}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('assert');
const server=http.createServer((q,r)=>{
  const url=new URL(q.url,'http://localhost');
  let path='prototipo'+(url.pathname==='/'?'/index.html':url.pathname);
  try{r.setHeader('Content-Type',path.endsWith('.js')?'text/javascript':path.endsWith('.html')?'text/html':'application/octet-stream');r.end(fs.readFileSync(path))}
  catch{r.writeHead(404);r.end()}
}).listen(8765);
(async()=>{
  const b=await chromium.launch({...(process.env.TRIA_CHROMIUM?{executablePath:process.env.TRIA_CHROMIUM}:{}),args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu','--no-zygote'],headless:true});
  try{
    for(const mobile of [false,true]){
      const c=await b.newContext({viewport:mobile?{width:390,height:844}:{width:1440,height:1000},reducedMotion:'reduce'});
      const p=await c.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));
      let requests=0,posts=0,fail=false;
      await p.route('**/*',async route=>{
        const u=new URL(route.request().url());
        if(u.hostname!=='127.0.0.1')return route.abort();
        if(['/estado','/prioridades','/asignacion'].includes(u.pathname)){
          requests++;
          if(fail)return route.fulfill({status:503,body:'offline'});
          const body=u.pathname==='/estado'?{minuto:12,consistencia:0.02,requiere_clave:true}:u.pathname==='/prioridades'?[{zona:'BRU',nombre:'Bruselas',en_silencio:true,color:'rojo',personas:0,heridos:0,latido:true,medio:'baliza',necesidades:[],indice:.8,aportes:{}}]:[];
          return route.fulfill({contentType:'application/json',body:JSON.stringify(body)});
        }
        if(route.request().method()==='POST'){posts++;return route.fulfill({contentType:'application/json',body:'{"ok":true}'})}
        return route.continue();
      });
      await p.goto('http://127.0.0.1:8765');await p.waitForTimeout(150);
      assert.equal(errors.length,0,errors.join(';'));
      assert(await p.locator('#inicio').isVisible());assert(!(await p.locator('#layout').isVisible()));assert.equal(requests,0);
      assert(!(await p.locator('#guia').evaluate(e=>e.open)));
      await p.screenshot({path:'/tmp/tria-inicio-'+(mobile?'movil':'desktop')+'.png',fullPage:true});
      await p.locator('#inicio [data-vista="mapa"]').click();await p.locator('#guia[open]').waitFor();await p.locator('#guiaOmitir').click();
      assert(await p.locator('#map').isVisible());assert(await p.locator('.side').isVisible());assert(await p.locator('#tab-prio').isVisible());
      const cajas=await p.evaluate(()=>{const m=document.querySelector('.mapcard').getBoundingClientRect(),s=document.querySelector('.side').getBoundingClientRect();return{m:{x:m.x,y:m.y,w:m.width,h:m.height},s:{x:s.x,y:s.y,w:s.width,h:s.height}}});
      if(mobile)assert(cajas.s.y>=cajas.m.y+cajas.m.h-2,'el panel móvil debe quedar debajo del mapa');
      else assert(cajas.s.x>=cajas.m.x+cajas.m.w-2,'el panel debe quedar a la derecha del mapa');
      await p.screenshot({path:'/tmp/tria-mapa-'+(mobile?'movil':'desktop')+'.png',fullPage:true});
      await p.locator('#btnStep').click();await p.waitForTimeout(1200);
      const time=await p.locator('#tplus').textContent();
      for(const id of ['rec','log','prio']){
        await p.locator('.tabs [data-tab="'+id+'"]').click();
        assert(await p.locator('#tab-'+id).isVisible());assert(await p.locator('#map').isVisible());
        assert.equal(await p.locator('body').getAttribute('data-vista'),'mapa');
      }
      await p.locator('#secciones [data-vista="model"]').click();assert(await p.locator('#tab-model').isVisible());assert(!(await p.locator('#map').isVisible()));
      await p.locator('#secciones [data-vista="mapa"]').click();assert(await p.locator('#map').isVisible());assert(await p.locator('.side').isVisible());
      await p.locator('#btnPlay').click();
      await p.locator('#secciones [data-vista="live"]').click();
      await p.waitForFunction(()=>document.querySelector('#liveEstado').textContent.includes('Conectado'));
      assert(!(await p.locator('#simulacionControles').isVisible()));assert(!(await p.locator('#map').isVisible()));
      const paused=await p.locator('#tplus').textContent();await p.keyboard.press('ArrowRight');await p.keyboard.press(' ');await p.waitForTimeout(700);
      assert.equal(await p.locator('#tplus').textContent(),paused);
      assert((await p.locator('#liveActualizado').textContent()).includes('Última consulta correcta'));
      await p.screenshot({path:'/tmp/tria-live-'+(mobile?'movil':'desktop')+'.png',fullPage:true});
      await p.locator('#liveDemo summary').click();
      p.once('dialog',d=>d.dismiss());await p.locator('#lvReporte').click();assert.equal(posts,0);
      p.once('dialog',d=>d.accept());await p.locator('#lvReporte').click();await p.waitForTimeout(100);assert.equal(posts,1);
      fail=true;await p.locator('#secciones [data-vista="inicio"]').click();await p.locator('#inicio [data-vista="live"]').click();
      await p.waitForFunction(()=>document.querySelector('#liveEstado').textContent.includes('Sin conexión'));
      assert((await p.locator('#liveActualizado').textContent()).includes('Datos sin actualizar'));
      assert(await p.locator('#configConexion').evaluate(e=>e.open));
      await p.locator('#secciones [data-vista="inicio"]').click();const count=requests;
      await p.waitForTimeout(5500);assert.equal(requests,count);
      await p.reload();assert(!(await p.locator('#guia').evaluate(e=>e.open)));
      await p.locator('#inicio [data-vista="mapa"]').click();assert(!(await p.locator('#guia').evaluate(e=>e.open)));
      assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'overflow horizontal');
      assert.deepEqual(errors,[]);
      console.log((mobile?'Móvil':'Escritorio')+': inicio, guía, navegación, estado conservado, aislamiento API, pausa/atajos, confirmación, fallo de conexión y fin de sondeo OK');
      await c.close();
    }
  } finally {await b.close();server.close()}
})().catch(e=>{console.error(e);process.exitCode=1;server.close()});
