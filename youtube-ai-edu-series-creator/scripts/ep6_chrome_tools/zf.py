import subprocess,sys,io
from PIL import Image
# zf.py NAME a b crop [n] -> n frames, 3 per row, 640 wide -> build/look.png
n,a,b,c=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),sys.argv[4]; N=int(sys.argv[5]) if len(sys.argv)>5 else 9
w,h=map(int,c.split(':')[:2]); H=int(640*h/w); o=Image.new('RGB',(1920,H*((N+2)//3)))
for k in range(N):
    t=a+(b-a)*k/(N-1)
    p=subprocess.run(['ffmpeg','-v','error','-ss',f'{t:.2f}','-i',f'clips/{n}.mp4','-frames:v','1','-vf','crop='+c,'-f','image2pipe','-vcodec','png','-'],capture_output=True).stdout
    if p: o.paste(Image.open(io.BytesIO(p)).convert('RGB').resize((640,H)),((k%3)*640,(k//3)*H))
o.save('build/look.png')
