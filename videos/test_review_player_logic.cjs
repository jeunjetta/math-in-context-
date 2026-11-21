// Built-in Node APIs only. DOM shims test logic, NOT layout, playback or browser safety.
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const {webcrypto}=require('node:crypto');
const html=fs.readFileSync(__dirname+'/fft-latency/review-player.html','utf8');
const data=html.match(/<script id="candidate-data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const code=html.match(/<script>\s*([\s\S]*?)<\/script>/)[1];
function element(){return {disabled:true,textContent:'',value:'',checked:false,files:[],duration:28,currentTime:0,
 listeners:{},addEventListener(name,fn){this.listeners[name]=fn},pause(){},load(){},click(){}};}
const ids=['candidate-data','movie','files','status','identity','cut-a','cut-b','closing','mark','note','kind','saved','notes','preference','watched-a','watched-b','download'];
const elements=Object.fromEntries(ids.map(id=>[id,element()]));elements['candidate-data'].textContent=data;
elements.preference.value='undecided';elements.kind.value='Pacing';
const blobs=[],revoked=[];
const context=vm.createContext({document:{getElementById:id=>elements[id],createElement:()=>element()},
 window:{addEventListener(){}},crypto:webcrypto,Blob,Uint8Array,setTimeout:fn=>fn(),
 URL:{createObjectURL(blob){blobs.push(blob);return 'blob:test-'+blobs.length},revokeObjectURL:url=>revoked.push(url)}});
vm.runInContext(code,context);
async function run(){
 elements.files.files=[{size:3,arrayBuffer:async()=>Buffer.from('bad')}];await elements.files.onchange();
 assert.match(elements.status.textContent,/Unknown movie bytes/);assert.equal(blobs.length,0);
 elements.files.files=[{size:10000001}];await elements.files.onchange();assert.match(elements.status.textContent,/10 MB/);
 // Injecting a matching state below is a unit fixture, NOT a SHA verification claim.
 vm.runInContext("loaded.set('b',{url:'blob:fixture'});choose('b')",context);
 elements.movie.duration=34;elements.movie.listeners.loadedmetadata();assert.equal(elements.mark.disabled,false);
 elements.closing.onclick();assert.equal(elements.movie.currentTime,22);
 elements.note.value='<img src=x onerror=alert(1)>';elements.mark.onclick();
 assert.match(elements.notes.textContent,/34-second cut @ 22 s/);assert.match(elements.notes.textContent,/<img/);
 const record=JSON.parse(vm.runInContext('JSON.stringify(feedback())',context));
 assert.equal(record.publication_approved,false);assert.equal(record.notes[0].candidate,'b');assert.equal(record.notes[0].seconds,22);
 assert.equal(record.candidates.b.sha256,JSON.parse(data).b.sha256);assert.equal(record.playback_self_report.b,false);
 elements.movie.duration=28;elements.movie.listeners.loadedmetadata();assert.equal(elements.mark.disabled,true);assert.match(elements.status.textContent,/Duration mismatch/);
 elements.download.onclick();assert.equal(blobs.length,1);assert.equal(revoked.length,1);
 const exported=JSON.parse(await blobs[0].text());assert.equal(exported.publication_approved,false);
 assert.equal(exported.status,'draft human feedback, not approval');
 console.log('Logic PASS: unknown/oversize rejection, fixture switch/seek/note, literal text, exact-identity export, duration block and URL cleanup.');
 console.log('DOM shims do not verify real browser hashing acceptance, native media, layout, keyboard, accessibility or tablet behavior.');
}
run().catch(e=>{console.error(e);process.exitCode=1});
