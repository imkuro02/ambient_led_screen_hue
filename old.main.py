from screeninfo import get_monitors
import mss
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
import multiprocessing
import os

SAMPLES_X, SAMPLES_Y = 4,3 # amount of x and y leds
SAMPLE_RADIUS = 16
SAMPLE_CORNER = True 
MONITOR = 'DP-4' # monitor name


# get monitor 
# create blank image
# get colors
# sample by x and y of LEDS_XY 
# blend colors in sample of pixel

for m in get_monitors():
    print(str(m))
    if MONITOR == m.name:
        MONITOR_W,MONITOR_H = m.width,m.height

get_monitors()

def hex_to_rgb(hex):
  rgb = []
  for i in (0, 2, 4):
    decimal = int(hex[i:i+2], 16)
    rgb.append(decimal)
  return tuple(rgb)

def rgb_to_hex(r, g, b):
  return ('{:X}{:X}{:X}').format(r, g, b)

def get_pixel(x,y):
    with mss.mss() as sct:
        pic = sct.grab({'mon':0, 'top':1, 'left':1, 'width':1, 'height':1})
        g = pic.pixel(0,0)
        print(g)
        r,g,b = g
        print(rgb_to_hex(r,g,b))

def visualize_samples(samples):
    img = Image.new('RGB', (MONITOR_W, MONITOR_H), color = 'white')
    draw = ImageDraw.Draw(img)
    for s in samples:
        x,y,r = s['x'],s['y'],SAMPLE_RADIUS
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(255,0,0,0))
    img.save('img.png')

def space_samples(  monitor_w,
                    monitor_h,
                    sample_radius,
                    sample_corner,
                    samples_x,
                    samples_y):

    # x is amount of samples
    samples = []
    # * SAMPLE_CORNER means, if true, do this, and if not true then 0 so false 
    space_x = round(monitor_w/(samples_x-int(sample_corner*1)))
    space_y = round(monitor_h/(samples_y-int(SAMPLE_CORNER*1)))
    for i in range(0,samples_x):
        for ii in range(0,samples_y):
                sample = {
                'x':(space_x*i)+((space_x/2)*int(not SAMPLE_CORNER)),
                'y':(space_y*ii)+((space_y/2)*int(not SAMPLE_CORNER))}
                samples.append(sample)
    visualize_samples(samples)

class myGUI(object):
    def __init__(self):
        self.image_scale = 0.3
        self.scaled_w = int(MONITOR_W * self.image_scale)
        self.scaled_h = int(MONITOR_H * self.image_scale)

        self.root = tk.Tk()
        self.canvas = tk.Canvas(width=800, height=800, bg='white')
        self.canvas.pack()

        filename="img.png"
        image = Image.open(filename)
        self.photo = ImageTk.PhotoImage(image)
        self.img = self.canvas.create_image(250, 250, image=self.photo)

        self.root.after(100, self.change_photo)
        self.root.mainloop()

    def change_photo(self):
        filename = "img.png"
        image = Image.open(filename)

        self.photo = ImageTk.PhotoImage(image)
        self.canvas.itemconfig(self.img, image=self.photo)
        self.root.after(3000, self.change_photo)
            

def gui():
    root = tk.Tk()
    canvas = tk.Canvas(root, width = MONITOR_W, height = MONITOR_H)
    canvas.pack()

    def update_canvas():
        img = Image.open("iimg.png")

        resized_image= img.resize((scaled_w,scaled_h), Image.Resampling.LANCZOS)
        new_image= ImageTk.PhotoImage(resized_image)

        canvas.itemconfig(image, image=new_image)
        root.after(3000,update_canvas)
        print('!@')

    image_scale = 0.3
    scaled_w = int(MONITOR_W * image_scale)
    scaled_h = int(MONITOR_H * image_scale)

    img = Image.open('img.png')
    resized_image= img.resize((scaled_w,scaled_h), Image.Resampling.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    image = canvas.create_image(10, 10, anchor=tk.NW, image=new_image)

    root.after(1000,update_canvas)
    root.mainloop()

if __name__ == '__main__':
    space_samples(MONITOR_W,MONITOR_H,SAMPLE_RADIUS,SAMPLE_CORNER,SAMPLES_X,SAMPLES_Y)

    #gui = myGUI()
    #process = multiprocessing.Process(target=myGUI)
    #process.start()
