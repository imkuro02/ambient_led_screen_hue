import serial
from color import *

class Serial:
    def __init__(self,port):
        self.port = port
        self.serialPort = serial.Serial(port=self.port, baudrate=2000000, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

    def send_to_serial(self,msg):
        for c in msg.split('\\'):
            c+='\\'
            if c == '\\': break
            c = c.encode('utf-8')
            self.serialPort.write(c)
            self.serialPort.flushInput()

    def send(self,samples):
        data = ''
        data += '0'+'\\'
        data += data*100
        for _, i in enumerate(samples):
            r,g,b = hex_to_rgb(i.color)
            data += f'{_},{r},{g},{b}\\'
        data += f'24\\'
        self.send_to_serial(data)

