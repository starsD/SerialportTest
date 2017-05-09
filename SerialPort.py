import serial
import serial.tools.list_ports
from time import sleep

class serialPort(object):
    def __init__(self):
        self.ser = None
        pass

    def detectPort(self):
        port_list = list(serial.tools.list_ports.comports())
        ports_name = []
        for i in range(len(port_list)):
            ports_name.append(port_list[i][0])
        return ports_name

    def set(self, **kwargs):
        print(kwargs)

        self.ser = serial.Serial(port=kwargs['port'], baudrate=kwargs['baudrate'], bytesize=kwargs['bytesize'])


