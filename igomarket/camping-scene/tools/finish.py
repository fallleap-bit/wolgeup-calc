from PIL import Image, ImageFilter, ImageChops
import numpy as np
cart=Image.open('images/3.webp').convert('RGB'); photo=Image.open('images/4.webp').convert('RGB')
W,H=cart.size
ph=np.array(photo.convert('HSV')).astype(int); hue,s,v=ph[...,0],ph[...,1],ph[...,2]
yy=np.arange(H)[:,None]*np.ones((1,W),int)
dirt=(hue>=5)&(hue<=38)&(s>50)
green=(hue>38)&(hue<=110)&(s>45)
def L(k): return np.array(Image.open(f'gen/c/masks/{k}.png'))>0
def clean(a,r=5): return np.array(Image.fromarray(a.astype('uint8')*255).filter(ImageFilter.MinFilter(r)).filter(ImageFilter.MaxFilter(r)))>0
m={}
m['cooler']=clean(L('cooler')&~(dirt|green))
from PIL import ImageDraw
lan=((s>100)&(hue<=32))|(v>215)
lan=lan&L('lantern')
li=Image.fromarray(lan.astype('uint8')*255).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MinFilter(9))
inv=ImageChops.invert(li); pad=Image.new('L',(W+2,H+2),255); pad.paste(inv,(1,1)); ImageDraw.floodfill(pad,(0,0),128)
fl=(np.array(pad)[1:-1,1:-1]!=128)&L('lantern')
fl=np.where(yy<300, lan, fl)
m['lantern']=fl&~green&(v>35)
t=L('tent'); m['tent']=t&~(dirt&(yy>770))
m['fire-pit']=L('fire-pit'); m['camping-chair']=L('camping-chair')
allm=np.zeros((H,W),bool)
for k,a in m.items():
    Image.fromarray(a.astype('uint8')*255).save(f'gen/c/masks/{k}.png'); allm|=a
M=Image.fromarray(allm.astype('uint8')*255); M.save('gen/c/mask_all.png')
soft=M.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.6))
cart=cart.convert('L').convert('RGB')
fin=Image.composite(photo,cart,soft); fin.save('gen/c/final.png')
# 확대 검수
w=Image.new('RGB',(1200,600))
w.paste(fin.crop((60,760,460,1100)).resize((400,340)),(0,0))
w.paste(fin.crop((560,700,1010,860)).resize((450,160)),(400,0))
w.paste(fin.crop((1530,230,1700,460)).resize((340,460)),(860,0))
w.paste(fin.crop((1560,600,1960,1090)).resize((330,404)),(400,180))
w.save('gen/c/zoom.png')
