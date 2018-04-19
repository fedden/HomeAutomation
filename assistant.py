from mesh.programs import BaseProgram
from utils import to_bytes, to_str
import json


def create_message_dict(header,
                        data,
                        source_node,
                        required_output_devices):
    message_dict = {
        'header': header,
        'data': data,
        'source_node': source_node,
        'required_output_devices': required_output_devices
    }
    return message_dict


def dict_to_bytes(message_dict):
    message_str = json.dumps(message_dict)
    message_bytes = to_bytes(message_str)
    return message_bytes


def bytes_to_dict(message_bytes):
    message_str = to_str(message_bytes)
    message_dict = json.loads(message_str)
    return message_dict


class Albus(BaseProgram):

    def __init__(self, config):
        BaseProgram.__init__(self)
        self.node_name = config['node_name']
        self.node_location = config['node_location']
        self.available_input_devices = config['available_input_devices']
        self.available_output_devices = config['available_output_devices']

    def parse_message(self, message_dict):
        print('message:     ', message_dict['header'])
        print('data:        ', message_dict['data'])
        print('source:      ', message_dict['source_node'])
        print('req devices: ', message_dict['required_output_devices'])

    def recv(self, packet, interface):
        message_dict = bytes_to_dict(packet.decode())
        self.parse_message(message_dict)
