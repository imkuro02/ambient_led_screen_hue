import os
from monitor import get_monitor
import color
from clamp import clamp
from sample import Sample_manager
from overlay import Overlay
from screenshot import color_samples
from ser import Serial

import time

def main():
    SERIAL_PORT = '/dev/ttyACM0'
    MONITOR_NAME = 'DP-2'
    MONITOR = get_monitor(MONITOR_NAME)

    sample_bottom_only =    True
    sample_center =         False
    sample_edge =           True
    hor,ver,size =          24, 5, 140

    SAMPLE_MANAGER = Sample_manager(MONITOR,
                                    hor,
                                    ver,
                                    size,
                                    sample_bottom_only,
                                    sample_center,
                                    sample_edge)

    samples = SAMPLE_MANAGER.create_sample_locations()

    overlay = Overlay(MONITOR.x,MONITOR.y,MONITOR.width,MONITOR.height)
    overlay.draw(samples,size)
    
    
    while True:
        start = time.time()

        samples = color_samples(samples,size)
        ser = Serial(SERIAL_PORT)
        ser.send(samples)

        done = time.time()
        elapsed = done - start

        # the two lines below make sure for it to keep a steady 30 fps
        delay=0.033333-elapsed
        if delay >= 0 : time.sleep(delay)

        done = time.time()
        elapsed = done - start
        os.system('clear')
        print('spd:',elapsed)
        print('fps:',1/elapsed)




if __name__ == '__main__':
    main()
   
