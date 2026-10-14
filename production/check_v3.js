const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const root=path.resolve(__dirname,'..');
const w=JSON.parse(fs.readFileSync(path.join(root,'workflow.json'),'utf8'));
const source=JSON.parse(fs.readFileSync(path.join(root,'production/adopted_source_v3.json'),'utf8'));
const old=JSON.parse(fs.readFileSync(path.join(root,'production/history/revision_v2/workflow.json'),'utf8'));
const seconds=s=>{const [m,t]=s.split(':').map(Number);return m*60+t};
const matched=[];
for(let i=0;i<31;i++){
 const c=w.clips[i];
 assert.equal(c.start,seconds(source[i].start));assert.equal(c.end,seconds(source[i].end));
 let expected=source[i].speech;if(i===27)expected=expected.replace(/ 고마워\.$/,'');if(i===30)expected='고마워.';
 assert.equal(c.speech,expected,c.id+' source dialogue mismatch');matched.push(c.id);
 if(i<30)assert.equal(c.sound,source[i].sound,c.id+' source sound mismatch');
 if(i<30&&i!==24)assert.equal(c.event,source[i].event,c.id+' source direction mismatch');
}
assert.equal(w.clips.filter(c=>c.speech.includes('고마워')).length,1);
assert.equal(w.clips[30].speech,'고마워.');
assert.equal(w.clips[31].start,188);assert.equal(w.clips[31].end,194);
assert.equal(w.clips[30].end_state,w.clips[31].start_state);
assert.equal(w.clips[31].timeline.at(-1).end-w.clips[31].timeline.at(-1).start,1);
assert.equal(w.clips[28].timeline[1].end-w.clips[28].timeline[1].start,3);
assert.equal(w.clips[27].start,170);
const html=fs.readFileSync(path.join(root,'review.html'),'utf8');
const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
for(const [i,s] of scripts.entries())new vm.Script(s[1],{filename:'review-inline-'+i});
assert(html.includes('VERSION 03')&&html.includes('03:14'));
assert(!html.includes('씨익 웃고 종료.')&&!html.includes('첫 두 핵심 대사는 원문'));
for(const p of [...html.matchAll(/(?:src|href)="([^"]+)"/g)].map(m=>m[1])){
 if(!p.startsWith('#')&&!p.includes('$')&&!p.includes('\\')&&!p.includes("'+")&&!p.startsWith('http'))assert(fs.existsSync(path.join(root,p)),p);
}
const changedImages=w.boards.filter(b=>old.boards.find(o=>o.id===b.id)?.sha256!==b.sha256).map(b=>b.id);
assert.deepEqual(changedImages,['SB04','SB25','SB27','SB32']);
const speechRates=w.clips.filter(c=>c.speech).map(c=>({clip:c.id,hangul_syllables:(c.speech.match(/[가-힣]/g)||[]).length,allocated_seconds:Math.round((c.speech_end-c.speech_start)*100)/100}));
for(const r of speechRates)r.syllables_per_second=+(r.hangul_syllables/r.allocated_seconds).toFixed(2);
const report={ok:true,revision:'v3',source_dialogue_matches:matched,timing_of_original_31_clips_preserved:true,reveal_at:170,duration:194,thanks_only_in:'C031',new_exit_clip:'C032',changed_images:changedImages,reused_images:28,review_html_script_syntax:'valid',review_file_links:'valid',browser_render_check:'not rerun; existing browser policy blocks file URLs',speech_budget_estimate:speechRates,limitations:'음절 수/시간은 길이 추정이며 실제 발화·립싱크 검증이 아님.'};
fs.writeFileSync(path.join(root,'production/revision_v3_check.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({...report,source_dialogue_matches:matched.length,speech_budget_estimate:'max '+Math.max(...speechRates.map(r=>r.syllables_per_second))+' syllables/s'}));
