import argparse
from TCPproxy.TCPproxy import tcp_proxy

def main():
	"""Main method."""
	parser = argparse.ArgumentParser(description='TCP/UPD proxy.')
		  
	parser.add_argument('-s', '--src', required=True, help='Source IP and port, i.e.: 127.0.0.1:8000')
	parser.add_argument('-d', '--dst', required=True, help='Destination IP and port, i.e.: 127.0.0.1:8888')
	 
	args = parser.parse_args()

	tcp_proxy(args.src, args.dst)

if __name__ == '__main__':
	main()