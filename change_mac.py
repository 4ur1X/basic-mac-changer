#!/usr/bin/env python3
import subprocess
import optparse # get arguments from user, parse and use in code

def get_args():
	parser = optparse.OptionParser()
	parser.add_option("-i", "--interface", dest="interface", help="provide the interface to change its MAC address e.g eth0")
	parser.add_option("-m", "--mac", dest="new_mac", help="provide a new MAC address to change to")
	(options, arguments) = parser.parse_args()
	# check if user has provided all required inputs
	if not options.interface:
		parser.error("[-] Please specify an interface, use --help / -h for more info")
	elif not options.new_mac:
		parser.error("[-] Please specify a new MAC address, use --help / -h for more info")
	return options

def mac_change(interface, new_mac):
	print("[+] Changing MAC address for " + interface + " to " + new_mac)

	subprocess.call(["ifconfig", interface, "down"])
	subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
	subprocess.call(["ifconfig", interface, "up"])

options = get_args()
change_mac(options.interface, options.new_mac)