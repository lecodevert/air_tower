'''Epd2in9d module.'''
import os
import socket
import time
from PIL import Image, ImageDraw, ImageFont
from modules.waveshare_epd import epd2in9d

PICDIR = 'pic'
FONTDIR = 'fonts'


def display(func):
    '''Decorator for all display screens.'''
    def wrapper(*args, **kwargs):
        self = args[0]
        frame, draw = self.blank_frame()
        kwargs['draw'] = draw
        func(*args, **kwargs)
        self.epd.display(self.epd.getbuffer(frame))
        self.sleep()
    return wrapper


class Epaper:
    '''Class used for using the e-paper display.'''

    def __init__(self):
        '''Creates a new display object.'''
        self.epd = epd2in9d.EPD()
        self.epd.init()
        self.epd.Clear(0xFF)

        self.font24 = ImageFont.truetype(os.path.join(FONTDIR, 'Font.ttc'), 24)
        self.font18 = ImageFont.truetype(os.path.join(FONTDIR, 'Font.ttc'), 18)

    def blank_frame(self):
        '''Returns a blank image object and tools to draw on it.'''
        frame = Image.new('1', (self.epd.height, self.epd.width), 255)
        return [frame, ImageDraw.Draw(frame)]

    def clear(self):
        '''Physically clear the content of the display.'''
        self.epd.Clear(0xFF)

    def sleep(self):
        '''Put the display into sleep mode, with no power usage.'''
        time.sleep(2)
        self.epd.sleep()

    @staticmethod
    def get_ip():
        '''Returns the main ip address of the system.'''
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            sock.connect(('10.255.255.255', 1))
            ip_addr = sock.getsockname()[0]
        except socket.error:
            ip_addr = '127.0.0.1'
        finally:
            sock.close()
        return ip_addr

    @display
    def display_network_info(self, draw):
        '''Display a screen with network information.'''
        draw.text((10, 0), socket.gethostname(), font=self.font24, fill=0)
        draw.text((10, 20), Epaper.get_ip(), font=self.font24, fill=0)

    @display
    def display_all_data(self, data, draw):
        '''Display a screen with all the data collected from sensors.'''
        draw.text((10, 0), data, font=self.font24, fill=0)
