#!/usr/bin/env python3

"""
A python script to get battery level from Samsung Galaxy Buds devices
"""

# License: MIT
# Author: @ThePBone
# 06/30/2020

import bluetooth
import sys
import argparse
import datetime

msg_debounce = ""


def print_result(string, timestamp):
    global msg_debounce
    if msg_debounce != string:
        if timestamp:
            print(string + "," + datetime.datetime.now().strftime("%FT%T.%f")[:-4] + "Z")
        else:
            print(string)
        msg_debounce = string


def parse_message(data, islegacy, timestamp):
    if data[0] != (0xFE if islegacy else 0xFD ):
        print("Invalid SOM")
        exit(2)
    if data[3] == 97:
        if not islegacy:
            string = "{},{},{}".format(data[6], data[7], data[11])
        else:
            string = "{},{}".format(data[6], data[7])
    elif data[3] == 96:
        if not islegacy:
            string = "{},{},{}".format(data[5], data[6], data[10])
        else:
            string = "{},{}".format(data[5], data[6])
    else:
        return False
    print_result(string, timestamp)
    return True


def parse_message_wear_status(data, islegacy, timestamp):
    global msg_debounce
    if data[0] != (0xFE if islegacy else 0xFD):
        print("Invalid SOM")
        exit(2)
    if data[3] == 97:
        state = data[10]
    elif data[3] == 96:
        state = data[9]
    else:
        return False

    if not islegacy:
        left = id_to_placement((state & 240) >> 4)
        right = id_to_placement(state & 15)
        string = "{},{}".format(left, right)
    else:
        if state == 0:
            string = "None"
        elif state == 1:
            string = "Right"
        elif state == 16:
            string = "Left"
        elif state == 17:
            string = "Both"
        else:
            string = "Unknown"

    print_result(string, timestamp)
    return True


def id_to_placement(id):
    if id == 0:
        return "Disconnected"
    elif id == 1:
        return "Wearing"
    elif id == 2:
        return "Idle"
    elif id == 3:
        return "InCase"
    elif id == 4:
        return "InClosedCase"


def main():
    parser = argparse.ArgumentParser(description='Read battery values of the Samsung Galaxy Buds, Buds+, Buds Live or Buds Pro'
                                                 '[Left, Right, Case (Buds+ or later)]')
    parser.add_argument('mac', metavar='mac-address', type=str, nargs=1,
                        help='MAC-Address of your Buds')
    parser.add_argument('-m', '--monitor', action='store_true', help="Notify on change")
    parser.add_argument('-t', '--monitor-timestamp', action='store_true', help="Notify on change and print timestamps")
    parser.add_argument('-w', '--wearing-status', action='store_true', help="Print wearing status instead")
    parser.add_argument('-v', '--verbose', action='store_true', help="Print debug information")
    args = parser.parse_args()

    verbose = args.verbose

    if verbose:
        print("Checking device model...")
    islegacy = "Galaxy Buds (" in str(bluetooth.lookup_name(args.mac[0]))

    if verbose:
        print(str(bluetooth.lookup_name(args.mac[0])))
        print("Searching for RFCOMM interface...")

    uuid = ("00001101-0000-1000-8000-00805F9B34FB" if not islegacy else "00001102-0000-1000-8000-00805f9b34fd")
    service_matches = bluetooth.find_service(uuid=uuid, address=str(args.mac[0]))

    port = host = None
    for match in service_matches:
        if match["name"] in (b"GEARMANAGER", "GEARMANAGER"):
            port = match["port"]
            host = match["host"]
            break

    if port is None or host is None:
        print("Couldn't find the proprietary RFCOMM service")
        sys.exit(1)

    if verbose:
        print("RFCOMM interface found. Establishing connection...")

    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((host, port))

    if verbose:
        print("Connected. Waiting for incoming data...")

    try:
        while True:
            data = sock.recv(1024)
            if len(data) == 0:
                break
            if args.wearing_status:
                success = parse_message_wear_status(data, islegacy, args.monitor_timestamp)
            else:
                success = parse_message(data, islegacy, args.monitor_timestamp)

            if success and not args.monitor and not args.monitor_timestamp:
                exit(0)

    except IOError:
        pass


if __name__ == "__main__":
    main()
