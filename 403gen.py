import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("-o","--outfile",help="Specify an output file")
parser.add_argument("-s","--split",action="store_true",help="Separate headers and values into different files.")
parser.add_argument("-ch","--custom-headers",help="Specify a file with custom headers.")
parser.add_argument("-cv","--custom-values",help="Specify a file with custom values.")
parser.add_argument("-cp","--custom-ports",help="Specify a file with custom ports.")
parser.add_argument("-sd","--skip-default",action="store_true",help="Skip built-in values and only use custom values. Only if a custom list has been provided")
parser.add_argument("-hf","--http-force",action="store_true",help="Ensure https:// is prepended to each value.")
parser.add_argument("-pf","--port-force",action="store_true",help="Append port numbers to each value.")
parser.add_argument("-u","--upper",action="store_true",help="Force uppercase headers")
parser.add_argument("-us","--underscore",action="store_true",help="Replace - with _")

def ForceScheme(strin):
	output = re.sub(r"^http://","",strin)
	output = re.sub(r"^https://","",strin)
	output = "https://" + output
	return output

def ForcePort(strin):
	output = ""
	for p in default_ports:
		output += strin + ":" + p + "\n"
	output = output.rstrip("\n")
	return output

args = parser.parse_args()

#Common Referer based headers
default_headers = ["Client-IP","X-Real-IP","X-Client-IP","X-Rewrite-URL","X-Remote-IP","X-Remote-Addr","X-ProxyUser-Ip","X-Originating-IP","X-Original-URL","X-Forwarded","X-Custom-IP-Authorization","True-Client-IP","Referer","Host",
		   "Forwarded-For","Cluster-Client-IP","Connection","Content-Length","X-Original-For","X-Original-Forwarded-For","X-Forwarded-Host","X-Original-Host","X-Original-Proto","X-Requested-With","CF-Connecting-IP","Forwarded",
		   "Via","X-Azure-ClientIP","Fastly-Client-IP"]

#Various forms of private ip ranges, common CDN IP's, Search Engine Bot's, etc.
default_values = ["025405426427","025404000001","030052001017","030052000001","01215041440","01200000001","017710611200","017700000001","10101100.00010110.00101101.00010111","10101100.00010000.00000000.00000001",
				  "11000000.10101000.00000010.00001111","11000000.10101000.00000000.00000001","00001010.00110100.01000011.00100000","00001010.00000000.00000000.00000001","01111111.00100011.00010010.10000000",
				  "01111111.00000000.00000000.00000001","0xac162d17","0xac100001","0xc0a8020f","0xc0a80001","0x0a344320","0x0a000001","0x7f231280","0x7f000001","localhost:80","localhost:443","localhost","2887134487",
				  "2886729729","3232236047","3232235521","171197216","167772161","2133004928","2130706433","0254.0027.0055.0037","0254.0020.0000.0001","0300.0250.0002.0017","0300.0250.0000.0001","0012.0042.0113.0177",
				  "0012.0000.0000.0001","0177.0042.0200.0005","0177.0000.0000.0001","0","X-Foo","X-Close","http://localhost/","https://localhost/","0000.0000.0000.0000","0001.0001.0001.0001","0010.0010.0010.0010","0100200401",
				  "01002004010","16843009","134744072","00000000.00000000.00000000.00000000","00000001.00000001.00000001.00000001","00001000.00001000.00001000.00001000","0x00000000","0x01010101","0x08080808","64.233.160.23",
				  "162.247.240.23","64.39.96.23","149.154.167.34","199.16.156.124","173.252.64.7","107.21.0.27","104.18.0.5","77.88.21.3","180.76.15.1","20.191.45.203","98.137.207.1","157.55.39.1","66.249.66.1","127.1",
				  "127.99","10.1","10.4","172.16.1","127.0.0.1","127.35.18.128","10.0.0.1","10.52.67.32","192.168.0.1","192.168.2.15","172.16.0.1","172.22.45.23"]

default_ports = ["80","443","8080","8443"]

user_agents = ["Googlebot","facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)"]

#Here we are resetting the default values if specified by the user.
if args.skip_default:
	if args.custom_headers:
		default_headers = []
	if args.custom_values:
		default_values = []
	if args.custom_ports:
		default_ports = []

if args.custom_headers:
	with open(args.custom_headers,'r') as file:
		for line in file:
			default_headers.append(line.strip())

if args.custom_values:
	with open(args.custom_values,'r') as file:
		for line in file:
			default_values.append(line.strip())

if args.custom_ports:
	with open(args.custom_ports,'r') as file:
		for line in file:
			default_ports.append(line.strip())


#Write Headers and Values separately.

if args.split:
	for h in default_headers:
		if args.outfile:
			with open("headers_"+args.outfile, "a") as f:
				f.write(h + "\n")
				if args.upper:
					f.write(h.upper() + "\n")
				if args.underscore:
					f.write(re.sub(r"-","_",h) + "\n")
		else:
			print(h)
			if args.upper:
				print(h.upper())
			if args.underscore:
				print(re.sub(r"-","_",h))
	if args.outfile:
		print("Wrote headers to headers_" + args.outfile)

	for dv in default_values:
		if args.http_force:
			dv = ForceScheme(dv)
		if args.port_force:
			dv = ForcePort(dv)

		if args.outfile:
			with open("values_"+args.outfile, "a") as f:
				f.write(dv + "\n")
		else:
			print(dv)

	if args.outfile:
		print("Wrote values to values_" + args.outfile)
			

#Write Headers and Values together.
if not args.split:
	for h in default_headers:
		for dv in default_values:
			if args.http_force:
				dv = ForceScheme(dv)
			if args.outfile:
				with open(args.outfile, "a") as f:
					f.write(h + ": " + dv + "\n")
					if args.port_force:
						for p in default_ports:
							f.write(h + ": " + dv + ":" + p + "\n")
							if args.upper:
								f.write(h.upper() + ": " + dv + ":" + p + "\n")
							if args.underscore:
								f.write(re.sub(r"-","_",h) + ": " + dv + ":" + p + "\n")
					else:
						f.write(h + ": " + dv + "\n")
						if args.upper:
							f.write(h.upper() + ": " + dv + "\n")
						if args.underscore:
							f.write(re.sub(r"-","_",h) + ": " + dv + "\n")		
			else:
				if args.port_force:
						for p in default_ports:
							print(h + ": " + dv + ":" + p)
							if args.upper:
								print(h.upper() + ": " + dv + ":" + p)
							if args.underscore:
								print(re.sub(r"-","_",h) + ": " + dv + ":" + p)
				else:
					print(h + ": " + dv)
	if args.outfile:
			print("Wrote headers to " + args.outfile)





