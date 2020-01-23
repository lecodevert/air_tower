'''Epd2in9d module.'''
import os
import socket
import time
from PIL import Image, ImageDraw, ImageFont
from modules.waveshare_epd import epd2in9d

PICDIR = 'img'
FONTDIR = 'fonts'


def display(func):
    '''Decorator for all display screens.'''
    def wrapper(*args, **kwargs):
        self = args[0]
        # Background image support
        if 'bg' in kwargs:
            frame = Image.open(os.path.join(PICDIR, kwargs['bg']))
            del kwargs['bg']
            draw = ImageDraw.Draw(frame)
        else:
            frame, draw = self.blank_frame()

        kwargs['draw'] = draw
        func(*args, **kwargs)
        self.epd.display(self.epd.getbuffer(frame.transpose(Image.ROTATE_180)))
        time.sleep(2)
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
    def display_network_info(self, draw=None, bg=None):
        '''Display a screen with network information.'''
        draw.text((128, 0), socket.gethostname(), font=self.font24, fill=0)
        draw.text((128, 20), Epaper.get_ip(), font=self.font24, fill=0)

    @display
    def display_all_data(self, data, draw=None, bg=None):
        '''Display a screen with all the data collected from sensors.'''
        draw.text((32, 8), "{:.1f}{}".format(data['temperature']['value'],
                                             data['temperature']['unit']),
                  font=self.font24, fill=0)
        draw.text((32, 40), "{:.0f}{}".format(data['humidity']['value'],
                                              data['humidity']['unit']),
                  font=self.font24, fill=0)
        draw.text((32, 72), "{:.0f}{}".format(data['pressure']['value'],
                                              data['pressure']['unit']),
                  font=self.font24, fill=0)
        draw.text((32, 104), "{:.0f}{}".format(data['light']['value'],
                                               data['light']['unit']),
                  font=self.font24, fill=0)
        draw.text((128, 8), "{}: {:.0f}{}".format(data['pm1']['name'],
                                                  data['pm1']['value'],
                                                  data['pm1']['unit']),
                  font=self.font18, fill=0)
        draw.text((128, 24), "{}: {:.0f}{}".format(data['pm25']['name'],
                                                   data['pm25']['value'],
                                                   data['pm25']['unit']),
                  font=self.font18, fill=0)
        draw.text((128, 42), "{}: {:.0f}{}".format(data['pm10']['name'],
                                                   data['pm10']['value'],
                                                   data['pm10']['unit']),
                  font=self.font18, fill=0)
        draw.text((128, 60), "{}: {:.0f}{}".format(data['nh3']['name'],
                                                   data['nh3']['value'],
                                                   data['nh3']['unit']),
                  font=self.font18, fill=0)
        draw.text((128, 78), "{}: {:.0f}{}".format(data['oxidising']['name'],
                                                   data['oxidising']['value'],
                                                   data['oxidising']['unit']),
                  font=self.font18, fill=0)
        draw.text((128, 96), "{}: {:.0f}{}".format(data['reducing']['name'],
                                                   data['reducing']['value'],
                                                   data['reducing']['unit']),
                  font=self.font18, fill=0)
