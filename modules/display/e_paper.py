import os
import socket
import time
from modules.waveshare_epd import epd2in9d
from PIL import Image, ImageDraw, ImageFont

PICDIR = 'pic'

class Epaper:

    def __init__(self):
        self.epd = epd2in9d.EPD()
        self.epd.init()
        self.epd.Clear(0xFF)

        self.font24 = ImageFont.truetype(os.path.join(PICDIR, 'Font.ttc'), 24)
        self.font18 = ImageFont.truetype(os.path.join(PICDIR, 'Font.ttc'), 18)

    def blank_frame(self):
        frame = Image.new('1', (self.epd.height, self.epd.width), 255)
        return [frame, ImageDraw.Draw(frame)]

    def clear(self):
        self.epd.Clear(0xFF)

    def sleep(self):
        time.sleep(2)
        self.epd.sleep()

    @staticmethod
    def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def display_network_info(self):
        frame, draw = self.blank_frame()
        hostname = socket.gethostname()
        ip = Epaper.get_ip()

        draw.text((10, 0), hostname, font=self.font24, fill=0)
        draw.text((10, 20), ip, font=self.font24, fill=0)
        self.epd.display(self.epd.getbuffer(frame))
        self.sleep()
