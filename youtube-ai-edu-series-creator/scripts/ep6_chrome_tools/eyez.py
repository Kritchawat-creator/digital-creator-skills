import subprocess,sys
from PIL import Image
# eyez.py NAME:a:b:crop ... -> build/look.png (8 frames per row)
ims=[]
for it in sys.argv[1:]:
    n,a,b,c=it.split(':',3); a=float(a); b=float(b); r=[]
    w,h=map(int,c.split(':')[:2]); H=int(200*h/w)
    for k in range(8):
        t=a+(b-a)*k/7
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',f'clips/{n}.mp4','-frames:v','1','-vf','crop='+c,'build/e.png'])
        r.append(Image.open('build/e.png').convert('RGB').resize((200,H)))
    row=Image.new('RGB',(1600,H)); [row.paste(x,(i*200,0)) for i,x in enumerate(r)]; ims.append(row)
o=Image.new('RGB',(1600,sum(i.height for i in ims))); y=0
for i in ims: o.paste(i,(0,y)); y+=i.height
o.save('build/look.png')
