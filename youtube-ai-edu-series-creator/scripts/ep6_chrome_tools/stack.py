import sys
from PIL import Image
# stack.py OUT NAME... -> vertical stack of build/qc_NAME.png, scaled to 1600 wide
ims=[Image.open(f'build/qc_{n}.png') for n in sys.argv[2:]]
c=Image.new('RGB',(ims[0].width,sum(i.height for i in ims)),'white'); y=0
for i in ims: c.paste(i,(0,y)); y+=i.height
c.thumbnail((1600,4000)); c.save(sys.argv[1])
