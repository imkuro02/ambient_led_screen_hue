import mss
from PIL import Image, ImageDraw, ImageTk, ImageGrab
from color import *

sct = mss.mss()

def color_samples(samples,size):
        # flytt dette her inn i create sample cords
        # deretter gjør så sample cords for w og h values
        # da trenger vi ikke å kalkulere w og h på nytt hele tiden
        temp_samples = []
        for s in samples:
            x = int(s.x)
            y = int(s.y)#MONITOR_H-int(y)

            w = int(size)
            h = int(size)
            #print(x,y,w,h)

            pic = sct.grab({ 'left':x, 'top':y, 'width':w, 'height':h})
            pic = Image.frombytes("RGB", pic.size, pic.bgra, "raw", "BGRX")
            pic = pic.resize((1,1),resample=Image.CUBIC)
            #pic.save(f'testing/{x}-{y}.png')
            r,g,b = pic.convert('RGB').getpixel((0,0))

            color = rgb_to_hex((r,g,b))
            s.set_color(color)
            temp_samples.append(s)

        return temp_samples


