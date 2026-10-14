from pathlib import Path
import json
root=Path(__file__).resolve().parent.parent
p=root/'production/build.js'
s=p.read_text(encoding='utf-8')
def sub(old,new):
 global s
 assert old in s,old[:160]
 s=s.replace(old,new)
sub('production/history/ending_v1/workflow.json','production/history/revision_v2/workflow.json')
sub('sound,boardDescription]=r','sound,boardDescription,promptEvent=event]=r')
sub('주요 행동: ${event}','주요 행동: ${promptEvent}')
sub('이 이미지의 빈 의자는 공간 참조이며 해당 클립 인물이 의자에 앉는다.','빈 의자는 공간 참조이며, 인물의 착석과 이동은 각 클립의 행동을 따른다.')
sub("'@Image2의 침실에 앉은 @Image1의 기존 남성 한 명'", "i===30?'@Image2의 침실에 앉은 @Image1의 기존 남성 한 명':'@Image2의 침실에서 나가는 @Image1의 기존 남성 한 명'")
sub("'앞서 갇힌 방에 있던 @Image1의 동일한 남성 한 명이 @Image2의 침실 중앙 검은 사무용 의자에 앉는다. 웹캠은 모니터 위에서 남성을 향한다. 침대는 화면 왼쪽, 열린 문은 오른쪽이다.'", "'@Image1의 동일한 남성 한 명이 @Image2의 침실 중앙 검은 사무용 의자에서 장면을 시작한다. 모니터 위 웹캠은 방을 향한다. 침대는 화면 왼쪽이고, 의자 오른쪽의 빈 통로는 오른쪽 뒤편 열린 흰 문과 복도로 이어진다.'")
sub("let s0=speech?0.6:null,s1=speech?duration-1:null;", "let s0=speech?0.2:null,s1=speech?duration-0.3:null;")
sub("if(i===0){s0=.2;s1=3.3;}if(i===24){s0=1;s1=4;}if(i===25){s0=1;s1=3.5;}if(i===27){s0=.7;s1=7.5;}","if(i===0){s0=.15;s1=3.9;}if(i===24){s0=.6;s1=5.8;}if(i===25){s0=.8;s1=2.7;}if(i===27){s0=.6;s1=7.7;}if(i===30){s0=1.2;s1=2.2;}")
old=next(line for line in s.splitlines() if line.startswith(' if(i===30)timeline='))
sub(old,""" if(i===30)timeline=[{start:0,end:1.2,action:'여성의 마지막 놀란 프레임에서 같은 자리의 남성 첫 프레임으로 즉시 컷 전환한다. 남성이 렌즈를 보며 한쪽 입꼬리부터 씨익 올린다.',camera,speech:'무대사',sound:'여성의 들숨은 끊기고 침실 팬 소리는 이어진다.'},{start:1.2,end:2.2,action:'작은 미소와 렌즈 눈맞춤을 유지하며 고마워라고 말한다. 입과 턱이 발화에 맞게 움직인다.',camera,speech:'기존 남성 / 한국어 / 낮고 편안하게: 고마워.',sound:'남성의 가까운 한마디와 침실 팬 소리.'},{start:2.2,end:4,action:endState,camera,speech:'무대사; 추가 발화 없음.',sound:'옷감과 팔걸이의 작은 마찰, 침실 팬 소리.'}];
 if(i===31)timeline=[{start:0,end:1.3,action:'양손으로 팔걸이를 짚고 체중을 발로 옮겨 일어난다. 의자는 뒤로 조금 밀린 뒤 남는다.',camera,speech:delivery,sound:'의자의 짧은 삐걱임, 옷감 마찰.'},{start:1.3,end:5,action:'몸을 화면 오른쪽으로 돌려 의자 옆을 빠져나와 오른쪽 뒤편 열린 문까지 걷는다. 문턱을 넘고 복도 안쪽으로 걸어 시야에서 완전히 사라진다.',camera,speech:delivery,sound:'카펫의 둔한 발소리가 복도 바닥 발소리로 바뀌며 멀어진다. 침실 팬 소리는 일정하다.'},{start:5,end:6,action:endState+' 빈 방을 유지하다 영상과 소리를 끝낸다.',camera,speech:'무대사; 사람 없음.',sound:'침실 팬 소리만 남고 끝에서 끊긴다.'}];""")
