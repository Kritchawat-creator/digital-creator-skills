import subprocess,sys,io
from PIL import Image
# sheet.py OUT NAME:a:b ...  -> 8 frames per row (320x180) between a and b
out=sys.argv[1]; rows=[]
for it in sys.argv[2:]:
    n,a,b=it.split(':'); a=float(a); b=float(b); row=Image.new('RGB',(8*240,135))
    for k in range(8):
        t=a+(b-a)*k/7
        p=subprocess.run(['ffmpeg','-v','error','-ss',f'{t:.2f}','-i',f'clips/{n}.mp4','-frames:v','1','-f','image2pipe','-vcodec','png','-'],capture_output=True).stdout
        if p: row.paste(Image.open(io.BytesIO(p)).convert('RGB').resize((240,135)),(k*240,0))
    rows.append(row)
o=Image.new('RGB',(1920,135*len(rows)))
for i,r in enumerate(rows): o.paste(r,(0,i*135))
o.save(out)
