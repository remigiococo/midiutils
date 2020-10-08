import sys
import array
import struct
import pretty_midi

# gestione file binario
def gestione_file(nomefile):
	ff = open(nomefile, 'r+b')
	ff.seek(0, 2)
	flen = ff.tell()
	ff.seek(0, 0)
	print("total len:", flen)
	data_raw=array.array('B')
	while True:
		b = ff.read(8192) # blocchi di 8k max
		if not b:
			break
		data_raw.frombytes(b)
	if data_raw[0:4] != array.array('B', [ord(x) for x in "AC07"]):
		print("not AC7 format !!!", data_raw[0:4])
		sys.exit(0)
	dlen = struct.unpack('H', data_raw[4:6])[0]
	print("data len:", dlen)	
	parse_drum(data_raw, 6)
	parse_othr(data_raw, 6)
	#ff.seek(4, 0)
	#ff.write(struct.pack('l', dlen+36))
	#ff.seek(40, 0)
	#ff.write(struct.pack('l', dlen))
	ff.close()
	
def parse_drum(raw, offset=0):
	i = offset
	max_i = len(raw[i:]) - 4
	while (i < max_i) and ( raw[i:i+4] != array.array('B', [ord(x) for x in "DRUM"]) ):
		i = i + 1
	start_drum = i	
	print("found DRUM at offset:", start_drum, hex(start_drum))	
	i = i + 4
	dlen = struct.unpack('H', raw[i:i+2])[0]
	print("drum section len:", dlen)
	i = i + 4
	nsect = struct.unpack('H', raw[i:i+2])[0]
	print("n. sections:", nsect)
	i = i + 2
	sect_offs = []
	for j in range(nsect):
		offs = struct.unpack('L', raw[i:i+4])[0]
		sect_offs.append(offs)
		i = i + 4
	# final offset
	sect_offs.append(start_drum + dlen)	
	print([hex(x) for x in sect_offs]) # debug
	for j in range(nsect):
		print("Sect. #", j+1)
		i = sect_offs[j]
		while i < sect_offs[j+1]:
			b1 = raw[i]
			b2 = raw[i+1]
			b3 = raw[i+2]
			dr = '{0:24s}'.format(pretty_midi.note_number_to_drum_name(b2))
			print("time: ", b1, "\tnote: ", b2, "\t", dr, "\tvel: ", b3)
			i = i + 3

def parse_othr(raw, offset=0):
	i = offset
	max_i = len(raw[i:]) - 4
	while (i < max_i) and ( raw[i:i+4] != array.array('B', [ord(x) for x in "OTHR"]) ):
		i = i + 1
	start_othr = i	
	print("found OTHR at offset:", start_othr, hex(start_othr))	
	i = i + 4
	dlen = struct.unpack('H', raw[i:i+2])[0]
	print("othr section len:", dlen)
	i = i + 4
	nsect = struct.unpack('H', raw[i:i+2])[0]
	print("n. sections:", nsect)
	i = i + 2
	sect_offs = []
	for j in range(nsect):
		offs = struct.unpack('L', raw[i:i+4])[0]
		sect_offs.append(offs)
		i = i + 4
	# final offset
	sect_offs.append(start_othr + dlen)	
	print([hex(x) for x in sect_offs]) # debug
	for j in range(nsect):
		print("Sect. #", j+1)
		i = sect_offs[j]
		while i < sect_offs[j+1]:
			b1 = raw[i]
			b2 = raw[i+1]
			b3 = raw[i+2]
			if b2 <= 120:
				dr = '{0:6s}'.format(pretty_midi.note_number_to_name(b2))
			else:
				dr = "######"
			print("time: ", b1, "\tnote: ", b2, "\t", dr, "\tvel: ", b3)
			i = i + 3
		
if len(sys.argv) > 1:
	gestione_file(sys.argv[1])
