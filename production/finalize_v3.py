import json,hashlib,zipfile,re
from pathlib import Path
from PIL import Image

root=Path(__file__).resolve().parent.parent
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads((root/p).read_text(encoding='utf-8'))
w=read('workflow.json'); old=read('production/history/revision_v2/workflow.json')
check=read('production/revision_v3_check.json')
assert check['ok'] and w['revision']=='v3'
assert len(w['clips'])==len(w['boards'])==32
assert w['project']['duration']==194 and w['clips'][27]['start']==170
assert len(list((root/'prompts').glob('C*.txt')))==32
assert len(list((root/'storyboard').glob('SB*.png')))==32
assert len({b['sha256'] for b in w['boards']})==32
sizes={}
for a in w['assets']:assert digest(root/a['path'])==a['sha256']
for b in w['boards']:
 assert digest(root/b['path'])==b['sha256']
 for item in b['inputs']:assert digest(root/item['path'])==item['sha256']
 with Image.open(root/b['path']) as im:im.verify()
 with Image.open(root/b['path']) as im:sizes[b['id']]=list(im.size)
 assert b['qa']['revision']=='v3' and b['qa']['status']=='visually_checked'
for c in w['clips']:
 txt=(root/c['prompt']['path']).read_text(encoding='utf-8')
 assert digest(root/c['prompt']['path'])==c['prompt']['sha256']
 assert txt==(root/'clips'/c['id']/(c['id']+'.txt')).read_text(encoding='utf-8')
 assert not re.search(r'\b16:9\b|@Audio|@Video|\d+\s*[-~]\s*\d+\s*초',txt)
 for a in c['attachments']:
  asset=next(x for x in w['assets'] if x['id']==a['asset_id'])
  assert digest(root/a['path'])==asset['sha256']
changed=[]
for c in w['clips']:
 prev=next((o for o in old['clips'] if o['id']==c['id']),None)
 changed.append({'clip_id':c['id'],'old_prompt_sha256':prev['prompt']['sha256'] if prev else None,'new_prompt_sha256':c['prompt']['sha256']})
report={'ok':True,'version':'v3','independent_photo_boards':32,'prompts':32,'omni_assets':4,'attachment_copies':64,'duration':194,'reveal_at':170,'source_dialogue_verified':True,'thanks_only_in':'C031','male_exit_clip':'C032','image_sizes':sizes,'regenerated_or_added_boards':check['changed_images'],'reused_boards_after_script_comparison':28,'generated_videos':0,'changes':changed,'limitations':'정지 이미지와 문서·태그·해시를 확인함. 실제 발화·립싱크·교체·퇴장 동작은 영상 생성 후 검수.'}
(root/'production/final_check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
zip_path=root.parent/'trapped_soul_seedance_package_20261015_v3.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(root.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(root).as_posix())
with zipfile.ZipFile(zip_path) as z:
 assert z.testzip() is None
 assert sum(n.startswith('storyboard/SB') and n.endswith('.png') for n in z.namelist())==32
 assert sum(n.startswith('prompts/C') and n.endswith('.txt') for n in z.namelist())==32
 assert 'REVISION_V3.txt' in z.namelist()
print(json.dumps({'ok':True,'zip':str(zip_path),'zip_mb':round(zip_path.stat().st_size/1024**2,1),'zip_sha256':digest(zip_path),'boards':32,'prompts':32,'duration':194,'videos':0},ensure_ascii=False))
