#!/usr/bin/env python3
from scapy.all import *
import argparse
import time
import sys
from datetime import datetime

def get_mac(interface):
    with open(f'/sys/class/net/{interface}/address') as f:
        return f.read().strip()

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", required=True)
    parser.add_argument("-t", "--interval", type=int, default=15)
    parser.add_argument("-r", "--real-mac", action="store_true")
    args = parser.parse_args()
    # define MAC address
    mac = get_mac(args.interface) if args.real_mac else RandMAC()
    mac_type = "real" if args.real_mac else "random"
    # start sending packets
    log(
        f"Starting dhcp-keepalive on {args.interface}"
        f", using {mac_type} MAC"
        f", using interval {args.interval}s"
    )
    while True:
        # broadcast one DHCP DISCOVER packet
        sendp(
            Ether(dst="ff:ff:ff:ff:ff:ff")/
            IP(src="0.0.0.0", dst="255.255.255.255")/
            UDP(sport=68, dport=67)/
            BOOTP(chaddr=mac.encode()[:6] if args.real_mac else RandMAC().encode()[:6])/
            DHCP(options=[("message-type", "discover"), "end"]),
            iface=args.interface,
            verbose=0
        )
        log(
            f"Sent DHCPDISCOVER on {args.interface}"
            f", using {mac_type} MAC"
            f", next in {args.interval}s"
        )
        # wait before sending next packet
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
