import serial
import time
import random

serialPort = serial.Serial(port="/dev/ttyACM0", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

def send(msg):
    for c in msg:
        time.sleep(0.0001)
        serialPort.write(c.encode('utf-8'))
        serialPort.flushInput()

def test(x=0,xx=0,xxx=0,xxxx=0):
    while True:
        i = random.randrange(0,255)
        r = random.randrange(0,255)
        g = random.randrange(0,255)
        b = random.randrange(0,255)
        r,g,b = 255,255,255

        print(i,r,g,b)
        
        serialPort.write(f'{i},{r},{g},{b}\n'.encode())
        serialPort.flushInput()

if __name__ == '__main__':
    test()

