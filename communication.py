#!/usr/bin/env python3

from assistant import Albus, create_message_dict, dict_to_bytes

from mesh.links import UDPLink
from mesh.node import Node

import time


if __name__ == "__main__":

    living_room_config = {
        'node_name': 'beta',
        'node_location': 'living_room',
        'available_input_devices': [],
        'available_output_devices': [
            'speaker'
        ]
    }

    bedroom_config = {
        'node_name': 'alpha',
        'node_location': 'bedroom',
        'available_input_devices': [
            'microphone'
        ],
        'available_output_devices': []
    }

    config = bedroom_config

    links = [UDPLink('en0', 2010)]

    node = Node(links,
                config['node_name'],
                Filters=[],
                Program=Albus)

    node.program.apply_config(config)

    [link.start() for link in links]
    node.start()

    print("Run lan-chat.py on another laptop to talk between the two of you on en0.")
    try:
        while True:
            message = input('<< ')

            message_dict = create_message_dict('Light On',  '',
                                               config['node_name'],
                                               'light')
            message_bytes = dict_to_bytes(message_dict)

            node.send(message_bytes)

            time.sleep(0.3)

    except (EOFError, KeyboardInterrupt):
        node.stop()
        [link.stop() for link in links]
