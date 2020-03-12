'''Network related methods.'''
import socket
import subprocess


class Network:
    '''Network related methods.'''

    WIFI_GLYPH = '直'
    WIFI_DISABLED_GLYPH = '睊'

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

    @staticmethod
    def get_hostname():
        '''Returns the hostname.'''
        return socket.gethostname()

    @staticmethod
    def get_ssid():
        '''Get the SSID if the raspberry pi is connected to a wifi network.'''
        ssid = subprocess.run(['iwgetid', '-r'],
                              capture_output=True).stdout
        return ssid.strip().decode('utf-8')
