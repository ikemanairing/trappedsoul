from pathlib import Path
import json
root=Path(__file__).resolve().parent.parent
p=root/'production/build.js'
s=p.read_text(encoding='utf-8')
def sub(old,new):
 global s
 assert old in s, old[:100]
 s=s.replace(old,new)
sub("'의자는 비어 있다. 웹캠은 모니터 위에서 방 안을 향한다. 침대는 화면 왼쪽, 열린 문은 오른쪽이다.'", "i<30?'@Image2의 여성 한 명이 @Image1의 침실 중앙 검은 사무용 의자에 앉는다. 웹캠은 모니터 위에서 여성을 향한다. 침대는 화면 왼쪽, 열린 문은 오른쪽이다.':'앞서 갇힌 방에 있던 @Image1의 동일한 남성 한 명이 @Image2의 침실 중앙 검은 사무용 의자에 앉는다. 웹캠은 모니터 위에서 남성을 향한다. 침대는 화면 왼쪽, 열린 문은 오른쪽이다.'")
sub("'사람 없는 의자와 침대, 열린 문의 위치를 유지한다.'", "i<30?'같은 성인 여성 한 명의 얼굴·머리·청회색 긴팔 상의, 사무용 의자 한 개, 침대와 열린 문의 방향, 웹캠 높이와 화각을 유지한다.':'원래 남성 한 명의 얼굴·짧은 검은 머리·차콜 긴팔 상의를 유지한다. 여성의 침실, 중앙 사무용 의자 한 개, 왼쪽 침대와 오른쪽 열린 문, 동일한 웹캠 높이와 화각을 유지한다.'")
sub("(i<28?assets.slice(0,2):assets.slice(2)).map(a=>a.path)","assetsForClip(i).map(a=>a.path)")
sub("'Reference image 1 defines the ordinary bedroom and exact furniture placement. No people are present.'", "i<30?'Reference image 1 defines the ordinary bedroom and exact furniture placement; reference image 2 defines the adult female viewer identity and blue shirt. One woman only.':'Reference image 1 defines the original male identity and charcoal shirt; reference image 2 defines the ordinary viewer bedroom. One man only.'")
sub("json('production/board_plan.json',boardPlan);", """const endingRecords=JSON.parse(fs.readFileSync(path.join(root,'production/ending_v2_generation_records.json'),'utf8'));
for(const b of boardPlan){const r=endingRecords.find(r=>r.id===b.id);if(r){b.prompt=r.prompt;b.references=[...new Set([...b.references,...r.refs])];b.generation_references=r.refs;}}
json('production/board_plan.json',boardPlan);""")
sub("const skillPath=", """for(const b of boards){const old=priorWorkflow.boards.find(x=>x.id===b.id);if(old&&Number(b.id.slice(2))<29){b.inputs=old.inputs;}}
const skillPath=""")
sub("schema_version:1,project:","schema_version:1,revision:'v2',project:")
sub("review:{accepted_boards:[],evidence:[]},changes:[]", "review:{...priorWorkflow.review,accepted_boards:(priorWorkflow.review.accepted_boards||[]).filter(b=>!['SB29','SB30','SB31'].includes(typeof b==='string'?b:b.id))},changes:[...(priorWorkflow.changes||[]),{reason:'사용자 요청: 여성 시청자 3초, 놀라는 반응, 같은 자리의 기존 남성으로 즉시 교체, 웹캠을 보며 씨익 웃고 종료.',affected_clips:['C029','C030','C031'],affected_assets:['A02'],affected_boards:['SB29','SB30','SB31'],previous_version:'v1',version:'v2',review_status:'awaiting_user_review',open_issues:[]}]")
sub("boards.length===30&&Object.keys(qa).length>=30", "boards.length===clips.length&&boards.every(b=>b.qa.status==='visually_checked')")
sub("boards.length===30?[]", "boards.length===clips.length?[]")
sub('제작 패키지 v1','제작 패키지 v2')
sub('독립 프롬프트 30개, 실제 참조 이미지 3개','독립 프롬프트 ${clips.length}개, 실제 참조 이미지 ${assets.length}개')
sub('C029–C030은 Image1.png 한 장만 사용합니다.','C029–C030은 Image1.png=침실(B02), Image2.png=여성(A02)입니다. C031은 Image1.png=기존 남성(A01), Image2.png=침실(B02)입니다.')
sub('C029 첫 1초는 검정 화면을 편집으로 넣고 이어 가짜 웹캠 화면을 연결합니다.','C029는 02:58–02:59 검정 화면 뒤 02:59–03:02 여성의 평범한 시청 모습 3초를 연결합니다. C030은 03:02–03:04 여성의 놀라는 반응입니다. 03:04에 여성 마지막 화면에서 같은 자리의 남성 첫 화면으로 즉시 컷 전환합니다. C031은 남성이 렌즈를 보며 씨익 웃고 03:08에 종료합니다. 방·의자 위치·화각을 맞추고, 두 사람이 겹치거나 중간 모습으로 변형되는 전환을 사용하지 않습니다.')
sub('VERSION 01','VERSION 02')
sub('<b>30</b><span>클립 / 독립 포토 보드','<b>${clips.length}</b><span>클립 / 독립 포토 보드')
sub('참조 이미지 3장은','참조 이미지 ${assets.length}장은')
sub('포토 보드 30장은','포토 보드 ${clips.length}장은')
sub("grid.children.length+' / 30 SCENES'","grid.children.length+' / '+clips.length+' SCENES'")
sub('Math.min(29,i)','Math.min(clips.length-1,i)')
sub("+(selected+1)+' of 30'","+(selected+1)+' of '+clips.length")
sub('<div class="links"><a href="script.txt">', '<p class="note">수정된 엔딩 · 여성 시청자 3초 → 놀라는 반응 2초 → 같은 자리에 남성 등장 → 웹캠을 보며 씨익 웃고 종료. <a href="#ending" id="endingLink">새 엔딩 보기</a></p><div class="links"><a href="script.txt">')
sub('});render();', "});render();document.getElementById('endingLink').onclick=()=>{document.querySelector('[data-filter=\\\"4\\\"]').click();document.getElementById('grid').scrollIntoView({behavior:'smooth'});};if(location.hash==='#ending')document.getElementById('endingLink').click();")
p.write_text(s,encoding='utf-8')