sub('무표정한 얼굴에서 입꼬리 양쪽이 한 번에 올라가 작은 미소가 생긴다. 두 손은 그대로 멈춰 있다.','무표정한 얼굴에서 입꼬리가 매끄럽게 올라가 작은 미소가 생긴다. 깍지 낀 손은 그대로 멈춰 있다.')
sub('같은 침실·카메라 축·화각·의자 중심을 맞춘다. 마지막 1.5초는 웃는 얼굴을 유지하고 종료한다.','같은 침실·카메라 축·화각·의자 중심을 맞춘다. 고마워 한마디 후 양손을 팔걸이에 얹고 앞으로 기울인 자세로 끝내어 C032 퇴장과 연결한다.')
sub("json(`clips/${id}/SETTINGS.json`,settings);\n const localBoardTime", "if(i===31)settings.notes.push('C031 종료 자세에서 이어 일어나 의자 오른쪽을 지나 열린 문으로 나간다. 마지막 1초는 빈 방이다. 카메라를 따라 움직이지 않는다.');\n json(`clips/${id}/SETTINGS.json`,settings);\n const localBoardTime")
sub('i===30?3.2:i===27?7.8','i===30?.95:i===31?4:i===27?7.8')
sub("(i===0||i===27?'user_verbatim':'authored_with_user_permission')","(i===30?'user_requested_final_line':'user_supplied_revision_v3')")
start=s.index('const endingRecords=')
end=s.index("json('production/board_plan.json',boardPlan);",start)
s=s[:start]+"""const allRecords=JSON.parse(fs.readFileSync(path.join(root,'production/final_generation_records.json'),'utf8'));
for(const b of boardPlan){const r=allRecords.find(r=>r.id===b.id);if(r){b.prompt=r.prompt;b.references=[...new Set([...b.references,...(r.refs||[])])];b.generation_references=r.refs||b.references;}}
"""+s[end:]
old=next(line for line in s.splitlines() if line.startswith('for(const b of boards)'))
sub(old,"for(const b of boards){b.review_status='awaiting_user_review';}")
sub("revision:'v2'","revision:'v3'")
sub("authoring_permission:'사용자가 중간 대사도 새로 써서 완성을 선택함'","authoring_permission:'사용자가 첨부한 수정안 전체 채택 및 마지막 고마워 발화와 퇴장 요청',source_revision:{path:'sources/user_revision_v3.txt',sha256:hash('sources/user_revision_v3.txt')}")
sub("accepted_boards:(priorWorkflow.review.accepted_boards||[]).filter(b=>!['SB29','SB30','SB31'].includes(typeof b==='string'?b:b.id))", "accepted_boards:[]")
old="{reason:'사용자 요청: 여성 시청자 3초, 놀라는 반응, 같은 자리의 기존 남성으로 즉시 교체, 웹캠을 보며 씨익 웃고 종료.',affected_clips:['C029','C030','C031'],affected_assets:['A02'],affected_boards:['SB29','SB30','SB31'],previous_version:'v1',version:'v2',review_status:'awaiting_user_review',open_issues:[]}"
new="{reason:'사용자 첨부 수정안의 전체 구어체 대사·행동·음향 반영. C028의 고마워를 C031 최종 인사로 이동. C032 남성의 퇴장 6초 추가.',affected_clips:clips.map(c=>c.id),affected_assets:[],affected_boards:boards.map(b=>b.id),regenerated_boards:['SB04','SB25','SB27','SB32'],previous_version:'v2',version:'v3',review_status:'awaiting_user_review',open_issues:['실제 발화 길이와 퇴장 동작은 영상 생성 후 검수.']}"
sub(old,new)
sub('인물 수·원문 두 대사·170초 반전·현재 사건의 상태·태그 역할·파라미터 분리·음성 실제 미검수 상태 점검','첨부 수정안 대사 대조·고마워 C031 한 번·170초 반전·194초 종료·의자에서 오른쪽 열린 문까지 퇴장·태그와 현재 사건 상태·파라미터 분리 점검')
sub('미사용: 고정 웹캠과 단순 손 연기','미사용: 고정 웹캠, 단순 손 연기와 열린 문까지 단일 보행')
sub('제작 패키지 v2','제작 패키지 v3')
sub('C031은 Image1.png=기존 남성(A01), Image2.png=침실(B02)입니다.','C031–C032는 Image1.png=기존 남성(A01), Image2.png=침실(B02)입니다.')
sub('C031은 남성이 렌즈를 보며 씨익 웃고 03:08에 종료합니다.','C031은 남성이 렌즈를 보며 씨익 웃고 고마워라고 한 번 말한 뒤 팔걸이를 짚습니다. C032는 03:08–03:14이며, 남성이 일어나 오른쪽 열린 문으로 나가고 마지막 1초 빈 방을 남겨 종료합니다.')
sub('VERSION 02','VERSION 03')
sub('첫 두 핵심 대사는 원문을 유지했고, 중간 대사는 사용자 요청에 따라 새로 작성했습니다.','첨부한 수정안의 대사·지문을 반영했습니다. “고마워”는 마지막 인사로 옮기고 남성의 퇴장을 추가했습니다.')
sub('여성 시청자 3초 → 놀라는 반응 2초 → 같은 자리에 남성 등장 → 웹캠을 보며 씨익 웃고 종료.','여성 시청자 3초 → 놀라는 반응 2초 → 같은 자리에 남성 등장 → 웃으며 “고마워” → 오른쪽 문으로 퇴장 → 빈 방에서 종료.')
p.write_text(s,encoding='utf-8')

