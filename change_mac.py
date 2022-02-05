#!/usr/bin/env python3
import subprocess
import optparse # get arguments from user, parse and use in code
import re # to use regular expressions

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

def current_mac(interface):
	# ways to verify result:
	# 1. execute and read ifconfig
	ifconfig_result = subprocess.check_output(["ifconfig", interface])
	# 2. read the mac address from output using regex rule/pattern \w\w:\w\w:\w\w:\w\w:\w\w:\w\w
        # where, \w refers to alphanumeric character
	mac_address_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
	# 3. check if MAC in ifconfig is what the user requested
	if mac_address_search:
		return mac_address_search.group(0)
	else:
		print("[-] Could not read MAC address.")
	
options = get_args()
current_mac = current_mac(options.interface)
print("Current MAC = " + str(current_mac))
change_mac(options.interface, options.new_mac)
current_mac = current_mac(options.interface) # after change
if current_mac == options.new_mac:
	print("[+] MAC address was successfully changed to " + current_mac)
else:
	print("[-] MAC address did not change. Try again.")