qa=json.loads((root/'production/visual_qa.json').read_text(encoding='utf-8'))
notes={'SB29':'성인 여성 한 명, 청회색 긴팔, 평범한 닫힌 입과 편안한 어깨. 왼쪽 침대·오른쪽 열린 문·중앙 검은 의자 확인.','SB30':'SB29와 같은 여성·의상·침실·카메라 구도. 넓어진 눈·벌어진 입·올라간 어깨의 놀란 반응 확인.','SB31':'원래 남성 A01의 얼굴과 차콜 상의. 여성의 침실 중앙 의자에 남성만 앉아 있고 렌즈 눈맞춤과 입꼬리 올라간 음흉한 미소 확인. 여성 잔상 없음.'}
for key,note in notes.items():
 qa[key]={'status':'visually_checked','method':'built-in image_gen 반환 이미지 직접 확인','revision':'v2','note':note,'limits':'정지 이미지의 인물·수량·표정·의상·방 배치만 확인. 3초 유지·놀라는 동작·순간 교체·웃음 변화·음향은 실제 영상 생성 후 검수 필요.'}
(root/'production/visual_qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
records=json.loads((root/'production/final_generation_records.json').read_text(encoding='utf-8'))
records=[r for r in records if r['id'] not in notes]
records+=json.loads((root/'production/ending_v2_generation_records.json').read_text(encoding='utf-8'))
(root/'production/final_generation_records.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Updated ending source, metadata and visual review records.')
