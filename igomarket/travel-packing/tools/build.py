from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np, os
cart=Image.open('source/step2-cartoon.webp').convert('RGB'); photo=Image.open('source/step1-photo.webp').convert('RGB')
W,H=photo.size
ph=np.array(photo.convert('HSV')).astype(int); hue,s,v=ph[...,0],ph[...,1],ph[...,2]
wood=(hue>=12)&(hue<=32)&(s>55)&(v>60)
def poly(pts):
    m=Image.new('L',(W,H),0); ImageDraw.Draw(m).polygon(pts,fill=255); return np.array(m)>0
P={
 'suitcase':[(495,612),(522,586),(700,562),(880,546),(925,552),(1000,590),(1060,600),(1150,612),(1178,640),(1180,700),(1165,790),(1130,830),(1010,868),(940,860),(720,820),(690,800),(676,700),(640,712),(560,705),(505,680),(495,640)],
 'packing-cube':[(283,722),(300,700),(460,668),(600,692),(645,722),(648,860),(615,880),(440,893),(300,845),(285,820)],
 'toiletry-pouch':[(560,890),(610,848),(700,840),(760,848),(840,860),(856,880),(820,930),(785,1000),(770,1022),(720,1016),(580,990),(500,966),(488,940)],
 'mesh-pouch':[(895,915),(930,885),(990,858),(1050,860),(1100,880),(1110,960),(1050,990),(1000,996),(930,980),(900,960)],
 'travel-adapter':[(1095,960),(1110,930),(1125,918),(1180,910),(1225,916),(1232,945),(1268,985),(1258,1032),(1200,1042),(1130,1042),(1095,1012)],
 'umbrella':[(1232,868),(1258,840),(1300,843),(1342,878),(1400,918),(1452,958),(1458,1000),(1440,1020),(1448,1032),(1400,1042),(1352,1033),(1356,1008),(1395,1008),(1280,942),(1238,902)],
 'hair-straightener':[(1433,842),(1448,812),(1475,804),(1600,866),(1632,888),(1628,918),(1598,918),(1440,862)],
}
hands=poly([(878,600),(905,585),(940,575),(965,580),(975,600),(960,625),(930,640),(900,640),(880,625)])|poly([(1048,640),(1080,610),(1120,603),(1152,620),(1158,660),(1132,692),(1095,692),(1058,674)])|poly([(922,528),(1002,528),(1004,588),(962,582),(928,562)])
woodsafe={'suitcase':False,'mesh-pouch':False}
ch=np.array(cart.convert('HSV')).astype(int)
csat=Image.fromarray((((ch[...,1]>45)&(ch[...,2]>25))*255).astype('uint8')).filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.MinFilter(7))
inv=ImageChops.invert(csat); pad=Image.new('L',(W+2,H+2),255); pad.paste(inv,(1,1)); ImageDraw.floodfill(pad,(0,0),128)
cfill=np.array(pad)[1:-1,1:-1]!=128
masks={}
for k,pts in P.items():
    m=poly(pts)
    if k=='suitcase': m&=~hands
    if k in ('suitcase','mesh-pouch'): m&=cfill
    if woodsafe.get(k,True): m&=~wood
    mi=Image.fromarray(m.astype('uint8')*255).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))
    if k in ('suitcase','mesh-pouch'):
        mi=mi.filter(ImageFilter.MinFilter(11)).filter(ImageFilter.MaxFilter(11))
    masks[k]=np.array(mi)>0
os.makedirs('out/masks',exist_ok=True)
allm=np.zeros((H,W),bool)
for k,m in masks.items():
    Image.fromarray(m.astype('uint8')*255).save(f'out/masks/{k}.png'); allm|=m
M=Image.fromarray(allm.astype('uint8')*255); M.save('out/mask_all.png')
bg=cart.convert('L').convert('RGB')
soft=M.filter(ImageFilter.GaussianBlur(1.4))
fin=Image.composite(photo,bg,soft); fin.save('out/final.png')
red=Image.new('RGB',(W,H),(230,30,30))
Image.composite(Image.blend(bg,red,0.5),bg,M).save('out/check.png')
z=Image.new('RGB',(1400,700))
z.paste(fin.crop((270,520,1200,900)),(0,0))
z.paste(fin.crop((480,830,1660,1060)).resize((944,184)),(0,400))
z.paste(fin.crop((1200,780,1660,1060)),(940,0))
z.save('out/zoom.png')
