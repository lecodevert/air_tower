'''Network related methods.'''
import socket


class Network:
    '''Network related methods.'''

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
