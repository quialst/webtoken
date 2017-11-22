import io
import stem.process
import stem.control
from stem.util import term
import requests

class Node:
    def print_bootstrap_lines(line):
        if "Bootstrapped" in line:
            print(term.format(line, term.Color.BLUE))

    def init(port, locale):
        SOCKS_PORT = port
        if port == None:
            SOCKS_PORT = 7000
        if locale == None:
            locale = 'en'
        tor_process = stem.process.launch_tor_with_config(
            config = {
                'SocksPort': str(SOCKS_PORT),
                'ExitNodes': '{%s}' % locale,
            },
            init_msg_handler = print_bootstrap_lines,
        )
    def get_nodes():
    def query(payload, node):
            r = requests.post(str(node), data=payload)
            return r.text
