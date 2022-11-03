from screeninfo import get_monitors
import mss
from PIL import Image, ImageDraw, ImageTk, ImageGrab
import tkinter as tk
import threading
import multiprocessing
import os
import visualizer
import time
import numpy as np

SAMPLES_X, SAMPLES_Y = 11,11# amount of x and y leds
SAMPLE_RADIUS = 64
SAMPLE_CORNER = False
SAMPLE_CENTER = False
MONITOR_NAME = 'Virtual1' # monitor name

for m in get_monitors():
        if MONITOR_NAME == m.name:
            MONITOR_W,MONITOR_H = m.width,m.height

def get_monitor():
    for m in get_monitors():
        print(str(m))
        if MONITOR_NAME == m.name:
            return m

MONITOR = get_monitor()
MONITOR_W,MONITOR_H = MONITOR.width,MONITOR.height

def clamp(val, minval, maxval):
    if val <= minval:
       return minval
    if val >= maxval:
        return maxval
    return val

def hex_to_rgb(hex):
  rgb = []
  for i in (0, 2, 4):
    decimal = int(hex[i:i+2], 16)
    rgb.append(decimal)
  return tuple(rgb)

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

sct = mss.mss()

def get_pixel(x,y):
   
        # flytt dette her inn i create sample cords
        # deretter gjør så sample cords for w og h values
        # da trenger vi ikke å kalkulere w og h på nytt hele tiden
        x = int(x)
        y = MONITOR_H-int(y)

        x = MONITOR.x+clamp(x-int(SAMPLE_RADIUS/2),0,MONITOR_W-1)
        y = MONITOR.y+clamp(y-int(SAMPLE_RADIUS/2),0,MONITOR_H-1)

        w = int(SAMPLE_RADIUS)
        h = int(SAMPLE_RADIUS)

        if x-MONITOR.x + w >= MONITOR_W:
            w = MONITOR_W - x-MONITOR.x

        if y-MONITOR.y + h >= MONITOR_H:
            h = MONITOR_H - y-MONITOR.y

        pic = sct.grab({ 'left':x, 'top':y, 'width':w, 'height':h})
        pic = Image.frombytes("RGB", pic.size, pic.bgra, "raw", "BGRX")
        pic = pic.resize((1,1),resample=Image.CUBIC)
        #pic.save(f'testing/{x}-{y}.png')
        r,g,b = pic.convert('RGB').getpixel((0,0))

        return(rgb_to_hex((r,g,b)))

def create_sample_cords(monitor_w,
                        monitor_h,
                        sample_radius,
                        sample_corner,
                        samples_x,
                        samples_y):

    samples = []
    # * SAMPLE_CORNER means, if true, do this, and if not true then 0 so false 
    space_x = (monitor_w/(samples_x-int(sample_corner*1)))
    space_y = (monitor_h/(samples_y-int(sample_corner*1)))
    for ii in range(0,samples_y):
        for i in range(0,samples_x):
                sample = {
                'x':(space_x*i)+((space_x/2)*int(not sample_corner)),
                'y':(space_y*ii)+((space_y/2)*int(not sample_corner))}
                samples.append(sample)
    #visualize_samples(samples)
    return samples

def get_samples(samples):
    _samples = []
    for s in samples:
        color = get_pixel(s['x'],s['y'])
        s.update({'color':color})
        _samples.append(s)
    return _samples

def visualize(vis,samples):
    #vis.show()
    vis.update(samples)

def main():
    samples = create_sample_cords(MONITOR_W,MONITOR_H,SAMPLE_RADIUS,SAMPLE_CORNER,SAMPLES_X,SAMPLES_Y)
    temp_samples = []

    first_sample = samples[0]
    last_sample = samples[-1]
    x1, y1 = first_sample['x'], first_sample['y']  
    x2, y2 = last_sample['x'], last_sample['y']  

    if not SAMPLE_CENTER:
        for i, s in enumerate(samples):
            x,y = int(s['x']),int(s['y'])
            if (int(x) == int(x1) or int(x) == int(x2) or int(y) == int(y1) or int(y) == int(y2)):
                temp_samples.append(s)
            else:
                print('deleting:',s)
        samples = temp_samples
    #print(samples)

    vis = visualizer.Visualization()
    vis.setup(MONITOR_W,MONITOR_H,samples,SAMPLE_RADIUS)
    while True:
        start = time.time()
        samples = get_samples(samples)

        visualize(vis,samples)

        done = time.time()
        elapsed = done - start
        delay=0.033333-elapsed
        if delay >= 0 : time.sleep(delay)
        done = time.time()
        elapsed = done - start
    
        os.system('clear')
        print(elapsed)
        for s in samples:
            print(s)

       






if __name__ == '__main__':
    main()
    #space_samples(MONITOR_W,MONITOR_H,SAMPLE_RADIUS,SAMPLE_CORNER,SAMPLES_X,SAMPLES_Y)

    #gui = myGUI()
    #process = multiprocessing.Process(target=myGUI)
    #process.start()
