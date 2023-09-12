#!/usr/bin/env python
import argparse
import signal
import select
import socket
from importlib import reload
import TCPproxy.pwn_client as pwn_client
import keyboard
import sys

BUFFER_SIZE = 2 ** 12 #Keep buffer size as power of 2.

#DONT EDIT THIS UNLESS YOU WANT TO ADD MORE HOTKEYS (current functionality exists for ctrl + 'space' and 0..9)
	 
def tcp_proxy(src, dst):
	"""Run TCP proxy.
	Arguments:
	src -- Source IP address and port string. I.e.: '127.0.0.1:8000'
	dst -- Destination IP address and port. I.e.: '127.0.0.1:8888'
	"""
	print('Starting TCP proxy... press ctrl+C to exit... right-click to copy!')
	 
	sockets = []
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((src,2010))
	s.listen(1)
	s_src, _ = s.accept()
	s_dst = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s_dst.connect((dst,2010)) 
	
	sockets.append(s_src)
	sockets.append(s_dst)
	
	def set_HOTKEY(key):
		print(f'\n{key} pressed... Please Wait')
		global HOTKEY
		HOTKEY = key
		return None
	
	global HOTKEY
	HOTKEY = False
	  
	### add more hotkeys here
	for key in ['ctrl+space']+['ctrl+'+str(n) for n in range(0,10)]:
		keyboard.add_hotkey(key, set_HOTKEY, args=[key])
	
	while True:
		reload(pwn_client)
		
		s_read, _, _ = select.select(sockets, [], [])
	
		for s in s_read:
			data = s.recv(BUFFER_SIZE)

			if s == s_src:
				''' For manipulating client packets '''
				try:
					d1 = pwn_client.forward_packet(data)
					s_dst.sendall(d1)
				except Exception as e:
					print(e, '(error in forward_packet function)')
				
				'''for sending client packets'''
				if HOTKEY:
					try:
						d2, HOTKEY = pwn_client.create_packet(HOTKEY)
						s_dst.sendall(d2)
					except Exception as e:
						print(e, '(error in create_packet function).')
				
			elif s == s_dst:
				d = data
				s_src.sendall(d)
