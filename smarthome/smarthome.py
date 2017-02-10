# from smarthome.pyHS100 import SmartPlug
from pyHS100.pyHS100 import SmartPlug
import logging
import argparse
import socket
logging.basicConfig()
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


class SmartHome(object):

    def __init__(self):
        self.args = self.parse_args()
        ips = self.args.target
        LOGGER.info("Creating SmartPlug instance for IP: {}".format(ips))

        self.smart_plugs = []
        for ip in ips:
            self.smart_plugs.append(SmartPlug(ip))


    def perform_action(self):

        command = self.args.command

        for plug in self.smart_plugs:
            if command.lower() == "off":
                LOGGER.info("Turning SmartPlug: {} OFF".format(plug.mac))
                plug.turn_off()
            elif command.lower() == "on":
                LOGGER.info("Turning SmartPlug: {} ON".format(plug.mac))
                plug.turn_on()
            else:
                raise RuntimeError("Unsupported command: {}".format(command))


    def parse_args(self):
        commands = ["on", "off"]
        # Parse commandline arguments
        parser = argparse.ArgumentParser(description="TP-Link Wi-Fi Smart Plug Client")
        parser.add_argument("-t", "--target", metavar="<ip>", required=True, help="Target IP Address", type=self.validIP)
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("-c", "--command", metavar="<command>", help="Preset command to send. Choices are: {}".format(commands))
        return parser.parse_args()

    def validIP(self, ips):
        if ips.split(";"):
            ips = ips.split(";")
        try:
            for ip in ips:
                socket.inet_pton(socket.AF_INET, ip)
        except socket.error:
            LOGGER.error("Invalid IP Address.")
        return ips

if __name__ == "__main__":
    smart_home = SmartHome()
    smart_home.perform_action()
