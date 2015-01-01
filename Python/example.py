import sys
sys.path.insert(0, './Python/CyKit/')
import emotiv
import gevent
import socket
del socket
del sys

if __name__ == "__main__":
    headset = emotiv.Emotiv(False, False)
    gevent.spawn(headset.setup)
    gevent.sleep(1)
    try:
        while True:
            packet = headset.dequeue()
            print packet.gyro_x, packet.gyro_y
            gevent.sleep(0)
    except KeyboardInterrupt:
        headset.close()
    finally:
        headset.close()
