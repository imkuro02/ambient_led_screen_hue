import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from threading import Thread

plt.ion()

class Visualization:
    def __init__(self):
        pass
        
    def setup(self,monitor_x,monitor_y,monitor_w,monitor_h,samples,radius):
        self.fig, self.ax = plt.subplots()
        self.ax.axis('equal')
        plt.plot(monitor_x,monitor_y,monitor_w,monitor_h)
        self.ax.invert_yaxis()

        self.samples = []

        # dont care
        #self.border_rec = Rectangle((monitor_x-256,monitor_y-256),monitor_w,monitor_h,fill = False)
        #self.ax.add_artist(self.border_rec)
        self.ax.set_title('Click to move the circle')

        for i, s in enumerate(samples):
            c = Circle((s['x'],s['y']),radius)
            self.ax.add_artist(c)
            plt.text(s['x'],s['y'],f'{int(s["x"])},{int(s["y"])} {i}')
            self.samples.append(c)

    def update(self,samples):
        '''
        for i, c in reversed(list(enumerate(self.samples))):
            self.samples[i].set_facecolor(f"#{samples[i]['color']}")
        '''
        for s in samples:
            for i, self_sample in list(enumerate(self.samples)):   
                x,y = self_sample.get_center()
                if s['x'] == x and s['y'] == y :
                    self.samples[i].set_facecolor(f"#{samples[i]['color']}")
            
            
    '''
    def on_click(self, event):
        if event.inaxes is None:
            return
        self.circ[0].center = event.xdata, event.ydata
        self.fig.canvas.draw()
    '''

    def show(self):

        self.fig.canvas.flush_events()
        '''
        while True:
            #plt.show()
            self.fig.canvas.flush_events()
            self.update()
        '''

if __name__ == '__main__':
    vis = Visualization().show()
