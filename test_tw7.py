import sys
import struct
import array

# gestione file binario
def gestione_file(nomefile):
	ff = open(nomefile, 'r+b')
	ff.seek(0, 2)
	dlen = ff.tell()
	ff.seek(0,0)
	print("file length:", dlen)
	data_raw=array.array('B')
	while True:
		b = ff.read(8192) # blocchi di 8k max
		if not b:
			break
		data_raw.frombytes(b)
	magic = struct.unpack('4s', data_raw[0:4])[0]
	model = struct.unpack('8s', data_raw[4:12])[0]
	print( "magic/model:", ''.join([chr(x) for x in magic]), ''.join([chr(x) for x in model]) )
	# lunghezza dati
	l1_s = struct.unpack('BBB', data_raw[12:15])
	l1 = int(l1_s[0]) + int(l1_s[1]) * 256 + int(l1_s[2]) * 65536
	print("len1: ", l1)
	# lunghezza campioni
	l2_s = struct.unpack('BBB', data_raw[20:23])
	l2 = int(l2_s[0]) + int(l2_s[1]) * 256 + int(l2_s[2]) * 65536
	print("len2: ", l2)
	sf = struct.unpack('H', data_raw[366:368])[0]
	print("sampling freq:", sf)
	sk = struct.unpack('B', data_raw[368:369])[0]
	print("sample key:", sk)
	ss = 0x114 + (l1-l2)
	print("start samples:", hex(ss), "(dec ", ss, ")")
	ff.close()
	
if len(sys.argv) > 1:
	gestione_file(sys.argv[1])
	
