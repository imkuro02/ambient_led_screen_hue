# importing tkinter for gui
import tkinter as tk
import tkinter as tk # Python 3
from tkinter import Canvas, Frame, BOTH, Tk

class Drawer():
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self,samples,sample_radius):
        root = tk.Tk()
        root.overrideredirect(True)
        root.geometry(f'{self.w}x{self.h}+{self.x}+{self.y}')
        root.lift()
        root.wm_attributes("-topmost", True)
        root.wm_attributes("-alpha", 0.6)
        canvas = tk.Canvas(root,bg='white',height=self.h,width=self.w)
        for s in samples:
            x = s['x']-self.x
            y = s['y']-self.y
            print(x,y)
            size = sample_radius
            canvas.create_line(x, y, x+size, y, fill = "red")
            canvas.create_line(x, y, x, y+size, fill = "red")
            canvas.create_line(x+size, y+size, x+size, y, fill = "red")
            canvas.create_line(x, y+size, x+size, y+size, fill = "red")
        
        canvas.pack()
        root.mainloop()

if __name__  == '__main__':
    d = Drawer(0,0,100,100)
    d.draw()