prior=json.loads((root/'production/history/revision_v2/production/final_generation_records.json').read_text(encoding='utf-8'))
new=json.loads((root/'production/revision_v3_generation_records.json').read_text(encoding='utf-8'))
ids={x['id'] for x in new}
merged=[x for x in prior if x['id'] not in ids]+new
merged.sort(key=lambda r:r['id'])
(root/'production/final_generation_records.json').write_text(json.dumps(merged,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
qa=json.loads((root/'production/history/revision_v2/production/visual_qa.json').read_text(encoding='utf-8'))
for k,v in qa.items():
 v['revision']='v3'
 v['revision_comparison']='새 지문과 정지 장면의 인물·공간·동작 순간 대응을 대조. 대사 교체·호흡·움직임의 속도는 정지 이미지로 검증할 수 없음.'
 v['review_status']='awaiting_user_review'
notes={'SB04':'왼손으로 가슴팍 옷감을 움켜쥔 형태와 옷 주름, 오른손의 책상 접촉 확인.','SB25':'책상 중앙에서 두 손의 손가락이 깍지 낀 형태 확인. 미소 없이 렌즈를 향하는 얼굴.','SB27':'같은 깍지 손을 유지한 무표정과 정지 자세. 미소가 나타나기 전 상태 확인.','SB32':'중앙 의자가 비었고 기존 남성 한 명의 뒷모습이 화면 오른쪽 열린 문을 통해 복도로 걸어 나감. 왼쪽 침대와 방 배치 유지.'}
for key,note in notes.items():
 qa[key]={'status':'visually_checked','method':'built-in image_gen 반환 이미지 직접 확인','revision':'v3','review_status':'awaiting_user_review','note':note,'limits':'정지 장면만 확인. 실제 발화·립싱크·퇴장 동작·6초 길이·마지막 빈 방은 영상 생성 후 검수.'}
qa['SB31']['note']='동일한 기존 남성이 여성의 침실 의자에서 렌즈를 보며 웃음. 이 정지 이미지는 고마워 발화 직전 순간으로 재배치함.'
(root/'production/visual_qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('V3 build, generation provenance and revised visual comparison updated.')
