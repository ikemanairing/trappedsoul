const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const rows=require('./history/revision_v2/production/story.js');
const input=fs.readFileSync(path.join(root,'sources/user_revision_v3.txt'),'utf8');
const blocks=[...input.matchAll(/\[(\d\d:\d\d)–(\d\d:\d\d)\]\s+(C\d{3})\s+([^\r\n]+)\r?\n([\s\S]*?)(?=\[\d\d:\d\d–|💡 수정 포인트|$)/g)];
if(blocks.length!==31)throw new Error('Expected 31 source clips, got '+blocks.length);
const norm=s=>s.replace(/\s+/g,' ').trim();
const source=[];
for(const [i,m] of blocks.entries()){
 const body=m[5],event=norm(body.match(/- 화면:\s*([\s\S]*?)\s*- 인물:/)[1]);
 const line=norm(body.match(/- 인물:\s*([\s\S]*?)\s*- 음향:/)[1]);
 const speech=line==='(무대사)'?'':line.match(/^“([\s\S]*)”$/)[1];
 const sound=norm(body.match(/- 음향:\s*([\s\S]*)/)[1]);
 rows[i][1]=m[4].replace(' (반전)','');rows[i][3]=event;rows[i][5]=speech;rows[i][8]=sound;
 source.push({id:m[3],start:m[1],end:m[2],event,speech,sound});
}
rows[27][5]=rows[27][5].replace(/ 고마워\.$/,'');
rows[3][4]='왼손으로 가슴팍의 옷감을 움켜쥔 채 렌즈를 바라본다. 말이 끝나면 입술만 가볍게 닫고 손은 그대로 둔다.';
rows[4][2]='왼손으로 가슴팍의 옷감을 움켜쥐고 있다.';
rows[5][7]='같은 웹캠 축에서 양손에 집중한 인서트. 왼손바닥과 소매가 또렷하고, 얼굴은 화면 위쪽에 일부만 걸친다.';
rows[5][4]='왼손바닥이 위를 향하고 손가락이 조금 벌어진 상태로 멈춘다. 오른손은 책상 위에 있다.';
rows[6][2]=rows[5][4];
rows[6][4]='고개는 화면 오른쪽 닫힌 문을 향하고 입은 다문 채 긴장해서 듣고 있다.';
rows[9][4]='오른손바닥과 손끝이 유리 표면에 눌린 채 멈춘다. 발화가 끝난 뒤 입을 다물고 렌즈를 바라본다.';
rows[10][4]='오른손을 유리에서 떼어 뺨 옆을 지나 아래로 내리고, 렌즈를 바라보며 거칠게 숨을 내쉰다.';
rows[11][2]=rows[10][4];
rows[13][4]='고개를 세우고 긴 날숨을 마친다. 어깨는 내려가지만 입꼬리는 올라가지 않는다.';
rows[14][4]='왼손으로 관자놀이를 누른 채 미간을 찌푸리고 렌즈를 바라본다.';
rows[15][2]=rows[14][4];
rows[23][4]='눈 밑을 훔친 왼손이 책상으로 돌아온다. 발화를 마친 뒤 입을 가볍게 다문다.';
rows[24][2]='왼손이 책상에 돌아와 있고 눈은 렌즈를 향한다.';
rows[24][3]=rows[24][3].replace('깍지 낀 손가락의','두 손을 모아 느슨하게 깍지를 낀다. 깍지 낀 손가락의');
rows[24][4]='깍지 낀 두 손이 책상 중앙에 놓이고 손끝의 떨림이 거의 멈춘다. 시선은 다시 렌즈로 돌아온다.';
rows[25][2]=rows[24][4];
rows[25][4]='깍지 낀 손과 내려간 어깨는 멈춰 있다. 입꼬리는 올리지 않고 렌즈를 응시한다.';
rows[26][2]=rows[25][4];
rows[26][4]='깍지 낀 손끝까지 완전히 멈추고, 입은 다문 무표정으로 렌즈를 바라본다.';
rows[26][6]='무대사; 호흡 소리도 멎고 환풍기만 들린다.';
rows[27][2]=rows[26][4];
rows[27][6]='앞선 거친 호흡이 사라진 뒤, 낮고 안정된 일상적인 말투로 속삭이듯 또렷하게';
rows[27][4]='대사를 끝낸 뒤 입술을 닫고, 차갑게 눈을 맞추며 작은 미소를 유지한다.';
rows[28][4]='여성이 편안한 어깨와 닫힌 입을 유지하며 렌즈 아래의 모니터를 바라본다.';
rows[29][4]='여성은 눈을 크게 뜨고 입을 벌린 채 의자 등받이 쪽으로 몸을 뺀 상태다.';
rows[30][3]='여성이 사라진 같은 침실 의자에 기존 남성이 앉아 있다. 남자는 웹캠을 바라보며 어깨의 힘을 빼고, 한쪽 입꼬리부터 씨익 올려 만족스러운 미소를 짓는다. 낮고 편안하게 “고마워.”라고 말한다. 말을 마친 뒤 두 손을 의자 팔걸이에 얹고 몸을 조금 앞으로 기울인다.';
rows[30][4]='말을 끝낸 남성이 양손을 팔걸이에 얹은 채 상체를 조금 앞으로 기울인다. 입은 닫혀 있고 작은 미소가 남아 있다.';
rows[30][5]='고마워.';
rows[30][6]='낮고 편안한 목소리로, 웃음을 살짝 머금고 짧고 또렷하게';
rows[30][8]='침실 팬 소리, 남성의 낮고 편안한 한마디, 옷감과 팔걸이의 작은 마찰. 발화 뒤 방의 소리는 계속된다.';
rows.push([6,'자유롭게 나가는 남자',rows[30][4],
 '남성이 팔걸이를 짚고 의자에서 일어난다. 몸을 화면 오른쪽으로 돌려 의자 옆의 빈 바닥으로 빠져나온 뒤, 오른쪽 뒤편의 열린 흰 문을 향해 느긋하게 걸어간다. 카메라는 그대로 남고, 남성은 문턱을 넘어 따뜻한 빛의 복도로 나가 시야에서 완전히 사라진다. 빈 의자와 열린 문만 잠깐 남은 뒤 영상이 끝난다.',
 '남성은 복도로 나가 화면에 보이지 않는다. 중앙의 빈 검은 의자와 오른쪽 열린 흰 문은 그대로이고, 침실 팬 소리만 남아 있다.',
 '', '무대사; 인물의 추가 발화나 웃음소리는 없다.',
 '직전과 같은 모니터 위 고정 웹캠. 팬·틸트·줌 없이 중앙 의자, 의자 오른쪽 통로, 뒤편 열린 문을 계속 보여 준다. 남성이 카메라에서 멀어지면 전신이 화면 안에 들어오고 문턱을 넘는 뒷모습이 보인다.',
 '팔걸이와 의자의 짧은 삐걱임, 옷감 마찰, 카펫 위 둔한 발소리에서 복도의 단단한 바닥 발소리로 바뀐다. 발소리는 멀어지고 마지막에는 침실 팬 소리만 남는다.',
 'The original man in his charcoal long sleeve shirt and dark trousers seen from behind, crossing the open white doorway on screen right into the warm amber hallway. His natural walking stride is visible at the threshold. The black mesh office chair is now empty in the foreground center. Exact same bedroom, bed on screen left, identical fixed webcam view. One man only, moving away from the camera; no woman and no ghost.']);
rows[3][9]='Same original male seated in trapped concrete room, LEFT fingers tightly grasp a handful of his own charcoal shirt at upper chest on screen right, gathered fabric visible. Right hand stays on desk. Near tears, raised inner brows, lips parted during speech. No smile.';
rows[24][9]='Same original male with both hands loosely interlaced at desk center, fingers clearly woven together, looking up at webcam after a brief glance down. Lips slightly parted, fear fading but still no smile.';
rows[26][9]='Same original male fully still and blank-faced, unsmiling, two hands loosely interlaced together at desk center. Face muscles relaxed, eyes fixed on webcam, no speech.';
const deliveries={0:'겁에 질려 숨이 터지듯 다급하게 절규하는 말투',1:'거친 숨 사이로 다그치듯 짧게',2:'급하게 몰아붙이는 빠른 말투',3:'울먹이며 짧은 숨을 사이에 두고',4:'믿기지 않는다는 듯 떨리는 목소리',5:'멍하니 자기 손을 보며 낮고 떨리는 목소리',7:'상체를 바짝 숙인 채 다급하게 애원하는 속삭임',8:'답답함에 말을 빠르게 이어 가며',9:'막힌 숨을 밀어내듯 거칠게',10:'힘이 빠진 채 절망적으로',11:'급히 붙잡듯 첫마디를 높이고 뒤를 낮추며',12:'초조하게 대답을 재촉하는 말투',13:'긴 날숨 뒤 안도하면서도 불안한 목소리',14:'말을 찾지 못해 머뭇거리는 혼란스러운 말투',15:'공포를 억누르며 떨리는 목소리',17:'체념과 원망을 섞어 빠르게 말을 이어 가며',18:'미안함과 외로움을 삼키는 낮은 목소리',19:'숨결이 가까이 들리는 아주 작은 속삭임',20:'혼잣말처럼 작게 달래는 말투',21:'스스로를 다그치다 다시 상대를 재촉하는 말투',22:'낮고 집요하게, 문장을 빠르게 잇는 말투',23:'미안하다는 듯 숨을 섞되 말은 이어서',24:'자기도 모르게 붙잡듯 작고 부드럽게',25:'차분해진 숨으로 작고 또렷하게'};
for(const [i,d] of Object.entries(deliveries))rows[+i][6]=d;
for(const r of rows){
 r[10]=r[3].replace(/\[시점 전환[^\]]*\]\s*/g,'').replace(/\(시간이 얼마 안 남았음을 체크하는 복선\)|\(약간의 기괴함이 스며듦\)|\(상황 파악 전\)/g,'').trim();
}
rows[30][10]='남성이 렌즈에 눈을 맞추고 어깨의 힘을 뺀다. 한쪽 입꼬리를 먼저 올리고 양쪽 입꼬리를 씨익 끌어올린 뒤 짧게 말한다. 발화를 마치면 양손을 의자 팔걸이에 얹고 몸을 조금 앞으로 기울인다.';
fs.writeFileSync(path.join(root,'production/story.js'),'module.exports = '+JSON.stringify(rows,null,2)+';\n','utf8');
fs.writeFileSync(path.join(root,'production/adopted_source_v3.json'),JSON.stringify(source,null,2)+'\n','utf8');
console.log(JSON.stringify({source_clips:source.length,total_clips:rows.length,duration:rows.reduce((a,r)=>a+r[0],0),thanks:rows.filter(r=>r[5].includes('고마워')).map((r)=>r[1])}));
