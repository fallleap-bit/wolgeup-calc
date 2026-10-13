from PIL import Image, ImageFilter, ImageDraw, ImageChops
import numpy as np, os
cart=Image.open('images/3.webp').convert('RGB'); photo=Image.open('images/4.webp').convert('RGB')
W,H=cart.size
ch=np.array(cart.convert('HSV')).astype(int); ph=np.array(photo.convert('HSV')).astype(int)
sat=((ch[...,1]>55)&(ch[...,2]>25))
def img(a): return Image.fromarray((a>0).astype('uint8')*255)
def close(m,r): return m.filter(ImageFilter.MaxFilter(r)).filter(ImageFilter.MinFilter(r))
def fill_holes(m):
    inv=ImageChops.invert(m).convert('L'); w,h=inv.size
    pad=Image.new('L',(w+2,h+2),255); pad.paste(inv,(1,1))
    ImageDraw.floodfill(pad,(0,0),128)
    a=np.array(pad)[1:-1,1:-1]
    return img(a!=128)
def poly(pts):
    m=Image.new('L',(W,H),0); ImageDraw.Draw(m).polygon(pts,fill=255); return m
def crop_to(m,box):
    z=Image.new('L',(W,H),0); z.paste(m.crop(box),box[:2]); return z
def biggest(m):
    # keep pixels of components larger than ~ small specks: approximate via open
    return m.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))
S=img(sat)
masks={}
# 텐트
t=crop_to(S,(95,285,1000,845)); t=fill_holes(close(biggest(t),15))
tp=poly([(105,712),(150,600),(235,470),(330,380),(460,322),(530,298),(612,305),(690,338),(745,390),(805,455),(880,545),(940,640),(990,738),(985,752),(900,770),(670,826),(648,836),(470,800),(300,770),(108,728)])
masks['tent']=ImageChops.lighter(t,tp)
# 아이스박스 (흰 뚜껑 포함 → 손 다각형 ∪ 채도)
c=poly([(78,826),(110,806),(430,806),(452,826),(448,1005),(420,1040),(180,1064),(98,1048),(86,960)])
masks['cooler']=c
# 화로대
f=crop_to(S,(860,800,1210,1052)); f=fill_holes(close(biggest(f),11)); masks['fire-pit']=f
# 랜턴 (번짐 제외 → 몸통 다각형)
masks['lantern']=poly([(1580,262),(1638,262),(1644,300),(1650,330),(1647,440),(1566,440),(1561,330),(1572,300)])
# 의자: 천(채도) + 프레임(실사에서 흙/풀 색이 아닌 부분)
cp=poly([(1572,738),(1745,705),(1755,612),(1935,620),(1924,760),(1940,775),(1925,1075),(1600,1075),(1612,900),(1650,890),(1655,770),(1572,760)])
hue,s,v=ph[...,0],ph[...,1],ph[...,2]
ground=((hue>=8)&(hue<=45)&(s>45)) | ((hue>45)&(hue<=110)&(s>50))   # 흙(갈색) / 풀(초록)
frame=img(~ground & (v>40))
fab=close(crop_to(S,(1565,600,1950,1080)),9)
chair=ImageChops.multiply(ImageChops.lighter(frame,fab),cp)
chair=biggest(chair)
masks['camping-chair']=chair
os.makedirs('gen/c/masks',exist_ok=True)
allm=Image.new('L',(W,H),0)
for k,m in masks.items():
    m.save(f'gen/c/masks/{k}.png'); allm=ImageChops.lighter(allm,m)
allm.save('gen/c/mask_all.png')
red=Image.new('RGB',(W,H),(230,30,30))
Image.composite(Image.blend(cart,red,0.5),cart,allm).save('gen/c/check.png')
