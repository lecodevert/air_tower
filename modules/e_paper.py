'''Epd2in9d module.'''
import os
import time
from PIL import Image, ImageDraw, ImageFont
from modules.waveshare_epd import epd2in9d
from modules import network

PICDIR = 'img'
FONTDIR = 'fonts'
FONT24 = 'Roboto Mono Bold Nerd Font Complete.ttf'
FONT18 = 'Roboto Mono Nerd Font Complete.ttf'


def display(func):
    '''Decorator for all display screens.'''
    def wrapper(*args, **kwargs):
        self = args[0]
        # Background image support
        if 'background' in kwargs:
            frame = Image.open(os.path.join(PICDIR, kwargs['background']))
            del kwargs['background']
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

        self.font24 = ImageFont.truetype(os.path.join(FONTDIR, FONT24), 24)
        self.font18 = ImageFont.truetype(os.path.join(FONTDIR, FONT18), 18)

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

    # pylint: disable=unused-argument
    # background argument is actually used in the decorator
    @display
    def display_network_info(self, draw=None, background=None):
        '''Display a screen with network information.'''
        net = network.Network
        draw.text((2, 2), net.get_hostname(), font=self.font24,
                  fill=0)
        draw.text((2, 28), net.get_ip(), font=self.font24,
                  fill=0)
        ssid = net.get_ssid()
        glyph = net.WIFI_GLYPH if ssid else net.WIFI_DISABLED_GLYPH
        draw.text((2, 54), "{} {}".format(glyph, ssid), font=self.font24,
                  fill=0)

    # pylint: disable=unused-argument
    # background argument is actually used in the decorator
    @display
    def display_all_data(self, data, draw=None, background=None):
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
