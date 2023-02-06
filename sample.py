import numpy as np

class Sample:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.color = None

    def set_color(self,col):
        self.color = col

class Sample_manager:
    def __init__(self,monitor,hor,ver,size,sample_bottom_only,sample_center,sample_edge):
        self.monitor = monitor  # monitor object
        self.hor = hor          # amount of samples horizontally
        self.ver = ver          # amount of samples vertically
        self.size = size        # size of sample (square)

        self.sample_bottom_only = sample_bottom_only
        self.sample_center = sample_center 
        self.sample_edge = sample_edge

    def create_sample_locations(self) -> Sample:
        samples = []
        
        x = self.monitor.x + np.linspace(start=0,
                                          stop=self.monitor.width-self.size,
                                          num=self.hor,
                                          endpoint=True)

        y = self.monitor.y + np.linspace(start=0,
                                          stop=self.monitor.height-self.size,
                                          num=self.ver,
                                          endpoint=True)

        for _x in x:
            for _y in y:
                s = Sample(_x,_y)
                samples.append(s)

        first_sample = samples[0]
        last_sample = samples[-1]
        x1, y1 = first_sample.x, first_sample.y
        x2, y2 = last_sample.x, last_sample.y

        if not self.sample_center:
            temp_samples = []
            for i, s in enumerate(samples):
                x,y = int(s.x),int(s.y)
                if (int(x) == int(x1) or int(x) == int(x2) or int(y) == int(y1) or int(y) == int(y2)):
                    temp_samples.append(s)
                else:
                    pass
                    #print('deleting:',s.x,s.y)
            samples = temp_samples

        if self.sample_bottom_only:
            temp_samples = []
            for i, s in enumerate(samples):
                x,y = int(s.x),int(s.y)
                if (int(y) == int(y2)):
                    temp_samples.append(s)
                else:
                    pass
                    #print('deleting:',s)
            samples = temp_samples


        return samples

