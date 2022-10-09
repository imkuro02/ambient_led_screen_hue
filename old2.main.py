from screeninfo import get_monitors
import mss
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
import threading
import os
import visualizer

SAMPLES_X, SAMPLES_Y = 6,8 # amount of x and y leds
SAMPLE_RADIUS = 64
SAMPLE_CORNER = True
MONITOR_NAME = 'DP-4' # monitor name

for m in get_monitors():
        if MONITOR_NAME == m.name:
            MONITOR_W,MONITOR_H = m.width,m.height

def get_monitor():
    for m in get_monitors():
        print(str(m))
        if MONITOR_NAME == m.name:
            MONITOR_W,MONITOR_H = m.width,m.height
            return m

MONITOR = get_monitor()

def hex_to_rgb(hex):
  rgb = []
  for i in (0, 2, 4):
    decimal = int(hex[i:i+2], 16)
    rgb.append(decimal)
  return tuple(rgb)

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb
    #return ('{:X}{:X}{:X}').format(r, g, b)

def get_pixel(x,y):
    with mss.mss() as sct:
        x = int(x)
        y = MONITOR_H-int(y)
        if x >= MONITOR_W: x = MONITOR_W - 1
        if x <= 1: x = 1
        if y >= MONITOR_H: y = MONITOR_H - 1
        if y <= 1: y = 1

        pic = sct.grab({'mon':MONITOR, 'left':MONITOR.x+x, 'top':MONITOR.y+y, 'width':1, 'height':1})
        #pic = sct.grab({'top':x, 'left':y, 'width':1, 'height':1})
        g = pic.pixel(0,0)
        #print(g)
        r,g,b = g
        #print(x,y,rgb_to_hex((r,g,b)))
        return(rgb_to_hex((r,g,b)))

def create_sample_cords(  
                    monitor_w,
                    monitor_h,
                    sample_radius,
                    sample_corner,
                    samples_x,
                    samples_y):

    samples = []
    # * SAMPLE_CORNER means, if true, do this, and if not true then 0 so false 
    space_x = round(monitor_w/(samples_x-int(sample_corner*1)))
    space_y = round(monitor_h/(samples_y-int(sample_corner*1)))
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
    threads = []

    thread_samples = {}

    def get_sample_colors(i,reps,samples):
        sample_batch = []
        for s in samples[i*reps:i*reps+reps]:
            color = get_pixel(s['x'],s['y'])
            s.update({'color':color})
            sample_batch.append(s)

        thread_samples.update({i:sample_batch})

    for i in range(0,SAMPLES_Y):
        t = threading.Thread(target = get_sample_colors, args=(i,SAMPLES_X,samples))
        t.setDaemon(True)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    for i in sorted(thread_samples):
        for l in thread_samples[i]:
            #print(l)
            _samples.append(l)
            
    for t in threads:
        print(t.name)
        del(t)

    print(threads)
    '''
    for s in samples:
        color = get_pixel(s['x'],s['y'])
        s.update({'color':color})
        _samples.append(s)
    ''' 
    return _samples

def visualize(vis,samples):
    vis.show()
    vis.update(samples)

def main():
    samples = create_sample_cords(MONITOR_W,MONITOR_H,SAMPLE_RADIUS,SAMPLE_CORNER,SAMPLES_X,SAMPLES_Y)
    vis = visualizer.Visualization()
    vis.setup(MONITOR_W,MONITOR_H,samples,SAMPLE_RADIUS)
    while True:
        # calculate cords for the samples
        # get color from the sample cords
        samples = get_samples(samples) # ---------------------- lag
        visualize(vis,samples)
        print('tick')


if __name__ == '__main__':
    main()
    #space_samples(MONITOR_W,MONITOR_H,SAMPLE_RADIUS,SAMPLE_CORNER,SAMPLES_X,SAMPLES_Y)

    #gui = myGUI()
    #process = multiprocessing.Process(target=myGUI)
    #process.start()
