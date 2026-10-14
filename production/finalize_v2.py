import json, hashlib, zipfile, re
from pathlib import Path
from PIL import Image

root=Path(__file__).resolve().parent.parent
digest=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
workflow=json.loads((root/'workflow.json').read_text(encoding='utf-8'))
prior=json.loads((root/'production/history/ending_v1/workflow.json').read_text(encoding='utf-8'))
count=len(workflow['clips'])
assert count==len(workflow['boards'])==31
assert workflow['clips'][27]['start']==170 and workflow['project']['duration']==188
assert len(list((root/'prompts').glob('C*.txt')))==count
assert len(list((root/'storyboard').glob('SB*.png')))==count
assert len({b['sha256'] for b in workflow['boards']})==count
assert workflow['clips'][0]['speech']=='제발 누르지 말랬잖아!'
assert workflow['clips'][27]['speech']=='농담이야. 사실 끝까지 본 사람과 내 위치가 바뀌는 거거든.'
assert all(not c['speech'] for c in workflow['clips'][28:])
female=workflow['clips'][28]['timeline'][1]
assert female['end']-female['start']==3
assert workflow['clips'][29]['duration']==2
assert workflow['clips'][30]['duration']==4
assert [a['asset_id'] for a in workflow['clips'][28]['attachments']]==['B02','A02']
assert [a['asset_id'] for a in workflow['clips'][29]['attachments']]==['B02','A02']
assert [a['asset_id'] for a in workflow['clips'][30]['attachments']]==['A01','B02']
unchanged=[]
for old,new in zip(prior['clips'][:28],workflow['clips'][:28]):
 assert old==new, new['id']
 assert digest(root/new['prompt']['path'])==old['prompt']['sha256']
 unchanged.append(new['id'])
for old,new in zip(prior['boards'][:28],workflow['boards'][:28]):
 assert old==new, new['id']
 assert digest(root/new['path'])==old['sha256']
sizes={}
for b in workflow['boards']:
 with Image.open(root/b['path']) as im: im.verify()
 with Image.open(root/b['path']) as im: sizes[b['id']]=list(im.size)
 assert b['qa']['status']=='visually_checked'
for c in workflow['clips']:
 txt=(root/c['prompt']['path']).read_text(encoding='utf-8')
 assert txt==(root/'clips'/c['id']/(c['id']+'.txt')).read_text(encoding='utf-8')
 assert not re.search(r'\b16:9\b|@Audio|@Video|\d+\s*[-~]\s*\d+\s*초',txt)
 for a in c['attachments']:
  src=next(x for x in workflow['assets'] if x['id']==a['asset_id'])
  assert digest(root/a['path'])==src['sha256']
changes=[]
for i in range(28,count):
 c=workflow['clips'][i];b=workflow['boards'][i]
 changes.append({'clip_id':c['id'],'old_prompt_sha256':prior['clips'][i]['prompt']['sha256'] if i<len(prior['clips']) else None,'new_prompt_sha256':c['prompt']['sha256'],'board_id':b['id'],'old_board_sha256':prior['boards'][i]['sha256'] if i<len(prior['boards']) else None,'new_board_sha256':b['sha256']})
report={'ok':True,'version':'v2','independent_photo_boards':count,'unique_image_hashes':count,'prompts':count,'omni_assets':len(workflow['assets']),'attachment_copies':sum(len(c['attachments']) for c in workflow['clips']),'duration':188,'reveal_at':170,'exact_user_lines_preserved':True,'unchanged_clips':unchanged,'revised_ending':changes,'female_neutral_seconds':3,'female_startle_seconds':2,'male_reveal_grin_seconds':4,'generated_videos':0,'image_sizes':sizes,'visual_check':'개별 생성 이미지 직접 확인; visual_qa.json 참조','limitations':'실제 동작·교체·발화·음색 검수 미실행'}
(root/'production/final_check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
zip_path=root.parent/'trapped_soul_seedance_package_20261015_v2.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(root.rglob('*')):
  if p.is_file(): z.write(p,p.relative_to(root).as_posix())
with zipfile.ZipFile(zip_path) as z:
 assert z.testzip() is None
 assert sum(n.startswith('storyboard/SB') and n.endswith('.png') for n in z.namelist())==count
 assert sum(n.startswith('prompts/C') and n.endswith('.txt') for n in z.namelist())==count
print(json.dumps({'ok':True,'zip':str(zip_path),'zip_mb':round(zip_path.stat().st_size/1024**2,1),'zip_sha256':digest(zip_path),'boards':count,'prompts':count,'unchanged_clips':len(unchanged),'videos':0},ensure_ascii=False))
