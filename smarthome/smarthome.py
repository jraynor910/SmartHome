from pprint import pprint
import logging
import argparse
import socket
from pyHS100.pyHS100 import SmartPlug, TPLinkSmartHomeProtocol
logging.basicConfig()
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


class SmartHome(object):

    def __init__(self):
        self.args = self.parse_args()
        devices = self.args.target

        if self.args.command == 'discovery':
            self.discover_devices()

        if devices:
            self.smart_plugs = []
            for device in devices:
                LOGGER.debug("Creating SmartPlug instance for IP: {}".format(device))
                self.perform_action(SmartPlug(device))


    def perform_action(self, smart_plug):
        command = self.args.command

        try:
            if command.lower() == "off":
                LOGGER.info("Turning SmartPlug: {} OFF".format(smart_plug.mac))
                smart_plug.turn_off()
            elif command.lower() == "on":
                LOGGER.info("Turning SmartPlug: {} ON".format(smart_plug.mac))
                smart_plug.turn_on()
            elif command.lower() == 'status':
                LOGGER.info("SmartPlug {} is: {}".format(smart_plug.mac, smart_plug.state))
            else:
                raise RuntimeError("Unsupported command: {}".format(command))
        except Exception as error:
            LOGGER.error(error)


    def parse_args(self):
        commands = ["on", "off", "status", "discovery"]
        # Parse commandline arguments
        parser = argparse.ArgumentParser(description="TP-Link Wi-Fi Smart Plug Client")
        parser.add_argument("-t", "--target", metavar="<ip>", help="Target IP Address", type=self.validIP)
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

    def discover_devices(self):

        devices = TPLinkSmartHomeProtocol.discover()
        for device in devices:
            LOGGER.info("Found SmartPlug: {}".format(device))

if __name__ == "__main__":
    smart_home = SmartHome()
